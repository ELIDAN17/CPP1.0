"""
Visualización de grafos con Plotly y NetworkX.
"""

import plotly.graph_objects as go
import networkx as nx

def dibujar_grafo(grafo, nodo_destacado=None, visitados=None, camino=None, arbol=None, operacion="normal"):
    """
    Dibuja un grafo usando Plotly y NetworkX.
    
    Args:
        grafo: Diccionario de adyacencia {nodo: [(vecino, peso)]}
        nodo_destacado: Nodo a resaltar
        visitados: Lista de nodos visitados
        camino: Lista de nodos en orden de visita (para BFS/DFS)
        arbol: Lista de aristas del árbol (para PRIM)
        operacion: Tipo de operación
    """
    if not grafo:
        fig = go.Figure()
        fig.add_annotation(
            text="🔗 Grafo vacío",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=24, color="#888")
        )
        fig.update_layout(height=500, template="plotly_white")
        return fig
    
    # Construir grafo de NetworkX
    G = nx.Graph()
    
    for nodo in grafo:
        G.add_node(nodo)
    
    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos:
            G.add_edge(nodo, vecino, weight=peso)
    
    pos = nx.spring_layout(G, seed=42, k=0.5)
    
    # ========== COLORES DE NODOS ==========
    colores_nodos = []
    for nodo in G.nodes():
        if nodo_destacado and nodo == nodo_destacado:
            colores_nodos.append("#ff7f0e")  # Naranja
        elif visitados and nodo in visitados:
            colores_nodos.append("#2ca02c")  # Verde
        else:
            colores_nodos.append("#1f77b4")  # Azul
    
    # ========== COLORES DE ARISTAS ==========
    colores_aristas = []
    anchos_aristas = []
    
    # Convertir camino a set de aristas (para BFS/DFS/Dijkstra)
    camino_set = set()
    if camino and len(camino) > 1:
        for i in range(len(camino) - 1):
            u, v = str(camino[i]), str(camino[i + 1])
            camino_set.add((u, v))
            camino_set.add((v, u))
    
    # Convertir arbol a set de aristas (para PRIM)
    arbol_set = set()
    if arbol:
        for u, v, peso in arbol:
            arbol_set.add((u, v))
            arbol_set.add((v, u))
    
    for edge in G.edges():
        u, v = edge
        # Verificar si la arista está en el camino o en el árbol
        if (u, v) in camino_set or (v, u) in camino_set:
            colores_aristas.append("#d62728")  # Rojo para camino
            anchos_aristas.append(3)
        elif (u, v) in arbol_set or (v, u) in arbol_set:
            colores_aristas.append("#d62728")  # Rojo para árbol (PRIM)
            anchos_aristas.append(3)
        else:
            colores_aristas.append("#888")  # Gris normal
            anchos_aristas.append(1)
    
    # ========== CREAR FIGURA ==========
    fig = go.Figure()
    
    # Dibujar aristas
    for i, edge in enumerate(G.edges()):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        fig.add_trace(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode="lines",
            line=dict(color=colores_aristas[i], width=anchos_aristas[i]),
            hoverinfo="none",
            showlegend=False
        ))
        
        if 'weight' in G.edges[edge]:
            peso = G.edges[edge]['weight']
            mid_x, mid_y = (x0 + x1) / 2, (y0 + y1) / 2
            fig.add_annotation(
                x=mid_x, y=mid_y,
                text=str(peso),
                showarrow=False,
                font=dict(size=10, color="#666"),
                bgcolor="rgba(255,255,255,0.8)",
                borderpad=2
            )
    
    # Dibujar nodos
    fig.add_trace(go.Scatter(
        x=[pos[n][0] for n in G.nodes()],
        y=[pos[n][1] for n in G.nodes()],
        mode="markers+text",
        marker=dict(
            size=35,
            color=colores_nodos,
            line=dict(color="white", width=2)
        ),
        text=list(G.nodes()),
        textposition="middle center",
        textfont=dict(color="white", size=14, family="Arial Black"),
        hoverinfo="text",
        hovertext=[f"Nodo: {n}" for n in G.nodes()],
        showlegend=False
    ))
    
    # Título
    titulos = {
        "normal": "🔗 Grafo",
        "inicio": "🚀 Iniciando recorrido",
        "visitando": "🔍 Visitando nodo",
        "agregado": "✅ Nodo agregado",
        "procesado": "📌 Nodo procesado",
        "completado": "✅ Recorrido completado",
        "evaluando": "⚖️ Evaluando arista",
        "descartado": "❌ Arista descartada",
        "candidato": "📌 Arista candidata",
        "actualizando": "🔄 Actualizando distancia",
        "encontrado": "🎯 Camino encontrado",
        "ya_visitado": "⏭️ Nodo ya visitado",
    }
    
    titulo = titulos.get(operacion, f"🔗 {operacion}")
    
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
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig