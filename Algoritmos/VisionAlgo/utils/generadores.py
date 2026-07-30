"""
Generadores de datos de prueba para los algoritmos.
"""

import random

def lista_aleatoria(n, min_val=10, max_val=200):
    """Genera lista de n enteros aleatorios entre min_val y max_val."""
    return [random.randint(min_val, max_val) for _ in range(n)]

def lista_ordenada(n, min_val=10, max_val=200):
    """Genera lista de n enteros en orden creciente con valores grandes."""
    step = (max_val - min_val) / max(1, n - 1)
    return [int(min_val + i * step) for i in range(n)]

def lista_inversa(n, min_val=10, max_val=200):
    """Genera lista de n enteros en orden decreciente con valores grandes."""
    step = (max_val - min_val) / max(1, n - 1)
    return [int(max_val - i * step) for i in range(n)]

def lista_casi_ordenada(n, swaps=3, min_val=10, max_val=200):
    """Genera lista casi ordenada con 'swaps' intercambios aleatorios."""
    arr = lista_ordenada(n, min_val, max_val)
    for _ in range(swaps):
        i, j = random.sample(range(n), 2)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def lista_con_duplicados(n, min_val=10, max_val=100):
    """Genera lista con muchos valores repetidos (útil para Counting/Radix Sort)."""
    return [random.randint(min_val, max_val) for _ in range(n)]

def lista_uniforme(n, min_val=10, max_val=200):
    """Genera lista con distribución uniforme (buena para Bucket Sort)."""
    return lista_aleatoria(n, min_val, max_val)