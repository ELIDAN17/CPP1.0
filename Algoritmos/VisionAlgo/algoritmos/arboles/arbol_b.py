"""
Árbol B (multinodo) para bases de datos.
"""

class NodoB:
    """Nodo de árbol B."""
    
    def __init__(self, hoja=True):
        self.hoja = hoja
        self.claves = []
        self.hijos = []
    
    def __repr__(self):
        return f"NodoB({self.claves})"

class ArbolB:
    """Árbol B de orden mínimo t."""
    
    def __init__(self, t=3):
        self.t = t  # Grado mínimo
        self.raiz = NodoB(hoja=True)
    
    def insertar(self, valor):
        """Inserta un valor en el árbol B."""
        raiz = self.raiz
        
        if len(raiz.claves) == (2 * self.t - 1):
            nueva_raiz = NodoB(hoja=False)
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
        else:
            # Encontrar el hijo adecuado
            i = 0
            while i < len(nodo.claves) and valor > nodo.claves[i]:
                yield nodo, f"buscando_hijo_{i}"
                i += 1
            
            yield nodo.hijos[i], "accediendo_hijo"
            
            if len(nodo.hijos[i].claves) == (2 * self.t - 1):
                self._dividir_hijo(nodo, i)
                yield nodo, "dividiendo_hijo"
                
                if valor > nodo.claves[i]:
                    i += 1
            
            yield from self._insertar_no_lleno(nodo.hijos[i], valor)
    
    def _dividir_hijo(self, padre, i):
        """Divide el hijo i del padre."""
        t = self.t
        hijo = padre.hijos[i]
        nuevo_hijo = NodoB(hoja=hijo.hoja)
        
        # Mover la mitad de las claves al nuevo hijo
        medio = t - 1
        padre.claves.insert(i, hijo.claves[medio])
        nuevo_hijo.claves = hijo.claves[medio + 1:]
        hijo.claves = hijo.claves[:medio]
        
        # Mover los hijos si no es hoja
        if not hijo.hoja:
            nuevo_hijo.hijos = hijo.hijos[medio + 1:]
            hijo.hijos = hijo.hijos[:medio + 1]
        
        padre.hijos.insert(i + 1, nuevo_hijo)
    
    def buscar(self, valor):
        """Busca un valor en el árbol B."""
        yield from self._buscar(self.raiz, valor)
    
    def _buscar(self, nodo, valor):
        if nodo is None:
            yield None, "no_encontrado"
            return
        
        i = 0
        while i < len(nodo.claves) and valor > nodo.claves[i]:
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