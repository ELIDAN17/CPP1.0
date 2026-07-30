import unittest

class Usuario:
    def __init__(self, nombre, email, edad):
        self.nombre = nombre
        self.email = email
        self.edad = edad

    def es_mayor_de_edad(self):
        return self.edad > 18

class TestUsuario(unittest.TestCase):
    def test_usuario_valido(self):
        # Prueba de usuario adulto (mayor de edad)
        u = Usuario("Aldo", "aldo@unap.edu.pe", 30)
        self.assertTrue(u.es_mayor_de_edad())

    def test_usuario_menor_edad(self):
        # Prueba de usuario menor de edad
        u = Usuario("Luis", "luis@test.com", 15)
        self.assertFalse(u.es_mayor_de_edad())
        
    def test_edad_invalida(self):
        # Prueba diseñada para fallar y demostrar la falta de validación
        u = Usuario("Ana", "ana@test.com", -5)
        # Esto DEBERÍA fallar si la validación no está implementada.
        # En la versión inicial, esta prueba PASA, lo cual es el problema.
        self.assertTrue(u.edad >= 0)
        
if __name__ == "__main__":
    unittest.main()