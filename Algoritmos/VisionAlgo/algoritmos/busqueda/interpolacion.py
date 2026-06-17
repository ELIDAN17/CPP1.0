"""
Búsqueda por Interpolación con generador para animación paso a paso.
Requiere lista ordenada con distribución uniforme.
"""

def busqueda_interpolacion_generator(lista, objetivo):
    """
    Generador que busca un elemento usando interpolación paso a paso.
    
    Yields:
        tuple: (lista, izquierda, derecha, pos, operacion)
    """
    izquierda = 0
    derecha = len(lista) - 1
    
    while izquierda <= derecha:
        # Fórmula de interpolación
        if lista[derecha] == lista[izquierda]:
            pos = izquierda
        else:
            pos = izquierda + int((objetivo - lista[izquierda]) * (derecha - izquierda) / (lista[derecha] - lista[izquierda]))
        
        if pos < izquierda or pos > derecha:
            yield lista, izquierda, derecha, pos, "fuera_rango"
            break
        
        yield lista, izquierda, derecha, pos, "buscando"
        
        if lista[pos] == objetivo:
            yield lista, izquierda, derecha, pos, "encontrado"
            return
        elif lista[pos] < objetivo:
            izquierda = pos + 1
        else:
            derecha = pos - 1
        
        yield lista, izquierda, derecha, pos, "actualizando"
    
    yield lista, -1, -1, -1, "no_encontrado"