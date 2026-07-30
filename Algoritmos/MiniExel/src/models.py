# src/models.py
"""
MODELO DE DATOS - Estudiante
Representa un registro de la hoja de cálculo académica
"""

class Estudiante:
    def __init__(self, codigo, nombre, nota1, nota2, nota3):
        self.codigo = codigo
        self.nombre = nombre
        self.nota1 = nota1
        self.nota2 = nota2
        self.nota3 = nota3
        
        self.promedio = self.calcular_promedio()
    
    def calcular_promedio(self):
        """Calcula el promedio aritmético de las 3 notas"""
        return round((self.nota1 + self.nota2 + self.nota3) / 3, 2)
    
    def actualizar(self, nombre=None, nota1=None, nota2=None, nota3=None):
        """Actualiza los datos del estudiante y recalcula el promedio"""
        if nombre:
            self.nombre = nombre
        if nota1 is not None:
            self.nota1 = nota1
        if nota2 is not None:
            self.nota2 = nota2
        if nota3 is not None:
            self.nota3 = nota3
        self.promedio = self.calcular_promedio()
    
    def to_dict(self):
        """Convierte el objeto a diccionario para exportar a CSV"""
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'nota1': self.nota1,
            'nota2': self.nota2,
            'nota3': self.nota3,
            'promedio': self.promedio
        }