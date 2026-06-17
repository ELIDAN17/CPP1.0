"""
Visualización para algoritmos de búsqueda con Plotly.
"""

import plotly.graph_objects as go

def dibujar_busqueda(lista, idx_actual=-1, izquierda=-1, derecha=-1, medio=-1, operacion="normal"):
    """
    Dibuja un gráfico de barras con colores según la operación de búsqueda.
    
    Args:
        lista: Lista de números
        idx_actual: Índice que se está revisando
        izquierda: Límite izquierdo (para binaria)
        derecha: Límite derecho (para binaria)
        medio: Índice medio (para binaria)
        operacion: "buscando", "encontrado", "no_encontrado", etc.
    """
    n = len(lista)
    
    # ========== CASO ESPECIAL: LISTA VACÍA ==========
    if n == 0:
        fig = go.Figure()
        fig.update_layout(
            title="📊 Lista vacía",
            height=400,
            template="plotly_white",
            xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False)
        )
        fig.add_annotation(
            text="No hay elementos en la lista",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=20, color="#888"),
            align="center"
        )
        return fig
    
    colores = ["#1f77b4"] * n  # Azul por defecto
    
    # ========== ASIGNAR COLORES SEGÚN OPERACIÓN ==========
    if operacion == "buscando" and idx_actual != -1 and 0 <= idx_actual < n:
        colores[idx_actual] = "#ff7f0e"  # Naranja
        if izquierda != -1 and derecha != -1:
            for i in range(izquierda, derecha + 1):
                if i != idx_actual:
                    colores[i] = "#c5c5c5"  # Gris claro
        titulo = f"🔍 Buscando: posición {idx_actual} = {lista[idx_actual]}"
        subtitulo = f"Rango activo: [{izquierda}...{derecha}]" if izquierda != -1 else ""
    
    elif operacion == "encontrado" and idx_actual != -1 and 0 <= idx_actual < n:
        colores[idx_actual] = "#2ca02c"  # Verde
        titulo = f"✅ ¡ENCONTRADO! posición {idx_actual} = {lista[idx_actual]}"
        subtitulo = f"Valor buscado: {lista[idx_actual]}"
    
    elif operacion == "no_encontrado":
        titulo = "❌ No encontrado"
        subtitulo = "El elemento no está en la lista"
    
    elif operacion == "actualizando" and izquierda != -1 and derecha != -1:
        for i in range(izquierda, derecha + 1):
            if i != medio:
                colores[i] = "#17becf"  # Cyan (en rango)
        if medio != -1:
            colores[medio] = "#e377c2"  # Púrpura (medio)
        titulo = f"🔄 Actualizando rango: [{izquierda}...{derecha}]"
        subtitulo = f"Medio: {medio if medio != -1 else 'N/A'}"
    
    elif operacion == "expandiendo" and idx_actual != -1:
        colores[idx_actual] = "#e377c2"  # Púrpura
        titulo = f"📈 Expandiendo búsqueda: índice {idx_actual}"
        subtitulo = f"Valor: {lista[idx_actual]}"
    
    elif operacion == "rango_encontrado" and izquierda != -1 and derecha != -1:
        for i in range(izquierda, derecha + 1):
            colores[i] = "#bcbd22"  # Verde oliva
        titulo = f"🎯 Rango encontrado: [{izquierda}...{derecha}]"
        subtitulo = f"Longitud: {derecha - izquierda + 1} elementos"
    
    elif operacion == "fuera_rango":
        titulo = "⚠️ Fuera de rango (datos no uniformes)"
        subtitulo = "El valor está fuera del rango estimado"
    
    elif operacion == "normal":
        titulo = f"📊 Lista de {len(lista)} elementos"
        subtitulo = "Presiona Play para iniciar la búsqueda"
    
    else:
        titulo = f"📊 Lista de {len(lista)} elementos"
        subtitulo = ""
    
    # ========== CREAR FIGURA ==========
    fig = go.Figure()
    
    # Barras
    fig.add_trace(go.Bar(
        x=list(range(n)),
        y=lista,
        marker_color=colores,
        text=[str(v) for v in lista],
        textposition='outside',
        hovertemplate='Índice: %{x}<br>Valor: %{y}<extra></extra>'
    ))
    
    # Líneas de rango
    if izquierda != -1 and derecha != -1 and operacion not in ["normal", "encontrado", "no_encontrado"]:
        # Líneas verticales en los límites
        if izquierda >= 0 and izquierda < n:
            fig.add_vline(x=izquierda - 0.5, line_color="#ff0000", line_dash="dot", line_width=2)
        if derecha >= 0 and derecha < n:
            fig.add_vline(x=derecha + 0.5, line_color="#ff0000", line_dash="dot", line_width=2)
        
        # Sombra del rango
        if izquierda >= 0 and derecha < n and izquierda <= derecha:
            fig.add_vrect(
                x0=izquierda - 0.5, x1=derecha + 0.5,
                fillcolor="rgba(255, 0, 0, 0.05)",
                line_width=0
            )
    
    # ========== CONFIGURAR LAYOUT ==========
    fig.update_layout(
        title={
            'text': titulo,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': 'Arial', 'weight': 'bold'}
        },
        xaxis_title="Índice",
        yaxis_title="Valor",
        height=500,
        template="plotly_white",
        bargap=0.15,
        showlegend=False,
        margin=dict(l=40, r=40, t=80, b=40)
    )
    
    # Configurar ejes
    fig.update_xaxes(
        tickmode='linear',
        tick0=0,
        dtick=1,
        title_font=dict(size=12)
    )
    
    fig.update_yaxes(
        title_font=dict(size=12),
        range=[0, max(lista) * 1.15 if lista else 100]
    )
    
    # Añadir subtítulo si existe
    if subtitulo:
        fig.add_annotation(
            text=subtitulo,
            xref="paper", yref="paper",
            x=0.5, y=-0.12,
            showarrow=False,
            font=dict(size=14, color="#666"),
            align="center"
        )
    
    return fig