"""
Búsqueda Exponencial con generador para animación paso a paso.
Requiere lista ordenada.
"""

def busqueda_exponencial_generator(lista, objetivo):
    """
    Generador que busca un elemento usando búsqueda exponencial + binaria.
    
    Yields:
        tuple: (lista, idx_actual, rango_inicio, rango_fin, operacion)
        - lista: estado actual de la lista
        - idx_actual: índice actual que se está revisando
        - rango_inicio: inicio del rango actual
        - rango_fin: fin del rango actual
        - operacion: "buscando", "encontrado", "no_encontrado", "rango_encontrado"
    """
    n = len(lista)
    
    # Si la lista está vacía
    if n == 0:
        yield lista, -1, -1, -1, "no_encontrado"
        return
    
    # Verificar el primer elemento
    if lista[0] == objetivo:
        yield lista, 0, 0, 0, "encontrado"
        return
    
    # Buscar rango exponencialmente
    i = 1
    while i < n and lista[i] <= objetivo:
        yield lista, i, 0, i, "expandiendo"
        i *= 2
    
    # Determinar rango para búsqueda binaria
    rango_inicio = i // 2
    rango_fin = min(i, n - 1)
    
    # Mostrar el rango encontrado
    yield lista, -1, rango_inicio, rango_fin, "rango_encontrado"
    
    # Si el rango es inválido o el objetivo está fuera
    if rango_inicio > rango_fin or objetivo < lista[rango_inicio] or objetivo > lista[rango_fin]:
        yield lista, -1, rango_inicio, rango_fin, "no_encontrado"
        return
    
    # Búsqueda binaria en el rango
    izquierda = rango_inicio
    derecha = rango_fin
    
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        yield lista, medio, izquierda, derecha, "buscando"
        
        if lista[medio] == objetivo:
            yield lista, medio, izquierda, derecha, "encontrado"
            return
        elif lista[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
        
        # Mostrar que estamos actualizando el rango
        yield lista, medio, izquierda, derecha, "actualizando"
    
    # No encontrado
    yield lista, -1, -1, -1, "no_encontrado"