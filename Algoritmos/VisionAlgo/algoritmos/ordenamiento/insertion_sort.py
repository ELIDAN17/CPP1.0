"""
Insertion Sort con generador para animación paso a paso.
Inserta cada elemento en su posición correcta dentro de la parte ya ordenada.
"""

def insertion_sort_generator(arr):
    """
    Generador que produce el estado del array después de cada comparación/intercambio.
    
    Args:
        arr: Lista de números a ordenar (se modifica in-place)
    
    Yields:
        tuple: (lista_actual, idx_actual, idx_comparado, operacion)
        - idx_actual: posición del elemento que estamos insertando
        - idx_comparado: posición con la que se está comparando
        - operacion: "comparing", "shifting", "inserted", "sorted_boundary", "finished"
    """
    n = len(arr)
    lista = arr.copy()
    
    for i in range(1, n):
        clave = lista[i]
        j = i - 1
        
        # Resaltar el elemento que vamos a insertar
        yield lista, i, -1, "selecting"
        
        # Desplazar elementos mayores que la clave
        while j >= 0 and lista[j] > clave:
            # Comparando
            yield lista, i, j, "comparing"
            
            # Desplazamiento (shifting)
            yield lista, j, j + 1, "shifting"
            lista[j + 1] = lista[j]
            j -= 1
        
        # Insertar la clave en su posición
        lista[j + 1] = clave
        yield lista, j + 1, -1, "inserted"
        
        # Marcar hasta i como ordenado
        yield lista, i, -1, "sorted_boundary"
    
    # Estado final
    yield lista, -1, -1, "finished"