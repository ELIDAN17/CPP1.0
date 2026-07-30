from collections import deque
class Cola:
    def __init__(self):
        self.elementos = deque()

    def enqueue(self, valor):
        self.elementos.append(valor)
        print(f"Encolado: {valor}")

    def dequeue(self):
        if self.esta_vacia():
            print("Error: Cola vacia")
            return None
        eliminado = self.elementos.popleft()
        print(f"Desencolado: {eliminado}")
        return eliminado

    def mostrar(self):
        if self.esta_vacia():
            print("Cola vacia")
            return
        print("Cola final (de frente a final):")
        for elemento in self.elementos:
            print(elemento)

    def esta_vacia(self):
        return len(self.elementos) == 0

if __name__ == "__main__":
    c = Cola()
    print("=== Encolando elementos ===")
    c.enqueue(3)
    c.enqueue(6)
    c.enqueue(9)
    c.enqueue(12)
    print("\n=== Desencolando un elemento ===")
    c.dequeue()
    print("\n=== Estado final ===")
    c.mostrar()