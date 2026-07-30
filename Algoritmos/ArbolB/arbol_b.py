# arbol_b.py
"""
ÁRBOL B PARA CATÁLOGO DE BIBLIOTECA
Implementación completa con inserción, búsqueda y eliminación
"""

from dataclasses import dataclass
from typing import Optional, Tuple, List


@dataclass
class Libro:
    """Modelo de libro para el catálogo"""
    codigo_topo: str    
    titulo: str
    autor: str
    disponible: bool = True


class NodoB:
    """Nodo de un árbol B"""
    def __init__(self, es_hoja: bool = True):
        self.claves: List[str] = []          # Códigos topográficos (ordenados)
        self.libros: List[Libro] = []        # Libros (paralelo a claves)
        self.hijos: List[NodoB] = []         # Hijos (solo si no es hoja)
        self.es_hoja: bool = es_hoja


class ArbolBBiblioteca:
    """Árbol B para indexar el catálogo de la biblioteca"""
    
    def __init__(self, t: int = 50):
        """
        Args:
            t: Orden mínimo del árbol B
                - t=2: árbol B clásico (mínimo)
                - t=50: simula bloque de disco (recomendado para biblioteca)
                - t=100: optimizado para disco
        """
        self.t = t
        self.raiz = NodoB(es_hoja=True)
    
    # ==================== BÚSQUEDA ====================
    
    def buscar(self, codigo: str) -> Optional[Tuple[NodoB, int]]:
        """
        Busca un código en el árbol B.
        
        Returns:
            (nodo, índice) si encuentra, None si no existe
        """
        return self._buscar(self.raiz, codigo)
    
    def _buscar(self, nodo: NodoB, codigo: str) -> Optional[Tuple[NodoB, int]]:
        i = 0
        # Buscar la posición donde debería estar el código
        while i < len(nodo.claves) and codigo > nodo.claves[i]:
            i += 1
        
        # Si encontramos el código
        if i < len(nodo.claves) and codigo == nodo.claves[i]:
            return (nodo, i)
        
        # Si es hoja, no existe
        if nodo.es_hoja:
            return None
        
        # Buscar en el hijo correspondiente
        return self._buscar(nodo.hijos[i], codigo)
    
    # ==================== VERIFICACIÓN ====================
    
    def recorrido_inorder(self) -> List[str]:
        """Retorna todos los códigos en orden ascendente"""
        resultado = []
        self._inorder(self.raiz, resultado)
        return resultado
    
    def _inorder(self, nodo: NodoB, resultado: List[str]):
        if nodo.es_hoja:
            resultado.extend(nodo.claves)
        else:
            for i in range(len(nodo.claves)):
                self._inorder(nodo.hijos[i], resultado)
                resultado.append(nodo.claves[i])
            self._inorder(nodo.hijos[-1], resultado)
    
    def altura(self) -> int:
        """Retorna la altura del árbol (número de niveles)"""
        if not self.raiz.claves:
            return 0
        return self._altura(self.raiz)
    
    def _altura(self, nodo: NodoB) -> int:
        if nodo.es_hoja:
            return 1
        return 1 + self._altura(nodo.hijos[0])

    # ==================== INSERCIÓN ====================
    
    def insertar(self, codigo: str, libro: Libro):
        """Inserta un libro en el árbol B"""
        raiz = self.raiz
        
        # Si la raíz está llena, crear nueva raíz
        if len(raiz.claves) == 2 * self.t - 1:
            nueva_raiz = NodoB(es_hoja=False)
            nueva_raiz.hijos.append(self.raiz)
            self._split(nueva_raiz, 0, self.raiz)
            self.raiz = nueva_raiz
        
        self._insertar_no_lleno(self.raiz, codigo, libro)
    
    def _split(self, padre: NodoB, i: int, y: NodoB):
        """
        Divide el nodo 'y' en dos, subiendo la clave media al padre.
        
        Args:
            padre: Nodo padre que contiene a 'y'
            i: Índice donde se encuentra 'y' en padre.hijos
            y: Nodo que está lleno y debe dividirse
        """
        t = self.t
        
        # Crear nuevo nodo 'z' (hermano derecho de 'y')
        z = NodoB(es_hoja=y.es_hoja)
        
        # Mover la mitad superior de claves a 'z'
        z.claves = y.claves[t:]          # Desde t hasta el final
        z.libros = y.libros[t:]
        
        # Mover la mitad superior de hijos a 'z' (si no es hoja)
        if not y.es_hoja:
            z.hijos = y.hijos[t:]
        
        # Guardar la clave media (t-1)
        clave_media = y.claves[t - 1]
        libro_medio = y.libros[t - 1]
        
        # Reducir 'y' a la mitad inferior
        y.claves = y.claves[:t - 1]
        y.libros = y.libros[:t - 1]
        if not y.es_hoja:
            y.hijos = y.hijos[:t]
        
        # Insertar 'z' como hijo del padre
        padre.hijos.insert(i + 1, z)
        padre.claves.insert(i, clave_media)
        padre.libros.insert(i, libro_medio)
    
    def _insertar_no_lleno(self, nodo: NodoB, codigo: str, libro: Libro):
        """Inserta en un nodo que NO está lleno"""
        i = len(nodo.claves) - 1
        
        if nodo.es_hoja:
            # Insertar en hoja (ordenado)
            nodo.claves.append(None)
            nodo.libros.append(None)
            
            while i >= 0 and codigo < nodo.claves[i]:
                nodo.claves[i + 1] = nodo.claves[i]
                nodo.libros[i + 1] = nodo.libros[i]
                i -= 1
            
            nodo.claves[i + 1] = codigo
            nodo.libros[i + 1] = libro
        
        else:
            # Nodo interno: buscar hijo apropiado
            while i >= 0 and codigo < nodo.claves[i]:
                i -= 1
            i += 1
            
            # Si el hijo está lleno, dividirlo
            if len(nodo.hijos[i].claves) == 2 * self.t - 1:
                self._split(nodo, i, nodo.hijos[i])
                if codigo > nodo.claves[i]:
                    i += 1
            
            self._insertar_no_lleno(nodo.hijos[i], codigo, libro)

    # ==================== ELIMINACIÓN ====================
    
    def eliminar(self, codigo: str):
        """Elimina un libro del árbol B por su código"""
        if not self._buscar(self.raiz, codigo):
            raise KeyError(f"Código no encontrado: {codigo}")
        
        self._eliminar(self.raiz, codigo)
        
        # Si la raíz quedó vacía y tiene hijos, bajar el hijo
        if len(self.raiz.claves) == 0 and not self.raiz.es_hoja:
            self.raiz = self.raiz.hijos[0]
    
    def _eliminar(self, nodo: NodoB, codigo: str):
        """Eliminación recursiva con los 3 casos"""
        t = self.t
        
        # Buscar la posición del código
        i = 0
        while i < len(nodo.claves) and codigo > nodo.claves[i]:
            i += 1
        
        # Caso 1 y 2: El código está en este nodo
        if i < len(nodo.claves) and nodo.claves[i] == codigo:
            if nodo.es_hoja:
                # Caso 1: Eliminar de hoja
                nodo.claves.pop(i)
                nodo.libros.pop(i)
            else:
                # Caso 2: Eliminar de nodo interno
                self._eliminar_interno(nodo, i)
        
        else:
            # Caso 3: El código está en un hijo
            if nodo.es_hoja:
                raise KeyError(f"Código no encontrado: {codigo}")
            
            # Verificar si el hijo necesita balanceo
            if len(nodo.hijos[i].claves) == t - 1:
                self._balancear_hijo(nodo, i)
            
            # Continuar eliminando en el hijo correspondiente
            if i > len(nodo.claves):
                self._eliminar(nodo.hijos[i - 1], codigo)
            else:
                self._eliminar(nodo.hijos[i], codigo)
    
    def _eliminar_interno(self, nodo: NodoB, i: int):
        """Caso 2: Eliminar clave de nodo interno"""
        t = self.t
        codigo = nodo.claves[i]
        
        # Caso 2a: Hijo izquierdo tiene al menos t claves → usar predecesor
        if len(nodo.hijos[i].claves) >= t:
            pred, libro = self._obtener_predecesor(nodo, i)
            nodo.claves[i] = pred
            nodo.libros[i] = libro
            self._eliminar(nodo.hijos[i], pred)
        
        # Caso 2b: Hijo derecho tiene al menos t claves → usar sucesor
        elif len(nodo.hijos[i + 1].claves) >= t:
            suc, libro = self._obtener_sucesor(nodo, i)
            nodo.claves[i] = suc
            nodo.libros[i] = libro
            self._eliminar(nodo.hijos[i + 1], suc)
        
        # Caso 2c: Ambos hijos tienen t-1 claves → fusionar
        else:
            self._fusionar(nodo, i)
            self._eliminar(nodo.hijos[i], codigo)
    
    def _obtener_predecesor(self, nodo: NodoB, i: int):
        """Obtiene el máximo del subárbol izquierdo"""
        cur = nodo.hijos[i]
        while not cur.es_hoja:
            cur = cur.hijos[-1]
        return cur.claves[-1], cur.libros[-1]
    
    def _obtener_sucesor(self, nodo: NodoB, i: int):
        """Obtiene el mínimo del subárbol derecho"""
        cur = nodo.hijos[i + 1]
        while not cur.es_hoja:
            cur = cur.hijos[0]
        return cur.claves[0], cur.libros[0]
    
    def _fusionar(self, nodo: NodoB, i: int):
        """Fusiona nodo.hijos[i] y nodo.hijos[i+1] con la clave media"""
        hijo = nodo.hijos[i]
        hermano = nodo.hijos[i + 1]
        
        # Mover clave media al hijo
        hijo.claves.append(nodo.claves[i])
        hijo.libros.append(nodo.libros[i])
        
        # Mover todas las claves del hermano al hijo
        hijo.claves.extend(hermano.claves)
        hijo.libros.extend(hermano.libros)
        
        # Mover hijos del hermano si no es hoja
        if not hijo.es_hoja:
            hijo.hijos.extend(hermano.hijos)
        
        # Eliminar la clave y el hermano del padre
        nodo.claves.pop(i)
        nodo.libros.pop(i)
        nodo.hijos.pop(i + 1)
    
    def _balancear_hijo(self, nodo: NodoB, i: int):
        """Asegura que el hijo i tenga al menos t claves"""
        t = self.t
        
        # Intentar prestar del hermano izquierdo
        if i != 0 and len(nodo.hijos[i - 1].claves) >= t:
            self._prestar_de_izquierda(nodo, i)
        
        # Intentar prestar del hermano derecho
        elif i != len(nodo.claves) and len(nodo.hijos[i + 1].claves) >= t:
            self._prestar_de_derecha(nodo, i)
        
        # Si no se puede prestar, fusionar
        else:
            if i != len(nodo.claves):
                self._fusionar(nodo, i)
            else:
                self._fusionar(nodo, i - 1)
    
    def _prestar_de_izquierda(self, nodo: NodoB, i: int):
        """Presta una clave del hermano izquierdo"""
        hijo = nodo.hijos[i]
        hermano = nodo.hijos[i - 1]
        
        # Mover la clave del padre al hijo (al inicio)
        hijo.claves.insert(0, nodo.claves[i - 1])
        hijo.libros.insert(0, nodo.libros[i - 1])
        
        # Mover el último hijo del hermano al hijo
        if not hijo.es_hoja:
            hijo.hijos.insert(0, hermano.hijos.pop())
        
        # Actualizar la clave del padre con la última del hermano
        nodo.claves[i - 1] = hermano.claves.pop()
        nodo.libros[i - 1] = hermano.libros.pop()
    
    def _prestar_de_derecha(self, nodo: NodoB, i: int):
        """Presta una clave del hermano derecho"""
        hijo = nodo.hijos[i]
        hermano = nodo.hijos[i + 1]
        
        # Mover la clave del padre al hijo (al final)
        hijo.claves.append(nodo.claves[i])
        hijo.libros.append(nodo.libros[i])
        
        # Mover el primer hijo del hermano al hijo
        if not hijo.es_hoja:
            hijo.hijos.append(hermano.hijos.pop(0))
        
        # Actualizar la clave del padre con la primera del hermano
        nodo.claves[i] = hermano.claves.pop(0)
        nodo.libros[i] = hermano.libros.pop(0)
        
