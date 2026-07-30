"""
Dibujo del gráfico de barras usando Plotly con líneas de división y rangos.
"""

import plotly.graph_objects as go

COLORES = {
    "normal": "#1f77b4",
    "comparing": "#ff7f0e",
    "swapping": "#d62728",
    "sorted": "#2ca02c",
    "sorted_boundary": "#9467bd",
    "pivot": "#e377c2",
    "selecting": "#17becf",
    "range": "#bcbd22",
    "dividing": "#ff9896",
    "merging": "#c5b0d5",
    "segment_sorted": "#98df8a",
    "gap_highlight": "#f7b6d2",
    "shifting": "#ffbb78",
    "inserted": "#aec7e8",
    "digit_highlight": "#ffff99",
    "pass_complete": "#b2df8a",
    "error": "#ff0000",
    "counting": "#ff9896",
    "placing": "#c5b0d5",
    "copying": "#98df8a",
    "range_highlight": "#f7b6d2",
    "bucket": "#aaffc3",
    "bucket_highlight": "#ffb3ba",
    "concatenating": "#ffcc99",
}

def dibujar_barras(lista, idx1=-1, idx2=-1, idx3=-1, operacion="normal", extra=None, ancho=900, alto=500):
    """
    Dibuja un gráfico de barras interactivo con Plotly.
    Incluye líneas de división para algoritmos de divide y vencerás.
    
    Args:
        lista: Lista de números
        idx1: Primer índice a resaltar
        idx2: Segundo índice a resaltar
        idx3: Tercer índice (pivote, gap, o límite de división)
        operacion: Tipo de operación
        extra: Información adicional (límites de rango, etc.)
    """
    n = len(lista)
    colores = [COLORES["normal"]] * n
    
    # Variables para líneas de división
    lineas_division = []  # Lista de (x, color, dash, texto)
    rango_sombra = None   # (inicio, fin) para sombrear un rango
    
    # Determinar colores según operación
    if operacion == "comparing" and idx1 != -1 and idx2 != -1:
        colores[idx1] = COLORES["comparing"]
        colores[idx2] = COLORES["comparing"]
        if idx3 != -1:
            colores[idx3] = COLORES["pivot"]
        titulo = f"🔍 Comparando: {lista[idx1]} vs {lista[idx2]}"
    
    elif operacion == "swapping" and idx1 != -1 and idx2 != -1:
        colores[idx1] = COLORES["swapping"]
        colores[idx2] = COLORES["swapping"]
        if idx3 != -1:
            colores[idx3] = COLORES["pivot"]
        titulo = f"🔄 Intercambiando: {lista[idx1]} ↔ {lista[idx2]}"
    
    elif operacion == "selecting" and idx1 != -1:
        colores[idx1] = COLORES["selecting"]
        titulo = f"✨ Seleccionando: {lista[idx1]} en posición {idx1}"
    
    elif operacion == "inserted" and idx1 != -1:
        colores[idx1] = COLORES["inserted"]
        titulo = f"✅ Insertado: {lista[idx1]} en posición {idx1}"
    
    elif operacion == "sorted_boundary" and idx1 != -1:
        for i in range(idx1 + 1):
            colores[i] = COLORES["sorted"]
        titulo = f"📌 Elementos ordenados hasta posición {idx1}"
        # Línea de límite de ordenados
        lineas_division.append((idx1 + 0.5, "#2ca02c", "dash", "Ordenado"))
    
    elif operacion == "pivot_placed" and idx1 != -1:
        colores[idx1] = COLORES["pivot"]
        titulo = f"📍 Pivote {lista[idx1]} colocado en posición {idx1}"
        lineas_division.append((idx1 + 0.5, "#e377c2", "dash", "Pivote"))
    
    # ========== DIVIDE Y VENCERÁS (Merge Sort) ==========
    elif operacion == "dividing" and idx1 != -1 and idx2 != -1:
        for i in range(idx1, idx2 + 1):
            colores[i] = COLORES["dividing"]
        titulo = f"✂️ Dividiendo segmento [{idx1}...{idx2}]"
        # Línea en el medio (idx3 es el medio)
        if idx3 != -1 and idx3 > idx1 and idx3 < idx2:
            lineas_division.append((idx3 + 0.5, "#ff0000", "dot", "División"))
        # Sombra del segmento
        rango_sombra = (idx1, idx2)
    
    elif operacion == "merging_start" and idx1 != -1 and idx2 != -1:
        for i in range(idx1, idx2 + 1):
            colores[i] = COLORES["merging"]
        titulo = f"🔄 Mezclando segmentos"
        # Línea de división entre los dos subsegmentos
        if idx3 != -1:
            lineas_division.append((idx3 + 0.5, "#ff0000", "dash", "Mezcla"))
        rango_sombra = (idx1, idx2)
    
    elif operacion == "segment_sorted" and idx1 != -1 and idx2 != -1:
        for i in range(idx1, idx2 + 1):
            colores[i] = COLORES["segment_sorted"]
        titulo = f"✅ Segmento [{idx1}...{idx2}] ordenado"
        lineas_division.append((idx2 + 0.5, "#2ca02c", "dash", "Segmento ordenado"))
    
    # ========== QUICK SORT ==========
    elif operacion == "selecting_range" and idx1 != -1 and idx2 != -1:
        for i in range(idx1, idx2 + 1):
            colores[i] = COLORES["range"]
        titulo = f"🎯 Rango a ordenar: [{idx1}...{idx2}]"
        rango_sombra = (idx1, idx2)
        if idx3 != -1:
            lineas_division.append((idx3 + 0.5, "#e377c2", "dash", "Pivote"))
    
    # ========== SHELL SORT ==========
    elif operacion == "new_gap":
        gap = idx3 if idx3 > 0 else 0
        titulo = f"🎯 Nuevo gap: {gap}"
        # Líneas verticales cada 'gap' elementos
        if gap > 0:
            for i in range(gap, n, gap):
                lineas_division.append((i - 0.5, "#9467bd", "dot", f"gap={gap}"))
            for i in range(0, n, gap):
                colores[i] = COLORES["gap_highlight"]
    
    # ========== BÚSQUEDA POR INTERPOLACIÓN (extra) ==========
    elif operacion == "range_highlight" and extra:
        inicio = extra.get("inicio", -1)
        fin = extra.get("fin", -1)
        if inicio != -1 and fin != -1:
            for i in range(inicio, fin + 1):
                colores[i] = COLORES["range_highlight"]
            titulo = f"🎯 Rango activo: [{inicio}...{fin}]"
            rango_sombra = (inicio, fin)
    
    # ========== FINALIZADO ==========
    elif operacion == "finished":
        colores = [COLORES["sorted"]] * n
        titulo = "🏁 LISTA ORDENADA"
        # Línea final
        lineas_division.append((n - 0.5, "#2ca02c", "solid", "Fin"))
    
    else:
        titulo = f"📊 Estado actual - {len(lista)} elementos"
    
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
    
    # ========== SOMBRA DE RANGO ==========
    if rango_sombra:
        inicio, fin = rango_sombra
        if inicio >= 0 and fin < n and inicio <= fin:
            fig.add_vrect(
                x0=inicio - 0.5, x1=fin + 0.5,
                fillcolor="rgba(255, 0, 0, 0.05)",
                line_width=0
            )
    
    # ========== LÍNEAS DE DIVISIÓN ==========
    for x, color, dash, texto in lineas_division:
        if 0 <= x <= n:
            fig.add_vline(
                x=x,
                line_color=color,
                line_dash=dash,
                line_width=2,
                annotation_text=texto,
                annotation_position="top left" if x < n/2 else "top right",
                annotation_font_size=10,
                annotation_font_color=color
            )
    
    # ========== CONFIGURAR LAYOUT ==========
    fig.update_layout(
        title={
            'text': titulo,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'family': 'Arial', 'weight': 'bold'}
        },
        xaxis_title="Índice",
        yaxis_title="Valor",
        width=ancho,
        height=alto,
        template="plotly_white",
        bargap=0.15,
        showlegend=False,
        margin=dict(l=40, r=40, t=80, b=60)
    )
    
    # Configurar ejes
    fig.update_xaxes(
        tickmode='linear',
        tick0=0,
        dtick=1,
        title_font=dict(size=12),
        range=[-0.5, n - 0.5]
    )
    
    fig.update_yaxes(
        title_font=dict(size=12),
        range=[0, max(lista) * 1.15 if lista else 100]
    )
    
    return fig