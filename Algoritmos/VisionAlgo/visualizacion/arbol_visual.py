"""
Visualización de árboles binarios con Plotly y NetworkX.
Muestra información del nodo en el gráfico.
"""

import plotly.graph_objects as go
import networkx as nx

def dibujar_arbol(raiz, nodo_destacado=None, operacion="normal", info_extra=None):
    """
    Dibuja un árbol binario mostrando información en el gráfico.
    
    Args:
        raiz: Nodo raíz del árbol
        nodo_destacado: Nodo a resaltar (opcional)
        operacion: Tipo de operación
        info_extra: Información adicional para mostrar en el gráfico
    """
    # Caso: árbol vacío
    if raiz is None:
        fig = go.Figure()
        fig.add_annotation(
            text="🌳 Árbol vacío<br><br>💡 Inserta valores para comenzar",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=20, color="#888"),
            align="center"
        )
        fig.update_layout(
            height=550,
            template="plotly_white",
            xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False)
        )
        return fig
    
    # Construir grafo
    G = nx.DiGraph()
    pos = {}
    nodo_info = {}  # Para almacenar información de cada nodo
    
    def construir_grafo(nodo, x=0, y=0, nivel=0, ancho_total=1):
        if nodo is None:
            return
        
        # Guardar información del nodo
        info = []
        if hasattr(nodo, 'altura'):
            info.append(f"h={nodo.altura}")
        if hasattr(nodo, 'color'):
            info.append(f"color={nodo.color}")
        if hasattr(nodo, 'factor_balance'):
            info.append(f"fb={nodo.factor_balance}")
        
        nodo_info[nodo.valor] = {
            "info": " | ".join(info) if info else "",
            "izquierdo": nodo.izquierdo.valor if nodo.izquierdo else None,
            "derecho": nodo.derecho.valor if nodo.derecho else None,
            "es_hoja": nodo.izquierdo is None and nodo.derecho is None
        }
        
        pos[nodo.valor] = (x, y)
        G.add_node(nodo.valor)
        
        desplazamiento = ancho_total / (2 ** (nivel + 2))
        
        if nodo.izquierdo:
            G.add_edge(nodo.valor, nodo.izquierdo.valor)
            construir_grafo(nodo.izquierdo, x - desplazamiento, y - 1.5, nivel + 1, ancho_total)
        
        if nodo.derecho:
            G.add_edge(nodo.valor, nodo.derecho.valor)
            construir_grafo(nodo.derecho, x + desplazamiento, y - 1.5, nivel + 1, ancho_total)
    
    construir_grafo(raiz, x=0, y=0, nivel=0, ancho_total=6)
    
    # Escalar posiciones
    pos_escaladas = {}
    for key, (x, y) in pos.items():
        pos_escaladas[key] = (x * 1.5, y * 1.5)
    
    # ========== COLORES ==========
    colores_nodos = []
    colores_bordes = []
    tamanos = []
    etiquetas = []
    textos_hover = []
    etiquetas_info = []
    
    nodo_destacado_valor = nodo_destacado.valor if nodo_destacado else None
    
    for nodo_valor in G.nodes():
        # Obtener información del nodo
        info = nodo_info.get(nodo_valor, {})
        info_texto = info.get("info", "")
        es_hoja = info.get("es_hoja", False)
        
        # Texto principal (valor)
        etiquetas.append(str(nodo_valor))
        
        # Texto de información (debajo del valor)
        if info_texto:
            etiquetas_info.append(info_texto)
        else:
            etiquetas_info.append("")
        
        # Hover con información detallada
        hover_text = f"<b>Valor: {nodo_valor}</b><br>"
        hover_text += f"Izquierdo: {info.get('izquierdo', 'None')}<br>"
        hover_text += f"Derecho: {info.get('derecho', 'None')}<br>"
        hover_text += f"Hoja: {'Sí' if es_hoja else 'No'}<br>"
        if info_texto:
            hover_text += f"Info: {info_texto}"
        textos_hover.append(hover_text)
        
        # Colores según estado
        if nodo_destacado and nodo_valor == nodo_destacado_valor:
            if operacion in ["encontrado", "encontrado_sucesor"]:
                colores_nodos.append("#2ca02c")  # Verde
                colores_bordes.append("#1a6b1a")
                tamanos.append(45)
            elif operacion in ["insertado", "insertado_izquierdo", "insertado_derecho", "insertado_raiz"]:
                colores_nodos.append("#e377c2")  # Púrpura
                colores_bordes.append("#8b4a8b")
                tamanos.append(45)
            elif operacion in ["visitando", "comparando"]:
                colores_nodos.append("#ff7f0e")  # Naranja
                colores_bordes.append("#cc6600")
                tamanos.append(40)
            elif operacion in ["eliminando", "eliminado"]:
                colores_nodos.append("#d62728")  # Rojo
                colores_bordes.append("#8b0000")
                tamanos.append(40)
            elif operacion in ["rotacion_derecha", "rotacion_izquierda"]:
                colores_nodos.append("#9467bd")  # Morado
                colores_bordes.append("#6b3a7a")
                tamanos.append(45)
            elif operacion in ["balanceado", "reemplazando"]:
                colores_nodos.append("#17becf")  # Cyan
                colores_bordes.append("#0a7a8a")
                tamanos.append(40)
            else:
                colores_nodos.append("#ff7f0e")  # Naranja
                colores_bordes.append("#cc6600")
                tamanos.append(40)
        else:
            # Colores según tipo de árbol
            if hasattr(nodo_destacado, 'color') and nodo_destacado.color == "negro":
                colores_nodos.append("#2c3e50")  # Negro
                colores_bordes.append("#1a1a1a")
            elif hasattr(nodo_destacado, 'color') and nodo_destacado.color == "rojo":
                colores_nodos.append("#e74c3c")  # Rojo
                colores_bordes.append("#8b0000")
            else:
                colores_nodos.append("#1f77b4")  # Azul
                colores_bordes.append("#0f4a7a")
            tamanos.append(30)
    
    # ========== CREAR FIGURA ==========
    fig = go.Figure()
    
    # Dibujar aristas
    for edge in G.edges():
        if edge[0] in pos_escaladas and edge[1] in pos_escaladas:
            x0, y0 = pos_escaladas[edge[0]]
            x1, y1 = pos_escaladas[edge[1]]
            fig.add_trace(go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode="lines",
                line=dict(color="#888", width=2),
                hoverinfo="none",
                showlegend=False
            ))
    
    # Dibujar nodos
    fig.add_trace(go.Scatter(
        x=[pos_escaladas[n][0] for n in G.nodes()],
        y=[pos_escaladas[n][1] for n in G.nodes()],
        mode="markers+text",
        marker=dict(
            size=tamanos,
            color=colores_nodos,
            line=dict(color=colores_bordes, width=2)
        ),
        text=etiquetas,
        textposition="middle center",
        textfont=dict(color="white", size=12, family="Arial Black"),
        hoverinfo="text",
        hovertext=textos_hover,
        showlegend=False
    ))
    
    # ========== TÍTULO Y SUBTÍTULO ==========
    titulos = {
        "normal": "🌳 Árbol Binario",
        "visitando": "🔍 Visitando nodo",
        "comparando": "🔍 Comparando valores",
        "insertado": "✅ Nodo insertado",
        "insertado_izquierdo": "✅ Nodo insertado (izquierdo)",
        "insertado_derecho": "✅ Nodo insertado (derecho)",
        "insertado_raiz": "✅ Raíz insertada",
        "encontrado": "🎯 Nodo encontrado",
        "encontrado_sucesor": "🎯 Sucesor encontrado",
        "no_encontrado": "❌ Nodo no encontrado",
        "ya_existe": "⚠️ El nodo ya existe",
        "vacio": "🌳 Árbol vacío",
        "eliminando": "🗑️ Eliminando nodo",
        "eliminado": "✅ Nodo eliminado",
        "eliminado_sin_hijos": "✅ Eliminado (sin hijos)",
        "eliminado_un_hijo": "✅ Eliminado (un hijo)",
        "reemplazando": "🔄 Reemplazando nodo",
        "buscando_sucesor": "🔍 Buscando sucesor",
        "sucesor_encontrado": "🎯 Sucesor encontrado",
        "reemplazado_por_sucesor": "🔄 Reemplazado por sucesor",
        "rotacion_derecha": "🔄 Rotación derecha",
        "rotacion_izquierda": "🔄 Rotación izquierda",
        "balanceado": "⚖️ Árbol balanceado",
        "caso_tio_rojo": "🔄 Caso: tío rojo",
        "raiz_negra": "⚫ Raíz negra",
        "nueva_raiz": "🌳 Nueva raíz",
        "dividiendo_hijo": "📊 Dividiendo hijo",
        "insertado_en_hoja": "✅ Insertado en hoja",
        "accediendo_hijo": "📂 Accediendo a hijo",
        "buscando_hijo": "🔍 Buscando hijo",
        "actualizando_enlace": "🔗 Actualizando enlace",
    }
    
    titulo = titulos.get(operacion, f"🌳 {operacion}")
    
    # ========== INFORMACIÓN EXTRA EN EL GRÁFICO ==========
    info_extra_texto = ""
    if info_extra:
        if isinstance(info_extra, dict):
            info_parts = []
            for key, value in info_extra.items():
                if value is not None:
                    info_parts.append(f"{key}: {value}")
            info_extra_texto = " | ".join(info_parts)
        else:
            info_extra_texto = str(info_extra)
    
    # ========== CONFIGURAR LAYOUT ==========
    fig.update_layout(
        title={
            'text': titulo,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Arial', 'weight': 'bold'}
        },
        height=600,
        template="plotly_white",
        showlegend=False,
        xaxis=dict(
            showticklabels=False, 
            showgrid=False, 
            zeroline=False,
            range=[-5, 5]
        ),
        yaxis=dict(
            showticklabels=False, 
            showgrid=False, 
            zeroline=False,
            range=[-5.5, 1]
        ),
        margin=dict(l=40, r=40, t=80, b=60),
        annotations=[]
    )
    
    # Añadir información extra como anotación
    if info_extra_texto:
        fig.add_annotation(
            text=f"📌 {info_extra_texto}",
            xref="paper", yref="paper",
            x=0.5, y=-0.08,
            showarrow=False,
            font=dict(size=12, color="#555", family="Arial"),
            align="center",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#ccc",
            borderwidth=1,
            borderpad=4
        )
    
    return fig