"""
Árbol Rojo-Negro con generador para animación.
Muestra colores (rojo/negro) y rebalanceo paso a paso.
"""

from .nodo import Nodo

class ArbolRojoNegro:
    """Árbol Rojo-Negro con operaciones básicas y colores visibles."""
    
    def __init__(self):
        self.raiz = None
    
    def insertar(self, valor):
        """Inserta un valor en el árbol Rojo-Negro con animación."""
        if self.raiz is None:
            self.raiz = Nodo(valor)
            self.raiz.color = "negro"
            yield self.raiz, "insertado_raiz", {
                "mensaje": f"✅ Raíz insertada: {valor} (color: negro)",
                "color": "negro"
            }
            return
        
        # Inserción normal
        actual = self.raiz
        camino = []
        
        while True:
            camino.append(actual)
            yield actual, "visitando", {
                "mensaje": f"🔍 Visitando nodo {actual.valor} (color: {actual.color})",
                "color": actual.color
            }
            
            if valor < actual.valor:
                if actual.izquierdo is None:
                    nuevo = Nodo(valor)
                    nuevo.padre = actual
                    actual.izquierdo = nuevo
                    yield nuevo, "insertado_rojo", {
                        "mensaje": f"✅ Insertado {nuevo.valor} (color: rojo)",
                        "color": "rojo"
                    }
                    # Rebalancear
                    yield from self._rebalancear(nuevo, camino)
                    return
                actual = actual.izquierdo
            elif valor > actual.valor:
                if actual.derecho is None:
                    nuevo = Nodo(valor)
                    nuevo.padre = actual
                    actual.derecho = nuevo
                    yield nuevo, "insertado_rojo", {
                        "mensaje": f"✅ Insertado {nuevo.valor} (color: rojo)",
                        "color": "rojo"
                    }
                    yield from self._rebalancear(nuevo, camino)
                    return
                actual = actual.derecho
            else:
                yield actual, "ya_existe", {
                    "mensaje": f"⚠️ El valor {valor} ya existe",
                    "color": actual.color
                }
                return
    
    def _rebalancear(self, nodo, camino):
        """Rebalancea el árbol después de una inserción."""
        while nodo.padre and nodo.padre.color == "rojo":
            tio = self._obtener_tio(nodo)
            abuelo = self._obtener_abuelo(nodo)
            
            # ---- Caso 1: Tío rojo (recolorear) ----
            if tio and tio.color == "rojo":
                nodo.padre.color = "negro"
                tio.color = "negro"
                if abuelo and abuelo != self.raiz:
                    abuelo.color = "rojo"
                
                yield nodo, "caso_tio_rojo", {
                    "mensaje": f"🎨 Caso 1: Tío rojo - Recoloreando {nodo.padre.valor} y {tio.valor} a negro, {abuelo.valor} a rojo",
                    "color": nodo.color
                }
                nodo = abuelo if abuelo else nodo
                if nodo:
                    yield nodo, "recoloreado", {
                        "mensaje": f"🎨 Nodo {nodo.valor} ahora es {nodo.color}",
                        "color": nodo.color
                    }
            
            # ---- Caso 2: Tío negro ----
            else:
                if not abuelo:
                    break
                
                # ---- Caso 2a: Rotación izquierda (nodo a la derecha del padre) ----
                if nodo == nodo.padre.derecho and nodo.padre == abuelo.izquierdo:
                    yield nodo, "rotacion_izquierda", {
                        "mensaje": f"🔄 Rotación izquierda en {nodo.padre.valor}",
                        "color": nodo.color
                    }
                    nodo = nodo.padre
                    self._rotar_izquierda(nodo)
                    yield nodo, "despues_rotacion", {
                        "mensaje": f"✅ Después de rotación izquierda en {nodo.valor}",
                        "color": nodo.color
                    }
                
                # ---- Caso 2b: Rotación derecha (nodo a la izquierda del padre) ----
                elif nodo == nodo.padre.izquierdo and nodo.padre == abuelo.derecho:
                    yield nodo, "rotacion_derecha", {
                        "mensaje": f"🔄 Rotación derecha en {nodo.padre.valor}",
                        "color": nodo.color
                    }
                    nodo = nodo.padre
                    self._rotar_derecha(nodo)
                    yield nodo, "despues_rotacion", {
                        "mensaje": f"✅ Después de rotación derecha en {nodo.valor}",
                        "color": nodo.color
                    }
                
                # ---- Caso 3: Recolorear y rotar ----
                nodo.padre.color = "negro"
                abuelo.color = "rojo"
                
                if nodo == nodo.padre.izquierdo:
                    yield nodo, "rotacion_derecha", {
                        "mensaje": f"🔄 Rotación derecha en {abuelo.valor}",
                        "color": nodo.color
                    }
                    self._rotar_derecha(abuelo)
                else:
                    yield nodo, "rotacion_izquierda", {
                        "mensaje": f"🔄 Rotación izquierda en {abuelo.valor}",
                        "color": nodo.color
                    }
                    self._rotar_izquierda(abuelo)
                
                yield abuelo, "despues_rotacion", {
                    "mensaje": f"✅ Árbol rebalanceado",
                    "color": abuelo.color if abuelo else "negro"
                }
                break
        
        # Asegurar que la raíz sea negra
        if self.raiz:
            self.raiz.color = "negro"
            yield self.raiz, "raiz_negra", {
                "mensaje": f"⚫ Raíz {self.raiz.valor} es negra",
                "color": "negro"
            }
    
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
        """Rotación izquierda (mantiene colores)."""
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
        """Rotación derecha (mantiene colores)."""
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
        """Busca un valor en el árbol con animación paso a paso."""
        if self.raiz is None:
            yield None, "vacio", {"mensaje": "🌳 El árbol está vacío"}
            return
        
        actual = self.raiz
        while actual:
            yield actual, "visitando", {
                "mensaje": f"🔍 Visitando nodo {actual.valor} (color: {actual.color})",
                "color": actual.color
            }
            
            if valor == actual.valor:
                yield actual, "encontrado", {
                    "mensaje": f"✅ Encontrado: {actual.valor} (color: {actual.color})",
                    "color": actual.color
                }
                return
            elif valor < actual.valor:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        
        yield None, "no_encontrado", {"mensaje": f"❌ {valor} no encontrado en el árbol"}
    
    def eliminar(self, valor):
        """Elimina un valor del árbol (versión simplificada)."""
        if self.raiz is None:
            yield None, "vacio", {"mensaje": "🌳 El árbol está vacío"}
            return
        
        # Verificar si existe
        encontrado = False
        for estado in self.buscar(valor):
            if len(estado) >= 2 and estado[1] == "encontrado":
                encontrado = True
                break
        
        if not encontrado:
            yield None, "no_encontrado", {"mensaje": f"❌ {valor} no encontrado"}
            return
        
        # Reconstruir árbol sin el nodo
        valores = []
        for nodo, _, _ in self.in_order():
            if nodo.valor != valor:
                valores.append(nodo.valor)
        
        self.raiz = None
        yield None, "eliminando", {"mensaje": f"🗑️ Eliminando nodo {valor}"}
        
        for v in valores:
            for _ in self.insertar(v):
                pass
        
        yield None, "eliminado", {"mensaje": f"✅ Nodo {valor} eliminado"}

    # ========== RECORRIDOS ==========
    def in_order(self):
        yield from self._in_order(self.raiz)
    
    def _in_order(self, nodo):
        if nodo is None:
            return
        yield from self._in_order(nodo.izquierdo)
        yield nodo, "inorden", {
            "mensaje": f"📌 Inorden: {nodo.valor} (color: {nodo.color})",
            "color": nodo.color
        }
        yield from self._in_order(nodo.derecho)
    
    def pre_order(self):
        yield from self._pre_order(self.raiz)
    
    def _pre_order(self, nodo):
        if nodo is None:
            return
        yield nodo, "preorden", {
            "mensaje": f"📌 Preorden: {nodo.valor} (color: {nodo.color})",
            "color": nodo.color
        }
        yield from self._pre_order(nodo.izquierdo)
        yield from self._pre_order(nodo.derecho)
    
    def post_order(self):
        yield from self._post_order(self.raiz)
    
    def _post_order(self, nodo):
        if nodo is None:
            return
        yield from self._post_order(nodo.izquierdo)
        yield from self._post_order(nodo.derecho)
        yield nodo, "postorden", {
            "mensaje": f"📌 Postorden: {nodo.valor} (color: {nodo.color})",
            "color": nodo.color
        }
    
    def bfs(self):
        from collections import deque
        if self.raiz is None:
            return
        
        cola = deque([(self.raiz, 0)])
        while cola:
            nodo, nivel = cola.popleft()
            yield nodo, "bfs", {
                "mensaje": f"📌 BFS nivel {nivel}: {nodo.valor} (color: {nodo.color})",
                "nivel": nivel,
                "color": nodo.color
            }
            if nodo.izquierdo:
                cola.append((nodo.izquierdo, nivel + 1))
            if nodo.derecho:
                cola.append((nodo.derecho, nivel + 1))
    
    # ========== ESTADÍSTICAS ==========
    def altura(self):
        return self._altura(self.raiz)
    
    def _altura(self, nodo):
        if nodo is None:
            return -1
        return 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))
    
    def tamaño(self):
        return self._tamaño(self.raiz)
    
    def _tamaño(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._tamaño(nodo.izquierdo) + self._tamaño(nodo.derecho)