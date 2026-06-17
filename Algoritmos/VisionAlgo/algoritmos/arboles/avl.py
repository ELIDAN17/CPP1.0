"""
Árbol AVL (Balanceado) con generador para animación.
"""

from .nodo import Nodo

class ArbolAVL:
    """Árbol AVL con balanceo automático."""
    
    def __init__(self):
        self.raiz = None
    
    def altura(self, nodo):
        if nodo is None:
            return 0
        return nodo.altura
    
    def factor_balance(self, nodo):
        if nodo is None:
            return 0
        return self.altura(nodo.izquierdo) - self.altura(nodo.derecho)
    
    def actualizar_altura(self, nodo):
        if nodo:
            nodo.altura = 1 + max(self.altura(nodo.izquierdo), self.altura(nodo.derecho))
    
    def rotacion_derecha(self, y):
        x = y.izquierdo
        T2 = x.derecho
        
        # Rotación
        x.derecho = y
        y.izquierdo = T2
        
        # Actualizar alturas
        self.actualizar_altura(y)
        self.actualizar_altura(x)
        
        return x
    
    def rotacion_izquierda(self, x):
        y = x.derecho
        T2 = y.izquierdo
        
        # Rotación
        y.izquierdo = x
        x.derecho = T2
        
        # Actualizar alturas
        self.actualizar_altura(x)
        self.actualizar_altura(y)
        
        return y
    
    def insertar(self, valor):
        """Inserta un valor y balancea el árbol."""
        if self.raiz is None:
            self.raiz = Nodo(valor)
            yield self.raiz, "insertado_raiz"
            return
        
        # Usamos una pila para simular recursión
        pila = [(self.raiz, None, None)]  # (nodo, padre, direccion)
        
        while pila:
            actual, padre, direccion = pila.pop()
            
            yield actual, "visitando"
            
            if valor < actual.valor:
                if actual.izquierdo is None:
                    nuevo = Nodo(valor)
                    actual.izquierdo = nuevo
                    yield nuevo, "insertado_izquierdo"
                    # Balancear después de insertar
                    yield from self._balancear(actual)
                    return
                else:
                    pila.append((actual.izquierdo, actual, "izquierdo"))
            elif valor > actual.valor:
                if actual.derecho is None:
                    nuevo = Nodo(valor)
                    actual.derecho = nuevo
                    yield nuevo, "insertado_derecho"
                    yield from self._balancear(actual)
                    return
                else:
                    pila.append((actual.derecho, actual, "derecho"))
            else:
                yield actual, "ya_existe"
                return
    
    def _balancear(self, nodo):
        """Balancea el árbol después de una inserción."""
        if nodo is None:
            return
        
        self.actualizar_altura(nodo)
        balance = self.factor_balance(nodo)
        
        # Caso izquierda-izquierda
        if balance > 1 and self.factor_balance(nodo.izquierdo) >= 0:
            yield nodo, "rotacion_derecha"
            nodo = self.rotacion_derecha(nodo)
            yield nodo, "balanceado"
        
        # Caso izquierda-derecha
        elif balance > 1 and self.factor_balance(nodo.izquierdo) < 0:
            yield nodo.izquierdo, "rotacion_izquierda"
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
            yield nodo, "rotacion_derecha"
            nodo = self.rotacion_derecha(nodo)
            yield nodo, "balanceado"
        
        # Caso derecha-derecha
        elif balance < -1 and self.factor_balance(nodo.derecho) <= 0:
            yield nodo, "rotacion_izquierda"
            nodo = self.rotacion_izquierda(nodo)
            yield nodo, "balanceado"
        
        # Caso derecha-izquierda
        elif balance < -1 and self.factor_balance(nodo.derecho) > 0:
            yield nodo.derecho, "rotacion_derecha"
            nodo.derecho = self.rotacion_derecha(nodo.derecho)
            yield nodo, "rotacion_izquierda"
            nodo = self.rotacion_izquierda(nodo)
            yield nodo, "balanceado"
    
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