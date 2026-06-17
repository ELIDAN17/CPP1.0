"""
Árbol Rojo-Negro con generador para animación.
"""

from .nodo import Nodo

class ArbolRojoNegro:
    """Árbol Rojo-Negro con operaciones básicas."""
    
    def __init__(self):
        self.raiz = None
    
    def insertar(self, valor):
        """Inserta un valor en el árbol Rojo-Negro."""
        if self.raiz is None:
            self.raiz = Nodo(valor)
            self.raiz.color = "negro"
            yield self.raiz, "insertado_raiz"
            return
        
        # Inserción normal
        actual = self.raiz
        while True:
            yield actual, "visitando"
            
            if valor < actual.valor:
                if actual.izquierdo is None:
                    nuevo = Nodo(valor)
                    nuevo.padre = actual
                    actual.izquierdo = nuevo
                    yield nuevo, "insertado_rojo"
                    # Rebalancear
                    yield from self._rebalancear(nuevo)
                    return
                actual = actual.izquierdo
            elif valor > actual.valor:
                if actual.derecho is None:
                    nuevo = Nodo(valor)
                    nuevo.padre = actual
                    actual.derecho = nuevo
                    yield nuevo, "insertado_rojo"
                    yield from self._rebalancear(nuevo)
                    return
                actual = actual.derecho
            else:
                yield actual, "ya_existe"
                return
    
    def _rebalancear(self, nodo):
        """Rebalancea el árbol después de una inserción."""
        while nodo.padre and nodo.padre.color == "rojo":
            tio = self._obtener_tio(nodo)
            
            # Caso 1: Tío rojo
            if tio and tio.color == "rojo":
                nodo.padre.color = "negro"
                tio.color = "negro"
                abuelo = self._obtener_abuelo(nodo)
                if abuelo and abuelo != self.raiz:
                    abuelo.color = "rojo"
                yield nodo, "caso_tio_rojo"
                nodo = abuelo if abuelo else nodo
            
            # Caso 2: Tío negro
            else:
                abuelo = self._obtener_abuelo(nodo)
                if not abuelo:
                    break
                
                # Caso 2a: nodo está a la derecha del padre y padre a la izquierda
                if nodo == nodo.padre.derecho and nodo.padre == abuelo.izquierdo:
                    yield nodo, "rotacion_izquierda"
                    nodo = nodo.padre
                    nodo = self._rotar_izquierda(nodo)
                
                # Caso 2b: nodo está a la izquierda del padre y padre a la derecha
                elif nodo == nodo.padre.izquierdo and nodo.padre == abuelo.derecho:
                    yield nodo, "rotacion_derecha"
                    nodo = nodo.padre
                    nodo = self._rotar_derecha(nodo)
                
                # Caso 3: Padre rojo, tío negro
                nodo.padre.color = "negro"
                abuelo.color = "rojo"
                
                if nodo == nodo.padre.izquierdo:
                    yield nodo, "rotacion_derecha"
                    self._rotar_derecha(abuelo)
                else:
                    yield nodo, "rotacion_izquierda"
                    self._rotar_izquierda(abuelo)
                
                break
        
        if self.raiz:
            self.raiz.color = "negro"
            yield self.raiz, "raiz_negra"
    
    def _obtener_abuelo(self, nodo):
        return nodo.padre.padre if nodo and nodo.padre else None
    
    def _obtener_tio(self, nodo):
        abuelo = self._obtener_abuelo(nodo)
        if abuelo is None:
            return None
        if nodo.padre == abuelo.izquierdo:
            return abuelo.derecho
        return abuelo.izquierdo
    
    def _rotar_izquierda(self, x):
        y = x.derecho
        x.derecho = y.izquierdo
        if y.izquierdo:
            y.izquierdo.padre = x
        y.padre = x.padre
        if x.padre is None:
            self.raiz = y
        elif x == x.padre.izquierdo:
            x.padre.izquierdo = y
        else:
            x.padre.derecho = y
        y.izquierdo = x
        x.padre = y
        return y
    
    def _rotar_derecha(self, x):
        y = x.izquierdo
        x.izquierdo = y.derecho
        if y.derecho:
            y.derecho.padre = x
        y.padre = x.padre
        if x.padre is None:
            self.raiz = y
        elif x == x.padre.derecho:
            x.padre.derecho = y
        else:
            x.padre.izquierdo = y
        y.derecho = x
        x.padre = y
        return y
    
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