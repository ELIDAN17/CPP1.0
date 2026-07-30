# Simulación de desarrollo modificado con sprints para un sistema de estudiantes
class Estudiante:
    def __init__(self, nombre, edad, codigo):
        self.nombre = nombre
        self.edad = edad
        self.codigo = codigo
    def actualizar(self, nombre=None, edad=None):
        if nombre:
            self.nombre = nombre
        if edad:
            self.edad = edad
    def __str__(self):
        return f"[{self.codigo}] {self.nombre}, {self.edad} años"
class Sprint:
    def __init__(self, nombre, backlog):
        self.nombre = nombre
        self.backlog = backlog
        self.done = []
    def ejecutar(self):
        print(f"--- Ejecutando {self.nombre} ---")
        for tarea in self.backlog:
            print(f"Tarea pendiente: {tarea}")
            self.done.append(tarea)
            print(f"✔ Tarea completada: {tarea}")
        print(f"--- Fin de {self.nombre} ---\n")
    def reporte(self):
        print(f"Reporte {self.nombre}:")
        print("Backlog original:", self.backlog)
        print("Tareas completadas:", self.done)
        faltantes = [t for t in self.backlog if t not in self.done]
        print("Faltantes:", faltantes)
        print()   
class SistemaEstudiantes:
    def __init__(self):
        self.estudiantes = {}  # Acceso rápido por código
    def registrar(self, estudiante):
        if estudiante.codigo in self.estudiantes:
            print(f"Error: El código {estudiante.codigo} ya existe. Estudiante no registrado.")
            return False
        self.estudiantes[estudiante.codigo] = estudiante
        print(f"Estudiante registrado: {estudiante.nombre}")
        return True
    def buscar_por_codigo(self, codigo):
        return self.estudiantes.get(codigo, None)
    def listar_todos(self):
        print("\n--- Lista de Estudiantes ---")
        if not self.estudiantes:
            print("No hay estudiantes registrados.")
            return
        for estudiante in self.estudiantes.values():
            print(estudiante)
        print("----------------------------\n")
    def eliminar(self, codigo):
        if codigo in self.estudiantes:
            del self.estudiantes[codigo]
            print(f"Estudiante con código {codigo} eliminado.")
        else:
            print(f"Error: Estudiante con código {codigo} no encontrado.")
if __name__ == "__main__":
    sistema = SistemaEstudiantes()
    sprint1 = Sprint("Sprint 1", [
        "Registrar estudiante",
        "Listar estudiantes"
    ])
    sprint2 = Sprint("Sprint 2", [
        "Actualizar estudiante",
        "Eliminar estudiante",
        "Buscar por código"
    ])
    sprint3 = Sprint("Sprint 3", [
        "Validar datos de entrada",
        "Generar reporte de todos los estudiantes",
        "Verificar duplicados"
    ])
    print("--- Simulación de Proceso Modificado ---")
    # Simulación de ejecución de sprints y uso del sistema
    sprint1.ejecutar()
    sprint1.reporte()
    estudiante1 = Estudiante("Juan Perez", 20, "1001")
    estudiante2 = Estudiante("Maria Lopez", 22, "1002")
    sistema.registrar(estudiante1)
    sistema.registrar(estudiante2)
    sistema.listar_todos()
    sprint2.ejecutar()
    sprint2.reporte()
    estudiante_buscado = sistema.buscar_por_codigo("1001")
    if estudiante_buscado:
        estudiante_buscado.actualizar(edad=21)
        print(f"Estudiante actualizado: {estudiante_buscado}")
    sistema.eliminar("1002")
    sistema.listar_todos()
    sprint3.ejecutar()
    sprint3.reporte()
    estudiante3 = Estudiante("Pedro Gomez", 20, "1001")
    sistema.registrar(estudiante3) # falla por duplicado

""""
# Simulación de desarrollo ágil con sprints para un sistema de estudiantes
class Estudiante:
    def __init__(self, nombre, edad, codigo): #constructor(objeto, parametros)
        self.nombre = nombre 
        self.edad = edad
        self.codigo = codigo
    def actualizar(self, nombre=None, edad=None): #actulizar 
        if nombre:
            self.nombre = nombre
        if edad:
            self.edad = edad
    def __str__(self): #representacion cadena
        return f"[{self.codigo}] {self.nombre}, {self.edad} años" #f=f-string
class Sprint:
    def __init__(self, nombre, backlog): #constructor
        self.nombre = nombre
        self.backlog = backlog # lista de funciones a implementar
        self.done = []
    def ejecutar(self): #recorre la lista backlog
        print(f"--- Ejecutando {self.nombre} ---")
        for tarea in self.backlog:
            print(f"Tarea pendiente: {tarea}")
        # Simular: la tarea se completa
        self.done.append(tarea)
        print(f"✔ Tarea completada: {tarea}")
        print(f"--- Fin de {self.nombre} ---\n")
    def reporte(self): #reporte de tareas
        print(f"Reporte {self.nombre}:")
        print("Backlog original:", self.backlog)
        print("Tareas completadas:", self.done)
        faltantes = [t for t in self.backlog if t not in self.done]
        print("Faltantes:", faltantes)
        print()
if __name__ == "__main__":
    # Definición de backlog para cada sprint
    sprint1 = Sprint("Sprint 1", [
    "Registrar estudiante",
    "Listar estudiantes"
])
sprint2 = Sprint("Sprint 2", [
    "Actualizar estudiante",
    "Eliminar estudiante"
])
sprint3 = Sprint("Sprint 3", [
    "Validar datos de entrada",
    "Generar reporte de todos los estudiantes"
])
 # Simulación de ejecución de sprints
sprint1.ejecutar()
sprint1.reporte()
sprint2.ejecutar()
sprint2.reporte()
sprint3.ejecutar()
sprint3.reporte()
 # Comparación con proceso cascada simulado:
 # En cascada, primero se hubiera planeado todo el backlog completo antes de codificar ninguna tarea,
 # y pruebas al final.
"""