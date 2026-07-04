"""
Visualización de árboles binarios y B-Trees con Plotly y NetworkX.
Muestra información del nodo en el gráfico.
"""

import plotly.graph_objects as go
import networkx as nx

def es_nodo_b(nodo):
    """Verifica si un nodo es de tipo B (tiene claves y hijos)."""
    return hasattr(nodo, 'claves') and hasattr(nodo, 'hijos')

def dibujar_arbol(raiz, nodo_destacado=None, operacion="normal", info_extra=None):
    """
    Dibuja un árbol (binario o B-Tree) mostrando información en el gráfico.
    
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
    
    # ========== DETECTAR SI ES ÁRBOL B ==========
    if es_nodo_b(raiz):
        return _dibujar_arbol_b(raiz, nodo_destacado, operacion, info_extra)
    
    # ========== ÁRBOL BINARIO NORMAL ==========
    return _dibujar_arbol_binario(raiz, nodo_destacado, operacion, info_extra)


def _dibujar_arbol_b(raiz, nodo_destacado=None, operacion="normal", info_extra=None):
    """
    Dibuja un árbol B (multinodo) usando Plotly.
    """
    # Construir grafo
    G = nx.DiGraph()
    pos = {}
    nodo_info = {}
    nodo_destacado_id = id(nodo_destacado) if nodo_destacado else None
    
    def construir_grafo_b(nodo, x=0, y=0, nivel=0):
        if nodo is None or len(nodo.claves) == 0:
            return
        
        # Crear un ID único para el nodo
        nodo_id = id(nodo)
        claves_str = ", ".join(map(str, nodo.claves))
        
        # Posición del nodo
        pos[nodo_id] = (x, y)
        G.add_node(nodo_id, label=f"[{claves_str}]")
        nodo_info[nodo_id] = {
            "claves": nodo.claves.copy(),
            "hoja": nodo.hoja,
            "hijos": nodo.hijos,
            "es_destacado": nodo_destacado_id == nodo_id
        }
        
        # Posicionar hijos
        if nodo.hijos:
            num_hijos = len(nodo.hijos)
            desplazamiento = 1.5 / (2 ** (nivel + 1))
            for i, hijo in enumerate(nodo.hijos):
                hijo_id = id(hijo)
                G.add_edge(nodo_id, hijo_id)
                construir_grafo_b(hijo, x - desplazamiento + (i * 2 * desplazamiento / max(1, num_hijos-1)), y - 1.5, nivel + 1)
    
    construir_grafo_b(raiz, x=0, y=0, nivel=0)
    
    # Si el grafo está vacío, mostrar mensaje
    if len(G.nodes()) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="🌳 Árbol B vacío",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=20, color="#888"),
            align="center"
        )
        fig.update_layout(height=550, template="plotly_white")
        return fig
    
    # Escalar posiciones
    pos_escaladas = {}
    for key, (x, y) in pos.items():
        pos_escaladas[key] = (x * 2.5, y * 2.5)
    
    # ========== COLORES PARA ÁRBOL B ==========
    colores_nodos = []
    colores_bordes = []
    tamanos = []
    etiquetas = []
    textos_hover = []
    
    for nodo_id in G.nodes():
        info = nodo_info.get(nodo_id, {})
        label = G.nodes[nodo_id].get("label", "")
        es_hoja = info.get("hoja", False)
        es_destacado = info.get("es_destacado", False)
        
        etiquetas.append(label)
        
        hover_text = f"<b>Claves: {info.get('claves', [])}</b><br>"
        hover_text += f"Hoja: {'Sí' if es_hoja else 'No'}<br>"
        hover_text += f"Hijos: {len(info.get('hijos', []))}"
        textos_hover.append(hover_text)
        
        # Color según tipo y estado
        if es_destacado:
            color = "#ff7f0e"  # Naranja para destacado
            borde = "#cc6600"
            size = 45
        elif es_hoja:
            color = "#2ca02c"  # Verde para hojas
            borde = "#1a6b1a"
            size = 35
        else:
            color = "#1f77b4"  # Azul para nodos internos
            borde = "#0f4a7a"
            size = 35
        
        colores_nodos.append(color)
        colores_bordes.append(borde)
        tamanos.append(size)
    
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
        textfont=dict(color="white", size=10, family="Arial"),
        hoverinfo="text",
        hovertext=textos_hover,
        showlegend=False
    ))
    
    # ========== TÍTULO ==========
    titulo = "🌳 Árbol B"
    if operacion != "normal":
        titulo = f"🌳 Árbol B - {operacion}"
    
    # Información extra
    info_extra_texto = ""
    if info_extra and isinstance(info_extra, dict):
        info_parts = []
        for key, value in info_extra.items():
            if value is not None and key != "color":
                info_parts.append(f"{key}: {value}")
        info_extra_texto = " | ".join(info_parts)
    
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
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[-5, 5]),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[-5.5, 1]),
        margin=dict(l=40, r=40, t=80, b=60)
    )
    
    if info_extra_texto:
        fig.add_annotation(
            text=f"📌 {info_extra_texto}",
            xref="paper", yref="paper",
            x=0.5, y=-0.08,
            showarrow=False,
            font=dict(size=12, color="#555"),
            align="center",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#ccc",
            borderwidth=1,
            borderpad=4
        )
    
    return fig


def _dibujar_arbol_binario(raiz, nodo_destacado=None, operacion="normal", info_extra=None):
    """
    Dibuja un árbol binario estándar (ABB, AVL, Rojo-Negro).
    (Tu código original completo va aquí)
    """
    # ========== DETECTAR SI ES ROJO-NEGRO ==========
    def es_rojo_negro(nodo):
        """Verifica si todos los nodos tienen atributo 'color'."""
        if nodo is None:
            return False
        if not hasattr(nodo, 'color'):
            return False
        def revisar(n):
            if n is None:
                return True
            if not hasattr(n, 'color'):
                return False
            return revisar(n.izquierdo) and revisar(n.derecho)
        return revisar(nodo)
    
    es_rn = es_rojo_negro(raiz)
    
    # ========== CONSTRUIR GRAFO ==========
    G = nx.DiGraph()
    pos = {}
    nodo_info = {}
    colores_reales = {}
    
    def construir_grafo(nodo, x=0, y=0, nivel=0, ancho_total=1):
        if nodo is None:
            return
        
        info = []
        if hasattr(nodo, 'altura'):
            info.append(f"h={nodo.altura}")
        if hasattr(nodo, 'color'):
            info.append(f"color={nodo.color}")
            colores_reales[nodo.valor] = nodo.color
        if hasattr(nodo, 'factor_balance'):
            info.append(f"fb={nodo.factor_balance}")
        
        nodo_info[nodo.valor] = {
            "info": " | ".join(info) if info else "",
            "izquierdo": nodo.izquierdo.valor if nodo.izquierdo else None,
            "derecho": nodo.derecho.valor if nodo.derecho else None,
            "es_hoja": nodo.izquierdo is None and nodo.derecho is None,
            "color": nodo.color if hasattr(nodo, 'color') else None
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
    
    nodo_destacado_valor = nodo_destacado.valor if nodo_destacado else None
    
    for nodo_valor in G.nodes():
        info = nodo_info.get(nodo_valor, {})
        info_texto = info.get("info", "")
        es_hoja = info.get("es_hoja", False)
        color_nodo = info.get("color", None)
        
        etiquetas.append(str(nodo_valor))
        
        hover_text = f"<b>Valor: {nodo_valor}</b><br>"
        hover_text += f"Izquierdo: {info.get('izquierdo', 'None')}<br>"
        hover_text += f"Derecho: {info.get('derecho', 'None')}<br>"
        hover_text += f"Hoja: {'Sí' if es_hoja else 'No'}<br>"
        if info_texto:
            hover_text += f"Info: {info_texto}"
        textos_hover.append(hover_text)
        
        # ===== DETERMINAR COLOR DEL NODO =====
        if nodo_destacado and nodo_valor == nodo_destacado_valor:
            if operacion in ["encontrado", "encontrado_sucesor"]:
                colores_nodos.append("#2ca02c")
                colores_bordes.append("#1a6b1a")
                tamanos.append(45)
            elif operacion in ["insertado", "insertado_izquierdo", "insertado_derecho", "insertado_raiz"]:
                colores_nodos.append("#e377c2")
                colores_bordes.append("#8b4a8b")
                tamanos.append(45)
            elif operacion in ["visitando", "comparando"]:
                colores_nodos.append("#ff7f0e")
                colores_bordes.append("#cc6600")
                tamanos.append(40)
            elif operacion in ["eliminando", "eliminado"]:
                colores_nodos.append("#d62728")
                colores_bordes.append("#8b0000")
                tamanos.append(40)
            elif operacion in ["rotacion_derecha", "rotacion_izquierda"]:
                colores_nodos.append("#9467bd")
                colores_bordes.append("#6b3a7a")
                tamanos.append(45)
            elif operacion in ["balanceado", "reemplazando"]:
                colores_nodos.append("#17becf")
                colores_bordes.append("#0a7a8a")
                tamanos.append(40)
            else:
                colores_nodos.append("#ff7f0e")
                colores_bordes.append("#cc6600")
                tamanos.append(40)
        else:
            if es_rn and color_nodo:
                if color_nodo == "negro":
                    colores_nodos.append("#2c3e50")
                    colores_bordes.append("#1a1a1a")
                else:
                    colores_nodos.append("#e74c3c")
                    colores_bordes.append("#8b0000")
            else:
                colores_nodos.append("#1f77b4")
                colores_bordes.append("#0f4a7a")
            tamanos.append(30)
    
    # ========== CREAR FIGURA ==========
    fig = go.Figure()
    
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
    
    # Título
    titulos = {
        "normal": "🌳 Árbol Binario",
        "visitando": "🔍 Visitando nodo",
        "insertado": "✅ Nodo insertado",
        "insertado_izquierdo": "✅ Nodo insertado (izquierdo)",
        "insertado_derecho": "✅ Nodo insertado (derecho)",
        "insertado_raiz": "✅ Raíz insertada",
        "encontrado": "🎯 Nodo encontrado",
        "no_encontrado": "❌ Nodo no encontrado",
        "ya_existe": "⚠️ El nodo ya existe",
        "eliminando": "🗑️ Eliminando nodo",
        "eliminado": "✅ Nodo eliminado",
        "rotacion_derecha": "🔄 Rotación derecha",
        "rotacion_izquierda": "🔄 Rotación izquierda",
        "balanceado": "⚖️ Árbol balanceado",
        "raiz_negra": "⚫ Raíz negra",
        "caso_tio_rojo": "🔄 Caso: tío rojo",
    }
    
    titulo = titulos.get(operacion, f"🌳 {operacion}")
    
    info_extra_texto = ""
    if info_extra and isinstance(info_extra, dict):
        info_parts = []
        for key, value in info_extra.items():
            if value is not None and key != "color":
                info_parts.append(f"{key}: {value}")
        info_extra_texto = " | ".join(info_parts)
    
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
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[-5, 5]),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[-5.5, 1]),
        margin=dict(l=40, r=40, t=80, b=60),
    )
    
    if info_extra_texto:
        fig.add_annotation(
            text=f"📌 {info_extra_texto}",
            xref="paper", yref="paper",
            x=0.5, y=-0.08,
            showarrow=False,
            font=dict(size=12, color="#555"),
            align="center",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#ccc",
            borderwidth=1,
            borderpad=4
        )
    
    return fig