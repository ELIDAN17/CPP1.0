"""
DFS (Búsqueda en Profundidad) con generador para animación.
"""

def dfs_generator(grafo, inicio):
    """
    Recorre un grafo usando DFS paso a paso.
    
    Args:
        grafo: Diccionario de adyacencia {nodo: [(vecino, peso)]}
        inicio: Nodo inicial
    
    Yields:
        tuple: (nodo_actual, visitados, camino, pila, operacion)
    """
    if inicio not in grafo:
        yield None, [], [], [], "error"
        return
    
    visitados = set()
    pila = [inicio]
    camino = [inicio]  # Solo nodos, no tuplas
    
    yield inicio, list(visitados), camino.copy(), list(pila), "inicio"
    
    while pila:
        actual = pila.pop()
        
        if actual not in visitados:
            visitados.add(actual)
            if actual not in camino:
                camino.append(actual)
            yield actual, list(visitados), camino.copy(), list(pila), "visitando"
            
            # Explorar vecinos - extraer solo el nodo
            for vecino, peso in grafo.get(actual, []):
                if vecino not in visitados:
                    pila.append(vecino)
                    yield vecino, list(visitados), camino.copy(), list(pila), "agregado"
        else:
            yield actual, list(visitados), camino.copy(), list(pila), "ya_visitado"
    
    yield None, list(visitados), camino.copy(), [], "completado"