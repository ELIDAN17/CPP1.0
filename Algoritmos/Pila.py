class Pila:
    def __init__(self):
        self.elementos = []

    def push(self, dato):
        """Inserta un elemento en el tope de la pila."""
        self.elementos.append(dato)
        print(f"Insertado: {dato}")

    def pop(self):
        """Elimina y retorna el elemento del tope (LIFO)."""
        if self.esta_vacia():
            print("Error: Pila vacia")
            return None
        eliminado = self.elementos.pop()
        print(f"Eliminado: {eliminado}")
        return eliminado

    def mostrar(self):
        """Muestra la estructura actual de la pila."""
        if self.esta_vacia():
            print("Pila vacia")
            return
        print("Pila final (de tope a base):")
        # El tope es el último elemento insertado
        for elemento in reversed(self.elementos):
            print(f"| {elemento} |")
        print("-------")

    def esta_vacia(self):
        """Verifica si no hay elementos."""
        return len(self.elementos) == 0

if __name__ == "__main__":
    p = Pila()
    
    print("=== Insertando elementos ===")
    p.push(5)
    p.push(10)
    p.push(15)
    p.push(20)
    p.push(25)

    print("\n=== Eliminando dos elementos ===")
    p.pop()  # Elimina el 25
    p.pop()  # Elimina el 20

    print("\n=== Estado final ===")
    p.mostrar()