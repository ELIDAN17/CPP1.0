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
    
    def __repr__(self):
        return f"Nodo({self.valor})"