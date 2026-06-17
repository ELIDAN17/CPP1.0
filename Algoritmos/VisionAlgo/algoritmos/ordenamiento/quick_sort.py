"""
Quick Sort con generador para animación paso a paso.
Usa una pila manual para simular la recursión sin perder el control del generador.
"""

def quick_sort_generator(arr):
    """
    Generador que produce el estado del array después de cada operación importante.
    
    Args:
        arr: Lista de números a ordenar (se modifica in-place)
    
    Yields:
        tuple: (lista_actual, idx_izq, idx_der, idx_pivote, operacion)
    """
    lista = arr.copy()
    n = len(lista)
    
    # Usamos una pila manual para simular recursión: (inicio, fin)
    pila = [(0, n - 1)]
    
    while pila:
        inicio, fin = pila.pop()
        
        if inicio >= fin:
            continue
        
        # Mostrar el rango actual
        yield lista, inicio, fin, -1, "selecting_range"
        
        # Partición
        pivote = lista[fin]
        i = inicio - 1
        
        for j in range(inicio, fin):
            # Comparando
            yield lista, i + 1, j, fin, "comparing"
            
            if lista[j] <= pivote:
                i += 1
                if i != j:
                    # Intercambio
                    yield lista, i, j, fin, "swapping"
                    lista[i], lista[j] = lista[j], lista[i]
        
        # Colocar pivote en su posición final
        i += 1
        if i != fin:
            yield lista, i, fin, fin, "swapping_pivot"
            lista[i], lista[fin] = lista[fin], lista[i]
        
        # Marcar pivote como ordenado
        yield lista, i, -1, -1, "pivot_placed"
        
        # Agregar subproblemas a la pila (primero el derecho para que se procese después)
        if i + 1 < fin:
            pila.append((i + 1, fin))
        if inicio < i - 1:
            pila.append((inicio, i - 1))
    
    # Estado final
    yield lista, -1, -1, -1, "finished"