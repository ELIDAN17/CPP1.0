# src/controllers.py
"""
CONTROLADOR - Lógica de negocio
Conecta la interfaz gráfica con las estructuras de datos
Implementa el patrón MVC (Model-View-Controller)
"""

from src.core import HojaCalculoAcademica
from src.models import Estudiante
from src.algorithms import CalculosRecursivos


class ControladorHojaCalculo:
    def __init__(self):
        """Inicializa el controlador con una instancia de la hoja de cálculo"""
        self.hoja = HojaCalculoAcademica()
    
    # ==================== CRUD DE ESTUDIANTES ====================
    
    def registrar_estudiante(self, codigo, nombre, nota1, nota2, nota3):
        """
        Registra un nuevo estudiante con validaciones
        
        Args:
            codigo: Código único del estudiante
            nombre: Nombre completo
            nota1, nota2, nota3: Calificaciones (0-20)
        
        Returns:
            tuple: (exito, mensaje)
        """
        if not codigo or not nombre:
            return False, "Código y nombre son obligatorios"
        if not (0 <= nota1 <= 20 and 0 <= nota2 <= 20 and 0 <= nota3 <= 20):
            return False, "Las notas deben estar entre 0 y 20"
        
        return self.hoja.registrar_estudiante(codigo, nombre, nota1, nota2, nota3)
    
    def actualizar_estudiante(self, codigo, nombre=None, nota1=None, nota2=None, nota3=None):
        """
        Actualiza los datos de un estudiante existente
        
        Args:
            codigo: Código del estudiante a modificar
            nombre: Nuevo nombre (opcional)
            nota1, nota2, nota3: Nuevas notas (opcionales)
        
        Returns:
            tuple: (exito, mensaje)
        """
        return self.hoja.actualizar_estudiante(codigo, nombre, nota1, nota2, nota3)
    
    def eliminar_estudiante(self, codigo):
        """
        Elimina un estudiante de la hoja de cálculo
        
        Args:
            codigo: Código del estudiante a eliminar
        
        Returns:
            tuple: (exito, mensaje)
        """
        return self.hoja.eliminar_estudiante(codigo)
    
    def buscar_estudiante(self, codigo):
        """
        Busca un estudiante por código (búsqueda O(1) vía Hash)
        
        Args:
            codigo: Código del estudiante
        
        Returns:
            Estudiante or None
        """
        return self.hoja.buscar_estudiante(codigo)
    
    # ==================== ORDENAMIENTOS ====================
    
    def ordenar_por_promedio(self):
        """
        Ordena los estudiantes por promedio (descendente) usando QuickSort
        
        Returns:
            tuple: (exito, mensaje)
        """
        return self.hoja.ordenar_por_promedio()
    
    def ordenar_por_codigo(self):
        """
        Ordena los estudiantes por código (ascendente) usando MergeSort
        
        Returns:
            tuple: (exito, mensaje)
        """
        return self.hoja.ordenar_por_codigo()
    
    # ==================== SISTEMA DESHACER (STACK) ====================
    
    def deshacer(self):
        """
        Revierte la última modificación usando la Pila (Stack LIFO)
        
        Returns:
            tuple: (exito, mensaje)
        """
        return self.hoja.deshacer()
    
    # ==================== COLA DE ATENCIÓN (FIFO) ====================
    
    def agregar_a_cola(self, codigo):
        """
        Agrega un estudiante a la cola de atención (FIFO)
        
        Args:
            codigo: Código del estudiante
        
        Returns:
            tuple: (exito, mensaje)
        """
        return self.hoja.agregar_cola_atencion(codigo)
    
    def atender_siguiente(self):
        """
        Atiende al siguiente estudiante en la cola (FIFO)
        
        Returns:
            tuple: (exito, mensaje, estudiante)
        """
        return self.hoja.atender_estudiante()
    
    def obtener_cola_estado(self):
        """
        Obtiene el estado actual de la cola de atención
        
        Returns:
            list: Lista de tuplas (codigo, nombre)
        """
        return self.hoja.obtener_cola()
    
    def limpiar_cola(self):
        """Limpia toda la cola de atención"""
        self.hoja.limpiar_cola()
    
    # ==================== ESTADÍSTICAS RECURSIVAS ====================
    
    def obtener_estadisticas_recursivas(self):
        """
        Calcula estadísticas usando funciones recursivas puras
        
        Returns:
            dict: Diccionario con todas las métricas
        """
        return self.hoja.obtener_estadisticas()
    
    # ==================== MÉTODOS AUXILIARES ====================
    
    def obtener_datos_para_tabla(self):
        """
        Obtiene los datos formateados para mostrar en la tabla de la UI
        
        Returns:
            list: Lista de diccionarios con datos de estudiantes
        """
        return [e.to_dict() for e in self.hoja.obtener_todos()]
    
    def obtener_total_estudiantes(self):
        """Retorna la cantidad total de estudiantes registrados"""
        return len(self.hoja)