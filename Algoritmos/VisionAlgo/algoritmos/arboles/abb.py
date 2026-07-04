"""
Árbol Binario de Búsqueda (ABB) con generador para animación y explicaciones.
Incluye: inserción, búsqueda, eliminación (3 casos) y 4 recorridos.
"""

from .nodo import Nodo
from collections import deque

class ArbolABB:
    """Árbol Binario de Búsqueda con operaciones completas."""
    
    def __init__(self):
        self.raiz = None
        self._pasos = []  # Para almacenar pasos de operaciones
    
    # ==================== INSERTAR ====================
    def insertar(self, valor):
        """
        Inserta un valor en el árbol.
        Generador que produce (nodo, operacion, info_extra) para animación.
        """
        if self.raiz is None:
            self.raiz = Nodo(valor)
            yield self.raiz, "insertado_raiz", {"mensaje": f"Raíz insertada: {valor}"}
            return
        
        actual = self.raiz
        while True:
            yield actual, "visitando", {"mensaje": f"Visitando nodo {actual.valor}"}
            
            if valor < actual.valor:
                if actual.izquierdo is None:
                    actual.izquierdo = Nodo(valor)
                    yield actual.izquierdo, "insertado_izquierdo", {
                        "mensaje": f"Insertado {valor} a la izquierda de {actual.valor}"
                    }
                    return
                actual = actual.izquierdo
            elif valor > actual.valor:
                if actual.derecho is None:
                    actual.derecho = Nodo(valor)
                    yield actual.derecho, "insertado_derecho", {
                        "mensaje": f"Insertado {valor} a la derecha de {actual.valor}"
                    }
                    return
                actual = actual.derecho
            else:
                yield actual, "ya_existe", {"mensaje": f"El valor {valor} ya existe en el árbol"}
                return
    
    # ==================== BUSCAR ====================
    def buscar(self, valor):
        """
        Busca un valor en el árbol.
        Generador que produce (nodo, operacion, info_extra) para animación.
        """
        if self.raiz is None:
            yield None, "vacio", {"mensaje": "El árbol está vacío"}
            return
        
        actual = self.raiz
        while actual:
            yield actual, "visitando", {"mensaje": f"Visitando nodo {actual.valor}"}
            
            if valor == actual.valor:
                yield actual, "encontrado", {
                    "mensaje": f"✅ Encontrado: {actual.valor}",
                    "nivel": self._nivel(actual)
                }
                return
            elif valor < actual.valor:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        
        yield None, "no_encontrado", {"mensaje": f"❌ {valor} no encontrado en el árbol"}
    
    # ==================== ELIMINAR ====================
    def eliminar(self, valor):
        """
        Elimina un valor del árbol (3 casos).
        Generador que produce (nodo, operacion, info_extra) para animación.
        """
        if self.raiz is None:
            yield None, "vacio", {"mensaje": "El árbol está vacío"}
            return
        
        if self.buscar(valor) is None:
            yield None, "no_encontrado", {"mensaje": f"❌ {valor} no encontrado para eliminar"}
            return
        
        self.raiz = yield from self._eliminar(self.raiz, valor)
    
    def _eliminar(self, nodo, valor):
        """Eliminación recursiva con los 3 casos."""
        if nodo is None:
            yield None, "no_encontrado", {"mensaje": "Nodo no encontrado"}
            return None
        
        yield nodo, "visitando", {"mensaje": f"Visitando nodo {nodo.valor}"}
        
        if valor < nodo.valor:
            nodo.izquierdo = yield from self._eliminar(nodo.izquierdo, valor)
            return nodo
        elif valor > nodo.valor:
            nodo.derecho = yield from self._eliminar(nodo.derecho, valor)
            return nodo
        
        # ===== NODO ENCONTRADO =====
        yield nodo, "eliminando", {"mensaje": f"🗑️ Eliminando nodo {nodo.valor}"}
        
        # --- Caso 1: Nodo hoja (sin hijos) ---
        if nodo.es_hoja():
            yield nodo, "eliminado_sin_hijos", {
                "mensaje": f"✅ Eliminado {nodo.valor} (nodo hoja)"
            }
            return None
        
        # --- Caso 2: Nodo con un hijo ---
        if nodo.tiene_un_hijo():
            hijo = nodo.izquierdo if nodo.izquierdo else nodo.derecho
            yield hijo, "reemplazando", {
                "mensaje": f"🔄 Reemplazando {nodo.valor} por su hijo {hijo.valor}"
            }
            return hijo
        
        # --- Caso 3: Nodo con dos hijos ---
        # Buscar sucesor in-order (mínimo del subárbol derecho)
        sucesor = self._minimo(nodo.derecho)
        yield sucesor, "sucesor_encontrado", {
            "mensaje": f"🎯 Sucesor encontrado: {sucesor.valor}"
        }
        
        # Copiar los datos del sucesor al nodo actual
        nodo.valor = sucesor.valor
        yield nodo, "reemplazado_por_sucesor", {
            "mensaje": f"🔄 Reemplazado {nodo.valor} por sucesor {sucesor.valor}"
        }
        
        # Eliminar el sucesor (que ahora está duplicado)
        nodo.derecho = yield from self._eliminar(nodo.derecho, sucesor.valor)
        
        return nodo
    
    def _minimo(self, nodo):
        """Encuentra el nodo mínimo (más a la izquierda)."""
        while nodo.izquierdo:
            nodo = nodo.izquierdo
        return nodo
    
    def _nivel(self, nodo):
        """Calcula el nivel de un nodo en el árbol."""
        if nodo is None:
            return -1
        nivel = 0
        actual = self.raiz
        while actual and actual != nodo:
            if nodo.valor < actual.valor:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
            nivel += 1
        return nivel if actual else -1
    
    # ==================== RECORRIDOS ====================
    def in_order(self):
        """
        Recorrido in-order (izquierda → raíz → derecha).
        Generador que produce (nodo, operacion, info_extra).
        """
        yield from self._in_order(self.raiz)
    
    def _in_order(self, nodo):
        if nodo is None:
            return
        yield from self._in_order(nodo.izquierdo)
        yield nodo, "inorden", {"mensaje": f"📌 Inorden: {nodo.valor}"}
        yield from self._in_order(nodo.derecho)
    
    def pre_order(self):
        """
        Recorrido pre-order (raíz → izquierda → derecha).
        Generador que produce (nodo, operacion, info_extra).
        """
        yield from self._pre_order(self.raiz)
    
    def _pre_order(self, nodo):
        if nodo is None:
            return
        yield nodo, "preorden", {"mensaje": f"📌 Preorden: {nodo.valor}"}
        yield from self._pre_order(nodo.izquierdo)
        yield from self._pre_order(nodo.derecho)
    
    def post_order(self):
        """
        Recorrido post-order (izquierda → derecha → raíz).
        Generador que produce (nodo, operacion, info_extra).
        """
        yield from self._post_order(self.raiz)
    
    def _post_order(self, nodo):
        if nodo is None:
            return
        yield from self._post_order(nodo.izquierdo)
        yield from self._post_order(nodo.derecho)
        yield nodo, "postorden", {"mensaje": f"📌 Postorden: {nodo.valor}"}
    
    def bfs(self):
        """
        Recorrido por niveles (BFS - Breadth First Search).
        Generador que produce (nodo, operacion, info_extra).
        """
        if self.raiz is None:
            return
        
        cola = deque([(self.raiz, 0)])  # (nodo, nivel)
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
    
    # ==================== ESTADÍSTICAS ====================
    def altura(self):
        """Retorna la altura del árbol."""
        return self._altura(self.raiz)
    
    def _altura(self, nodo):
        if nodo is None:
            return -1
        return 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))
    
    def tamaño(self):
        """Retorna el número de nodos en el árbol."""
        return self._tamaño(self.raiz)
    
    def _tamaño(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._tamaño(nodo.izquierdo) + self._tamaño(nodo.derecho)
    
    def es_completo(self):
        """Verifica si el árbol es completo."""
        if self.raiz is None:
            return True
        return self._es_completo(self.raiz, 0, self.tamaño())
    
    def _es_completo(self, nodo, indice, tamaño):
        if nodo is None:
            return True
        if indice >= tamaño:
            return False
        return (self._es_completo(nodo.izquierdo, 2*indice+1, tamaño) and
                self._es_completo(nodo.derecho, 2*indice+2, tamaño))
    
    def es_balanceado(self):
        """Verifica si el árbol está balanceado (factor de balance ≤ 1)."""
        return self._es_balanceado(self.raiz)
    
    def _es_balanceado(self, nodo):
        if nodo is None:
            return True
        altura_izq = self._altura(nodo.izquierdo)
        altura_der = self._altura(nodo.derecho)
        if abs(altura_izq - altura_der) > 1:
            return False
        return self._es_balanceado(nodo.izquierdo) and self._es_balanceado(nodo.derecho)
    
    # ==================== CONSULTAS POR RANGO ====================
    def rango_valores(self, min_val, max_val):
        """
        Retorna lista de valores en el rango [min_val, max_val].
        Usa la propiedad BST para descartar subárboles completos.
        """
        resultado = []
        self._rango_valores(self.raiz, min_val, max_val, resultado)
        return resultado
    
    def _rango_valores(self, nodo, min_val, max_val, resultado):
        if nodo is None:
            return
        
        # Si el nodo está en el rango, agregarlo
        if min_val <= nodo.valor <= max_val:
            resultado.append(nodo.valor)
        
        # Si el valor mínimo es menor que el nodo, explorar izquierda
        if min_val < nodo.valor:
            self._rango_valores(nodo.izquierdo, min_val, max_val, resultado)
        
        # Si el valor máximo es mayor que el nodo, explorar derecha
        if max_val > nodo.valor:
            self._rango_valores(nodo.derecho, min_val, max_val, resultado)
    
    # ==================== IMPRESIÓN ASCII ====================
    def imprimir_ascii(self):
        """Imprime el árbol en formato ASCII (para consola)."""
        if self.raiz is None:
            print("🌳 Árbol vacío")
            return
        print("\n--- Estructura del BST ---")
        self._imprimir_ascii(self.raiz, "", True)
    
    def _imprimir_ascii(self, nodo, prefix, es_izquierdo):
        if nodo is None:
            return
        
        conector = "├── " if not es_izquierdo else "└── "
        if nodo == self.raiz:
            print(f"📌 {nodo.valor} (raíz)")
        else:
            print(f"{prefix}{conector}{nodo.valor}")
        
        extension = "│   " if not es_izquierdo else "    "
        self._imprimir_ascii(nodo.izquierdo, prefix + extension, True)
        self._imprimir_ascii(nodo.derecho, prefix + extension, False)