import tkinter as tk
from tkinter import messagebox

class CReal:
    def __init__(self, num=0.0):
        self.num = float(num)

    def imprimir(self):
        print(f"Valor: {self.num}")

    def get_signo(self):
        return '+' if self.num >= 0 else '-'

    def set_signo(self, s):
        if s == '+' and self.num < 0:
            self.num = abs(self.num)
        elif s == '-' and self.num > 0:
            self.num = -self.num

    @staticmethod
    def sumar(a, b):
        return CReal(a.num + b.num)

    @staticmethod
    def restar(a, b):
        return CReal(a.num - b.num)

    @staticmethod
    def multiplicar(a, b):
        return CReal(a.num * b.num)

    @staticmethod
    def dividir(a, b):
        if b.num == 0:
            raise ValueError("División por cero")
        return CReal(a.num / b.num)

# Interfaz gráfica
def operar(op):
    try:
        a = CReal(float(entry1.get()))
        b = CReal(float(entry2.get()))
        if op == '+':
            r = CReal.sumar(a, b)
        elif op == '-':
            r = CReal.restar(a, b)
        elif op == '*':
            r = CReal.multiplicar(a, b)
        elif op == '/':
            r = CReal.dividir(a, b)
        resultado.set(f"Resultado: {r.num} (signo: {r.get_signo()})")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Operaciones con CReal")

tk.Label(root, text="Número A").pack()
entry1 = tk.Entry(root)
entry1.pack()

tk.Label(root, text="Número B").pack()
entry2 = tk.Entry(root)
entry2.pack()

resultado = tk.StringVar()
tk.Label(root, textvariable=resultado).pack()

for op in ['+', '-', '*', '/']:
    tk.Button(root, text=op, command=lambda o=op: operar(o)).pack()

root.mainloop()
