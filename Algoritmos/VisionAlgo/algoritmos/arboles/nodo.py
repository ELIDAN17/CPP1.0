"""
Nodo para árboles binarios.
"""

class Nodo:
    """Nodo de árbol binario con atributos básicos."""
    
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.altura = 1  # Para AVL
        self.color = "rojo"  # Para Rojo-Negro (por defecto rojo)
        self.padre = None  # Para Rojo-Negro
        self.contador = 1  # Para manejo de duplicados (opcional)
    
    def __repr__(self):
        return f"Nodo({self.valor})"
    
    def es_hoja(self):
        """Retorna True si el nodo es hoja (no tiene hijos)."""
        return self.izquierdo is None and self.derecho is None
    
    def tiene_un_hijo(self):
        """Retorna True si el nodo tiene exactamente un hijo."""
        return (self.izquierdo is not None) != (self.derecho is not None)
    
    def tiene_dos_hijos(self):
        """Retorna True si el nodo tiene dos hijos."""
        return self.izquierdo is not None and self.derecho is not None