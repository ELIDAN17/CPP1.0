"""
Dijkstra (Camino mínimo) con generador para animación.
"""

import heapq

def dijkstra_generator(grafo, inicio, fin=None):
    """
    Encuentra el camino mínimo usando Dijkstra paso a paso.
    
    Args:
        grafo: Diccionario de adyacencia {nodo: [(vecino, peso)]}
        inicio: Nodo inicial
        fin: Nodo destino (opcional)
    
    Yields:
        tuple: (nodo_actual, distancias, visitados, camino, operacion)
    """
    if inicio not in grafo:
        yield None, {}, [], [], "error"
        return
    
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    visitados = set()
    cola = [(0, inicio)]
    padres = {inicio: None}
    camino_final = []  # Para Dijkstra, solo al final
    
    yield inicio, distancias.copy(), list(visitados), [], "inicio"
    
    while cola:
        dist_actual, actual = heapq.heappop(cola)
        
        if actual in visitados:
            continue
        
        visitados.add(actual)
        yield actual, distancias.copy(), list(visitados), [], "visitando"
        
        if fin and actual == fin:
            camino = []
            nodo = fin
            while nodo is not None:
                camino.append(str(nodo))
                nodo = padres.get(nodo)
            camino.reverse()
            yield actual, distancias.copy(), list(visitados), camino, "encontrado"
            return
        
        for vecino, peso in grafo.get(actual, []):
            if vecino not in visitados:
                nueva_dist = dist_actual + peso
                if nueva_dist < distancias[vecino]:
                    distancias[vecino] = nueva_dist
                    padres[vecino] = actual
                    heapq.heappush(cola, (nueva_dist, vecino))
                    yield vecino, distancias.copy(), list(visitados), [], "actualizando"
    
    # Si no se encontró el destino
    if fin and fin in padres:
        camino = []
        nodo = fin
        while nodo is not None:
            camino.append(str(nodo))
            nodo = padres.get(nodo)
        camino.reverse()
    else:
        camino = []
    
    yield None, distancias.copy(), list(visitados), camino, "completado"