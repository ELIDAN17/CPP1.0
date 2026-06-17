"""
Recorridos de árboles binarios.
"""

def recorrer_inorden(nodo):
    """Recorrido inorden (izquierdo - raíz - derecho)."""
    if nodo is None:
        return
    yield from recorrer_inorden(nodo.izquierdo)
    yield nodo
    yield from recorrer_inorden(nodo.derecho)

def recorrer_preorden(nodo):
    """Recorrido preorden (raíz - izquierdo - derecho)."""
    if nodo is None:
        return
    yield nodo
    yield from recorrer_preorden(nodo.izquierdo)
    yield from recorrer_preorden(nodo.derecho)

def recorrer_postorden(nodo):
    """Recorrido postorden (izquierdo - derecho - raíz)."""
    if nodo is None:
        return
    yield from recorrer_postorden(nodo.izquierdo)
    yield from recorrer_postorden(nodo.derecho)
    yield nodo