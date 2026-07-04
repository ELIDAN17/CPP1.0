"""
Árbol AVL (Balanceado) con generador para animación.
Muestra rotaciones paso a paso usando recursión.
"""

from .nodo import Nodo

class ArbolAVL:
    """Árbol AVL con balanceo automático y rotaciones visibles."""
    
    def __init__(self):
        self.raiz = None
    
    def _altura(self, nodo):
        if nodo is None:
            return 0
        return nodo.altura
    
    def _factor_balance(self, nodo):
        if nodo is None:
            return 0
        return self._altura(nodo.izquierdo) - self._altura(nodo.derecho)
    
    def _actualizar_altura(self, nodo):
        if nodo:
            nodo.altura = 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))
    
    def _rotacion_derecha(self, y):
        """Rotación simple a la derecha."""
        x = y.izquierdo
        T2 = x.derecho
        
        # Realizar rotación
        x.derecho = y
        y.izquierdo = T2
        
        # Actualizar alturas
        self._actualizar_altura(y)
        self._actualizar_altura(x)
        
        return x
    
    def _rotacion_izquierda(self, x):
        """Rotación simple a la izquierda."""
        y = x.derecho
        T2 = y.izquierdo
        
        # Realizar rotación
        y.izquierdo = x
        x.derecho = T2
        
        # Actualizar alturas
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        
        return y
    
    def insertar(self, valor):
        """
        Inserta un valor en el árbol AVL.
        Generador que produce (nodo, operacion, info) para animación.
        Usa recursión para balancear correctamente.
        """
        if self.raiz is None:
            self.raiz = Nodo(valor)
            yield self.raiz, "insertado_raiz", {"mensaje": f"✅ Raíz insertada: {valor}"}
            return
        
        # Llamar a la función recursiva
        self.raiz, pasos = self._insertar_recursivo(self.raiz, valor)
        
        # Emitir los pasos acumulados
        for paso in pasos:
            yield paso
    
    def _insertar_recursivo(self, nodo, valor):
        """
        Inserción recursiva con acumulación de pasos.
        Retorna (nuevo_nodo, lista_de_pasos)
        """
        pasos = []
        
        if nodo is None:
            nuevo = Nodo(valor)
            pasos.append((nuevo, "insertado", {"mensaje": f"✅ Nodo {valor} creado"}))
            return nuevo, pasos
        
        # Mostrar visita
        pasos.append((nodo, "visitando", {
            "mensaje": f"🔍 Visitando nodo {nodo.valor} (balance={self._factor_balance(nodo):.0f})"
        }))
        
        if valor < nodo.valor:
            nodo.izquierdo, sub_pasos = self._insertar_recursivo(nodo.izquierdo, valor)
            pasos.extend(sub_pasos)
        elif valor > nodo.valor:
            nodo.derecho, sub_pasos = self._insertar_recursivo(nodo.derecho, valor)
            pasos.extend(sub_pasos)
        else:
            pasos.append((nodo, "ya_existe", {"mensaje": f"⚠️ El valor {valor} ya existe"}))
            return nodo, pasos
        
        # ===== BALANCEO =====
        # Actualizar altura del nodo actual
        self._actualizar_altura(nodo)
        balance = self._factor_balance(nodo)
        
        # Mostrar información de balance
        pasos.append((nodo, "verificando_balance", {
            "mensaje": f"⚖️ Nodo {nodo.valor}: altura_izq={self._altura(nodo.izquierdo)}, "
                       f"altura_der={self._altura(nodo.derecho)}, factor={balance:.0f}"
        }))
        
        # ---- CASO 1: Izquierda-Izquierda (Rotación Derecha) ----
        if balance > 1 and self._factor_balance(nodo.izquierdo) >= 0:
            pasos.append((nodo.izquierdo, "rotacion_derecha", {
                "mensaje": f"🔄 Rotación derecha en {nodo.valor} (balance={balance:.0f})"
            }))
            pasos.append((nodo, "antes_rotacion", {
                "mensaje": f"📐 Antes: {nodo.valor} ← {nodo.izquierdo.valor}"
            }))
            
            nodo = self._rotacion_derecha(nodo)
            
            pasos.append((nodo, "despues_rotacion", {
                "mensaje": f"✅ Después de rotación derecha: raíz {nodo.valor}"
            }))
        
        # ---- CASO 2: Izquierda-Derecha (Rotación Doble) ----
        elif balance > 1 and self._factor_balance(nodo.izquierdo) < 0:
            pasos.append((nodo.izquierdo.derecho, "rotacion_izquierda", {
                "mensaje": f"🔄 Rotación izquierda en {nodo.izquierdo.valor} (doble)"
            }))
            nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)
            
            pasos.append((nodo, "rotacion_derecha", {
                "mensaje": f"🔄 Rotación derecha en {nodo.valor} (doble)"
            }))
            nodo = self._rotacion_derecha(nodo)
            
            pasos.append((nodo, "despues_rotacion", {
                "mensaje": f"✅ Después de doble rotación: raíz {nodo.valor}"
            }))
        
        # ---- CASO 3: Derecha-Derecha (Rotación Izquierda) ----
        elif balance < -1 and self._factor_balance(nodo.derecho) <= 0:
            pasos.append((nodo.derecho, "rotacion_izquierda", {
                "mensaje": f"🔄 Rotación izquierda en {nodo.valor} (balance={balance:.0f})"
            }))
            pasos.append((nodo, "antes_rotacion", {
                "mensaje": f"📐 Antes: {nodo.valor} → {nodo.derecho.valor}"
            }))
            
            nodo = self._rotacion_izquierda(nodo)
            
            pasos.append((nodo, "despues_rotacion", {
                "mensaje": f"✅ Después de rotación izquierda: raíz {nodo.valor}"
            }))
        
        # ---- CASO 4: Derecha-Izquierda (Rotación Doble) ----
        elif balance < -1 and self._factor_balance(nodo.derecho) > 0:
            pasos.append((nodo.derecho.izquierdo, "rotacion_derecha", {
                "mensaje": f"🔄 Rotación derecha en {nodo.derecho.valor} (doble)"
            }))
            nodo.derecho = self._rotacion_derecha(nodo.derecho)
            
            pasos.append((nodo, "rotacion_izquierda", {
                "mensaje": f"🔄 Rotación izquierda en {nodo.valor} (doble)"
            }))
            nodo = self._rotacion_izquierda(nodo)
            
            pasos.append((nodo, "despues_rotacion", {
                "mensaje": f"✅ Después de doble rotación: raíz {nodo.valor}"
            }))
        
        # ---- Si no hay rotación ----
        else:
            pasos.append((nodo, "balanceado", {
                "mensaje": f"⚖️ Nodo {nodo.valor} ya está balanceado (factor={balance:.0f})"
            }))
        
        return nodo, pasos

    def buscar(self, valor):
        """Busca un valor en el árbol."""
        if self.raiz is None:
            yield None, "vacio", {"mensaje": "El árbol está vacío"}
            return
        
        actual = self.raiz
        while actual:
            yield actual, "visitando", {"mensaje": f"🔍 Visitando nodo {actual.valor}"}
            
            if valor == actual.valor:
                yield actual, "encontrado", {
                    "mensaje": f"✅ Encontrado: {actual.valor}",
                    "altura": actual.altura
                }
                return
            elif valor < actual.valor:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        
        yield None, "no_encontrado", {"mensaje": f"❌ {valor} no encontrado"}
    
    def eliminar(self, valor):
        """Elimina un valor del árbol."""
        if self.raiz is None:
            yield None, "vacio", {"mensaje": "El árbol está vacío"}
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
        yield nodo, "inorden", {"mensaje": f"📌 Inorden: {nodo.valor}"}
        yield from self._in_order(nodo.derecho)
    
    def pre_order(self):
        yield from self._pre_order(self.raiz)
    
    def _pre_order(self, nodo):
        if nodo is None:
            return
        yield nodo, "preorden", {"mensaje": f"📌 Preorden: {nodo.valor}"}
        yield from self._pre_order(nodo.izquierdo)
        yield from self._pre_order(nodo.derecho)
    
    def post_order(self):
        yield from self._post_order(self.raiz)
    
    def _post_order(self, nodo):
        if nodo is None:
            return
        yield from self._post_order(nodo.izquierdo)
        yield from self._post_order(nodo.derecho)
        yield nodo, "postorden", {"mensaje": f"📌 Postorden: {nodo.valor}"}
    
    def bfs(self):
        from collections import deque
        if self.raiz is None:
            return
        
        cola = deque([(self.raiz, 0)])
        while cola:
            nodo, nivel = cola.popleft()
            yield nodo, "bfs", {
                "mensaje": f"📌 BFS nivel {nivel}: {nodo.valor}",
                "nivel": nivel
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