class Nodo:
    def __init__(self, valor):
        self.dato = valor
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def insertar_inicio(self, valor):
        nuevo = Nodo(valor)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        print(f"Insertado al inicio: {valor}")

    def insertar_final(self, valor):
        nuevo = Nodo(valor)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            temp = self.cabeza
            while temp.siguiente:
                temp = temp.siguiente
            temp.siguiente = nuevo
        print(f"Insertado al final: {valor}")

    def eliminar_inicio(self):
        if self.cabeza is None:
            print("Error: Lista vacia")
            return
        eliminado = self.cabeza.dato
        self.cabeza = self.cabeza.siguiente
        print(f"Eliminado del inicio: {eliminado}")

    def mostrar(self):
        if self.cabeza is None:
            print("Lista vacia")
            return
        print("Lista final:")
        temp = self.cabeza
        while temp:
            print(temp.dato)
            temp = temp.siguiente

if __name__ == "__main__":
    lista = ListaEnlazada()
    print("=== Insertando al inicio ===")
    lista.insertar_inicio(8)
    lista.insertar_inicio(4)
    print("\n=== Insertando al final ===")
    lista.insertar_final(11)
    print("\n=== Eliminando primer nodo ===")
    lista.eliminar_inicio()
    print("\n=== Estado final ===")
    lista.mostrar()