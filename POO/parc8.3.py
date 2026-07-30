import tkinter as tk

class Ascensor:
    def __init__(self, pisos=5, capacidad=4):
        self.piso_actual = 0
        self.num_pisos = pisos
        self.capacidad = capacidad

    def subir(self):
        if self.piso_actual < self.num_pisos - 1:
            self.piso_actual += 1

    def bajar(self):
        if self.piso_actual > 0:
            self.piso_actual -= 1

ascensor = Ascensor()

def actualizar():
    etiqueta.config(text=f"Piso actual: {ascensor.piso_actual}")

def subir():
    ascensor.subir()
    actualizar()

def bajar():
    ascensor.bajar()
    actualizar()

root = tk.Tk()
root.title("Ascensor")

etiqueta = tk.Label(root, text="Piso actual: 0", font=("Arial", 16))
etiqueta.pack()

tk.Button(root, text="Subir", command=subir).pack()
tk.Button(root, text="Bajar", command=bajar).pack()

root.mainloop()
