"""
Búsqueda Lineal con generador para animación paso a paso.
"""

def busqueda_lineal_generator(lista, objetivo):
    """
    Generador que busca un elemento en la lista paso a paso.
    
    Yields:
        tuple: (lista, idx_actual, idx_encontrado, operacion)
        - lista: estado actual de la lista
        - idx_actual: índice que se está revisando
        - idx_encontrado: índice donde se encontró (-1 si no)
        - operacion: "buscando", "encontrado", "no_encontrado"
    """
    n = len(lista)
    
    for i, valor in enumerate(lista):
        # Mostrar que estamos revisando este elemento
        yield lista, i, -1, "buscando"
        
        if valor == objetivo:
            # Encontrado - mostrar con verde
            yield lista, i, i, "encontrado"
            return
    
    # No encontrado - mostrar mensaje
    yield lista, -1, -1, "no_encontrado"