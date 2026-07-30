"""
Selection Sort con generador para animación paso a paso.
En cada iteración, encuentra el mínimo y lo coloca en la posición correcta.
"""

def selection_sort_generator(arr):
    """
    Generador que produce el estado del array después de cada comparación/intercambio.
    
    Args:
        arr: Lista de números a ordenar (se modifica in-place)
    
    Yields:
        tuple: (lista_actual, idx_actual, idx_minimo, operacion)
        - idx_actual: posición que estamos intentando llenar
        - idx_minimo: índice del mínimo encontrado hasta ahora
        - operacion: "searching", "found_min", "swapping", "finished"
    """
    n = len(arr)
    lista = arr.copy()
    
    for i in range(n - 1):
        # Asumimos que el mínimo está en i
        idx_minimo = i
        
        # Buscar el mínimo en el resto del arreglo
        for j in range(i + 1, n):
            # Estado: comparando
            yield lista, i, j, "comparing"
            
            if lista[j] < lista[idx_minimo]:
                idx_minimo = j
                # Encontramos un nuevo mínimo
                yield lista, i, idx_minimo, "found_min"
        
        # Si el mínimo no está en i, intercambiamos
        if idx_minimo != i:
            yield lista, i, idx_minimo, "swapping"
            lista[i], lista[idx_minimo] = lista[idx_minimo], lista[i]
        
        # Marcar la posición i como ordenada
        yield lista, i, -1, "sorted_boundary"
    
    # Estado final
    yield lista, -1, -1, "finished"