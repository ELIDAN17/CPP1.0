"""
Bubble Sort con generador para animación paso a paso.
Cada yield devuelve (lista, indice1, indice2, tipo_operacion)
"""

def bubble_sort_generator(arr):
    """
    Generador que produce el estado del array después de cada comparación/intercambio.
    
    Args:
        arr: Lista de números a ordenar (se modifica in-place)
    
    Yields:
        tuple: (lista_actual, idx_a, idx_b, operacion)
        - idx_a, idx_b: índices involucrados (o -1 si no aplica)
        - operacion: "comparing", "swapping", "sorted_boundary", "finished"
    """
    n = len(arr)
    # Copiar para no modificar la original fuera del generador
    lista = arr.copy()
    
    for i in range(n - 1):
        intercambiado = False
        
        for j in range(n - i - 1):
            # Estado: comparando arr[j] y arr[j+1]
            yield lista, j, j + 1, "comparing"
            
            if lista[j] > lista[j + 1]:
                # Estado: intercambiando
                yield lista, j, j + 1, "swapping"
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                intercambiado = True
        
        # Marcar el último elemento como "ya ordenado"
        yield lista, n - i - 1, -1, "sorted_boundary"
        
        if not intercambiado:
            break
    
    # Estado final: todo ordenado
    yield lista, -1, -1, "finished"