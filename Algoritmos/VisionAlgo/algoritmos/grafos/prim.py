"""
PRIM (Árbol de Expansión Mínima) con generador para animación.
"""

import heapq

def prim_generator(grafo, inicio):
    """
    Encuentra el árbol de expansión mínima usando PRIM paso a paso.
    
    Args:
        grafo: Diccionario de adyacencia {nodo: [(vecino, peso)]}
        inicio: Nodo inicial
    
    Yields:
        tuple: (nodo_actual, arbol, visitados, aristas, operacion)
    """
    if inicio not in grafo:
        yield None, [], [], [], "error"
        return
    
    visitados = set([inicio])
    arbol = []  # Lista de aristas (u, v, peso)
    aristas = []  # Cola de aristas candidatas
    
    # Agregar aristas del nodo inicial
    for vecino, peso in grafo.get(inicio, []):
        heapq.heappush(aristas, (peso, inicio, vecino))
    
    yield inicio, arbol.copy(), list(visitados), aristas.copy(), "inicio"
    
    total_peso = 0
    
    while aristas and len(visitados) < len(grafo):
        peso, u, v = heapq.heappop(aristas)
        
        yield v, arbol.copy(), list(visitados), aristas.copy(), "evaluando"
        
        if v in visitados:
            yield v, arbol.copy(), list(visitados), aristas.copy(), "descartado"
            continue
        
        # Agregar arista al árbol
        visitados.add(v)
        arbol.append((u, v, peso))
        total_peso += peso
        
        yield v, arbol.copy(), list(visitados), aristas.copy(), "agregado"
        
        # Agregar nuevas aristas
        for vecino, peso_arista in grafo.get(v, []):
            if vecino not in visitados:
                heapq.heappush(aristas, (peso_arista, v, vecino))
                yield vecino, arbol.copy(), list(visitados), aristas.copy(), "candidato"
    
    yield None, arbol.copy(), list(visitados), aristas.copy(), "completado"