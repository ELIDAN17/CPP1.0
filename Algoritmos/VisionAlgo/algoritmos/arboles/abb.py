"""
Árbol Binario de Búsqueda (ABB) con generador para animación.
"""

from .nodo import Nodo

class ArbolABB:
    """Árbol Binario de Búsqueda con operaciones básicas."""
    
    def __init__(self):
        self.raiz = None
    
    def insertar(self, valor):
        """Inserta un valor en el árbol."""
        if self.raiz is None:
            self.raiz = Nodo(valor)
            yield self.raiz, "insertado_raiz"
            return
        
        actual = self.raiz
        while True:
            yield actual, "visitando"
            
            if valor < actual.valor:
                if actual.izquierdo is None:
                    actual.izquierdo = Nodo(valor)
                    yield actual.izquierdo, "insertado_izquierdo"
                    return
                actual = actual.izquierdo
            elif valor > actual.valor:
                if actual.derecho is None:
                    actual.derecho = Nodo(valor)
                    yield actual.derecho, "insertado_derecho"
                    return
                actual = actual.derecho
            else:
                yield actual, "ya_existe"
                return
    
    def buscar(self, valor):
        """Busca un valor en el árbol."""
        if self.raiz is None:
            yield None, "vacio"
            return
        
        actual = self.raiz
        while actual:
            yield actual, "visitando"
            
            if valor == actual.valor:
                yield actual, "encontrado"
                return
            elif valor < actual.valor:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        
        yield None, "no_encontrado"
    
    def eliminar(self, valor):
        """Elimina un valor del árbol."""
        yield from self._eliminar(self.raiz, valor)
    
    def _eliminar(self, nodo, valor):
        if nodo is None:
            yield None, "no_encontrado"
            return
        
        yield nodo, "visitando"
        
        if valor < nodo.valor:
            yield from self._eliminar(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            yield from self._eliminar(nodo.derecho, valor)
        else:
            # Nodo encontrado
            yield nodo, "eliminando"
            
            # Caso 1: sin hijos
            if nodo.izquierdo is None and nodo.derecho is None:
                if nodo == self.raiz:
                    self.raiz = None
                else:
                    # Buscar padre para eliminar referencia
                    yield nodo, "eliminado_sin_hijos"
            
            # Caso 2: un hijo
            elif nodo.izquierdo is None:
                yield nodo.derecho, "reemplazando"
                if nodo == self.raiz:
                    self.raiz = nodo.derecho
                else:
                    yield nodo, "eliminado_un_hijo"
            elif nodo.derecho is None:
                yield nodo.izquierdo, "reemplazando"
                if nodo == self.raiz:
                    self.raiz = nodo.izquierdo
                else:
                    yield nodo, "eliminado_un_hijo"
            
            # Caso 3: dos hijos
            else:
                # Encontrar sucesor (mínimo del subárbol derecho)
                sucesor = nodo.derecho
                while sucesor.izquierdo:
                    yield sucesor, "buscando_sucesor"
                    sucesor = sucesor.izquierdo
                
                yield sucesor, "sucesor_encontrado"
                nodo.valor = sucesor.valor
                yield nodo, "reemplazado_por_sucesor"
                
                # Eliminar el sucesor
                yield from self._eliminar(nodo.derecho, sucesor.valor)