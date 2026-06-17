"""
Merge Sort con generador para animación paso a paso.
Muestra el proceso de división y mezcla.
"""

def merge_sort_generator(arr):
    """
    Generador que produce el estado del array durante el ordenamiento Merge Sort.
    
    Merge Sort divide el array en mitades, las ordena recursivamente,
    y luego las mezcla. Este generador muestra:
    - La división en subarreglos
    - El proceso de mezcla (merge) paso a paso
    
    Args:
        arr: Lista de números a ordenar
    
    Yields:
        tuple: (lista_actual, idx_inicio, idx_fin, idx_actual, operacion)
        - lista_actual: estado actual del arreglo
        - idx_inicio: inicio del subarreglo actual
        - idx_fin: fin del subarreglo actual  
        - idx_actual: índice actual en la mezcla
        - operacion: "dividing", "merging", "comparing", "placing", "finished"
    """
    lista = arr.copy()
    n = len(lista)
    
    # Usamos una pila para simular recursión: (inicio, fin, profundidad)
    pila = [(0, n - 1, 0)]
    
    # Almacenamos los resultados de merge para mostrarlos paso a paso
    resultados_merge = []
    
    while pila:
        inicio, fin, profundidad = pila.pop()
        
        if inicio >= fin:
            continue
        
        medio = (inicio + fin) // 2
        
        # Mostrar división
        yield lista, inicio, fin, medio, "dividing"
        
        # Agregar subproblemas a la pila (orden inverso para procesar izquierda primero)
        pila.append((medio + 1, fin, profundidad + 1))
        pila.append((inicio, medio, profundidad + 1))
    
    # Ahora hacemos el merge de abajo hacia arriba
    tamaño = 1
    while tamaño < n:
        for inicio in range(0, n - tamaño, 2 * tamaño):
            medio = inicio + tamaño - 1
            fin = min(inicio + 2 * tamaño - 1, n - 1)
            
            # Mostrar que vamos a mezclar estos dos subarreglos
            yield lista, inicio, fin, medio, "merging_start"
            
            # Hacer merge de lista[inicio:medio+1] y lista[medio+1:fin+1]
            izquierda = lista[inicio:medio + 1].copy()
            derecha = lista[medio + 1:fin + 1].copy()
            
            i = j = 0
            k = inicio
            
            # Proceso de mezcla paso a paso
            while i < len(izquierda) and j < len(derecha):
                # Comparar elementos
                yield lista, inicio + i, medio + 1 + j, k, "comparing"
                
                if izquierda[i] <= derecha[j]:
                    lista[k] = izquierda[i]
                    yield lista, k, -1, -1, "placing"
                    i += 1
                else:
                    lista[k] = derecha[j]
                    yield lista, k, -1, -1, "placing"
                    j += 1
                k += 1
            
            # Colocar los elementos restantes
            while i < len(izquierda):
                lista[k] = izquierda[i]
                yield lista, k, -1, -1, "placing"
                i += 1
                k += 1
            
            while j < len(derecha):
                lista[k] = derecha[j]
                yield lista, k, -1, -1, "placing"
                j += 1
                k += 1
            
            # Marcar este segmento como ordenado
            yield lista, inicio, fin, -1, "segment_sorted"
        
        tamaño *= 2
    
    # Estado final
    yield lista, -1, -1, -1, "finished"