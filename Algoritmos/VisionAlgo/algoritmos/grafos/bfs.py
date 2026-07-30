"""
BFS (Búsqueda en Amplitud) con generador para animación.
"""

from collections import deque

def bfs_generator(grafo, inicio):
    """
    Recorre un grafo usando BFS paso a paso.
    
    Args:
        grafo: Diccionario de adyacencia {nodo: [(vecino, peso)]}
        inicio: Nodo inicial
    
    Yields:
        tuple: (nodo_actual, visitados, camino, cola, operacion)
    """
    if inicio not in grafo:
        yield None, [], [], [], "error"
        return
    
    visitados = set()
    cola = deque([inicio])
    visitados.add(inicio)
    camino = [inicio]  # Solo nodos, no tuplas
    
    yield inicio, list(visitados), camino.copy(), list(cola), "inicio"
    
    while cola:
        actual = cola.popleft()
        
        yield actual, list(visitados), camino.copy(), list(cola), "visitando"
        
        # Explorar vecinos - extraer solo el nodo (primer elemento de la tupla)
        for vecino, peso in grafo.get(actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)
                camino.append(vecino)
                yield vecino, list(visitados), camino.copy(), list(cola), "agregado"
        
        yield actual, list(visitados), camino.copy(), list(cola), "procesado"
    
    yield None, list(visitados), camino.copy(), [], "completado"