"""
Shell Sort con generador para animación paso a paso.
Es una versión mejorada de Insertion Sort que usa "gaps" (intervalos) para mover elementos más rápido.
"""

def shell_sort_generator(arr):
    """
    Generador que produce el estado del array durante el ordenamiento Shell Sort.
    
    Shell Sort funciona así:
    1. Define una secuencia de gaps (intervalos)
    2. Para cada gap, aplica Insertion Sort a elementos separados por ese gap
    3. Reduce el gap progresivamente hasta llegar a 1
    
    Args:
        arr: Lista de números a ordenar (se modifica in-place)
    
    Yields:
        tuple: (lista_actual, idx_actual, idx_comparado, gap_actual, operacion)
    """
    lista = arr.copy()
    n = len(lista)
    
    # Secuencia de gaps (secuencia de Shell original)
    gaps = []
    gap = n // 2
    while gap > 0:
        gaps.append(gap)
        gap //= 2
    
    for gap in gaps:
        # Mostrar el gap actual
        yield lista, -1, -1, gap, "new_gap"
        
        # Aplicar Insertion Sort con este gap
        for i in range(gap, n):
            temp = lista[i]
            j = i
            
            # Resaltar el elemento que estamos insertando
            yield lista, i, -1, gap, "selecting"
            
            # Desplazar elementos que están separados por 'gap'
            while j >= gap and lista[j - gap] > temp:
                # Comparando
                yield lista, j, j - gap, gap, "comparing"
                
                # Desplazamiento
                yield lista, j, j - gap, gap, "shifting"
                lista[j] = lista[j - gap]
                j -= gap
            
            # Insertar el elemento en su posición
            lista[j] = temp
            if i != j:
                yield lista, j, i, gap, "inserted"
            
            # Marcar progreso
            yield lista, j, -1, gap, "progress"
        
        # Marcar que este gap está completo
        yield lista, -1, -1, gap, "gap_complete"
    
    # Estado final
    yield lista, -1, -1, 0, "finished"