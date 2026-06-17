"""
Counting Sort con generador para animación paso a paso.
Es un algoritmo de ordenamiento lineal (no comparativo) que cuenta frecuencias.
Funciona bien cuando el rango de valores es pequeño.
"""

def counting_sort_generator(arr):
    """
    Generador que produce el estado del array durante el ordenamiento Counting Sort.
    
    Counting Sort funciona así:
    1. Encuentra el valor mínimo y máximo
    2. Crea un arreglo de frecuencias
    3. Cuenta cuántas veces aparece cada valor
    4. Reconstruye el arreglo ordenado
    
    Args:
        arr: Lista de números a ordenar (se modifica in-place)
    
    Yields:
        tuple: (lista_actual, idx_actual, valor_actual, operacion, datos_extra)
        - lista_actual: estado actual del arreglo
        - idx_actual: índice actual en el arreglo original
        - valor_actual: valor que se está procesando
        - operacion: tipo de operación
        - datos_extra: información adicional (min, max, frecuencias, etc.)
    """
    lista = arr.copy()
    n = len(lista)
    
    if n == 0:
        yield lista, -1, -1, "finished", None
        return
    
    # Paso 1: Encontrar mínimo y máximo
    min_val = min(lista)
    max_val = max(lista)
    rango = max_val - min_val + 1
    
    yield lista, -1, -1, "finding_range", {"min": min_val, "max": max_val, "rango": rango}
    
    # Paso 2: Crear arreglo de frecuencias
    frecuencias = [0] * rango
    
    # Paso 3: Contar frecuencias
    yield lista, -1, -1, "creating_counts", {"frecuencias": frecuencias.copy()}
    
    for i, valor in enumerate(lista):
        idx_freq = valor - min_val
        frecuencias[idx_freq] += 1
        yield lista, i, valor, "counting", {
            "frecuencias": frecuencias.copy(),
            "min": min_val,
            "max": max_val
        }
    
    yield lista, -1, -1, "counts_complete", {"frecuencias": frecuencias.copy()}
    
    # Paso 4: Calcular frecuencias acumuladas (para ordenamiento estable)
    frecuencias_acum = frecuencias.copy()
    for i in range(1, rango):
        frecuencias_acum[i] += frecuencias_acum[i - 1]
    
    yield lista, -1, -1, "cumulative_counts", {"frecuencias_acum": frecuencias_acum.copy()}
    
    # Paso 5: Construir arreglo ordenado (versión estable, recorriendo de atrás a adelante)
    ordenado = [0] * n
    
    # Mostrar el proceso de construcción
    for i in range(n - 1, -1, -1):
        valor = lista[i]
        idx_freq = valor - min_val
        pos = frecuencias_acum[idx_freq] - 1
        ordenado[pos] = valor
        frecuencias_acum[idx_freq] -= 1
        
        yield lista, i, valor, "placing", {
            "ordenado": ordenado.copy(),
            "posicion_actual": pos,
            "min": min_val
        }
    
    # Paso 6: Copiar de vuelta a la lista original
    for i in range(n):
        lista[i] = ordenado[i]
        yield lista, i, ordenado[i], "copying", None
    
    # Estado final
    yield lista, -1, -1, "finished", None