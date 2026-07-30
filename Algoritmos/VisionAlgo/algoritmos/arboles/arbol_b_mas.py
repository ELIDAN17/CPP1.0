"""
Árbol B+ (versión mejorada para índices).
"""

from .arbol_b import NodoB

class NodoBPlus(NodoB):
    """Nodo de árbol B+ con enlace a siguiente hoja."""
    
    def __init__(self, hoja=True):
        super().__init__(hoja)
        self.siguiente = None  # Enlace a la siguiente hoja

class ArbolBMas:
    """Árbol B+ para índices de bases de datos."""
    
    def __init__(self, t=3):
        self.t = t
        self.raiz = NodoBPlus(hoja=True)
    
    def insertar(self, valor):
        """Inserta un valor en el árbol B+."""
        raiz = self.raiz
        
        if len(raiz.claves) == (2 * self.t - 1):
            nueva_raiz = NodoBPlus(hoja=False)
            nueva_raiz.hijos.append(raiz)
            self._dividir_hijo(nueva_raiz, 0)
            self.raiz = nueva_raiz
            yield self.raiz, "nueva_raiz"
        
        yield from self._insertar_no_lleno(self.raiz, valor)
    
    def _insertar_no_lleno(self, nodo, valor):
        """Inserta en un nodo no lleno."""
        if nodo.hoja:
            # Insertar en orden
            i = 0
            while i < len(nodo.claves) and valor > nodo.claves[i]:
                yield nodo, f"comparando_{i}"
                i += 1
            
            nodo.claves.insert(i, valor)
            yield nodo, f"insertado_en_hoja_{i}"
            
            # Actualizar enlace si es necesario
            if i == 0 and nodo.siguiente:
                yield nodo.siguiente, "actualizando_enlace"
        else:
            # Encontrar el hijo adecuado
            i = 0
            while i < len(nodo.claves) and valor >= nodo.claves[i]:
                yield nodo, f"buscando_hijo_{i}"
                i += 1
            
            yield nodo.hijos[i], "accediendo_hijo"
            
            if len(nodo.hijos[i].claves) == (2 * self.t - 1):
                self._dividir_hijo(nodo, i)
                yield nodo, "dividiendo_hijo"
                
                if valor >= nodo.claves[i]:
                    i += 1
            
            yield from self._insertar_no_lleno(nodo.hijos[i], valor)
    
    def _dividir_hijo(self, padre, i):
        """Divide el hijo i del padre (versión B+)."""
        t = self.t
        hijo = padre.hijos[i]
        nuevo_hijo = NodoBPlus(hoja=hijo.hoja)
        
        medio = t - 1
        
        if hijo.hoja:
            # Para hojas: mantener todas las claves
            padre.claves.insert(i, hijo.claves[medio])
            nuevo_hijo.claves = hijo.claves[medio:]
            hijo.claves = hijo.claves[:medio]
            
            # Actualizar enlace
            nuevo_hijo.siguiente = hijo.siguiente
            hijo.siguiente = nuevo_hijo
        else:
            # Para nodos internos: subir la clave media
            padre.claves.insert(i, hijo.claves[medio])
            nuevo_hijo.claves = hijo.claves[medio + 1:]
            hijo.claves = hijo.claves[:medio]
            
            # Mover hijos
            nuevo_hijo.hijos = hijo.hijos[medio + 1:]
            hijo.hijos = hijo.hijos[:medio + 1]
        
        padre.hijos.insert(i + 1, nuevo_hijo)
    
    def buscar(self, valor):
        """Busca un valor en el árbol B+."""
        yield from self._buscar(self.raiz, valor)
    
    def _buscar(self, nodo, valor):
        if nodo is None:
            yield None, "no_encontrado"
            return
        
        i = 0
        while i < len(nodo.claves) and valor >= nodo.claves[i]:
            yield nodo, f"comparando_{i}"
            i += 1
        
        if i < len(nodo.claves) and valor == nodo.claves[i]:
            yield nodo, "encontrado"
            return
        elif nodo.hoja:
            yield None, "no_encontrado"
            return
        else:
            yield nodo.hijos[i], "accediendo_hijo"
            yield from self._buscar(nodo.hijos[i], valor)
    
    def recorrer_hojas(self):
        """Recorre todas las hojas en orden (útil para índices)."""
        actual = self._primera_hoja()
        while actual:
            yield actual
            actual = actual.siguiente
    
    def _primera_hoja(self):
        """Encuentra la primera hoja del árbol."""
        actual = self.raiz
        while not actual.hoja:
            actual = actual.hijos[0]
        return actual
    
    # ========== MÉTODOS PARA ESTADÍSTICAS ==========
    
    def altura(self):
        """Retorna la altura del árbol B+."""
        return self._altura(self.raiz, 0)
    
    def _altura(self, nodo, nivel):
        if nodo is None or len(nodo.claves) == 0:
            return nivel - 1
        if nodo.hoja:
            return nivel
        return max(self._altura(hijo, nivel + 1) for hijo in nodo.hijos if hijo is not None)
    
    def tamaño(self):
        """Retorna el número total de claves en el árbol B+."""
        return self._tamaño(self.raiz)
    
    def _tamaño(self, nodo):
        if nodo is None or len(nodo.claves) == 0:
            return 0
        total = len(nodo.claves)
        for hijo in nodo.hijos:
            total += self._tamaño(hijo)
        return total
    
    def es_balanceado(self):
        """Los árboles B+ siempre están balanceados."""
        return True