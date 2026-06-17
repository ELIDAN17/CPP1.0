"""
Búsqueda Binaria con generador para animación paso a paso.
Requiere lista ordenada.
"""

def busqueda_binaria_generator(lista, objetivo):
    """
    Generador que busca un elemento usando búsqueda binaria paso a paso.
    
    Yields:
        tuple: (lista, izquierda, derecha, medio, operacion)
        - lista: estado actual
        - izquierda: límite izquierdo
        - derecha: límite derecho
        - medio: índice medio
        - operacion: "buscando", "encontrado", "no_encontrado"
    """
    izquierda = 0
    derecha = len(lista) - 1
    
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        yield lista, izquierda, derecha, medio, "buscando"
        
        if lista[medio] == objetivo:
            yield lista, izquierda, derecha, medio, "encontrado"
            return
        elif lista[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
        
        yield lista, izquierda, derecha, medio, "actualizando"
    
    yield lista, -1, -1, -1, "no_encontrado"