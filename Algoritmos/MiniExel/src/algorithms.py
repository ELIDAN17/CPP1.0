# src/algorithms.py
"""
ALGORITMOS DE ORDENAMIENTO Y RECURSIVIDAD
Implementación de QuickSort, MergeSort y funciones recursivas para estadísticas
"""

from src.models import Estudiante


class AlgoritmosOrdenamiento:
    """Clase con algoritmos de ordenamiento divide y vencerás"""
    
    @staticmethod
    def quicksort_por_promedio(estudiantes):
        """
        QuickSort - Ordena por PROMEDIO (descendente de mayor a menor)
        Complejidad: O(n log n) promedio, O(n²) peor caso
        """
        if len(estudiantes) <= 1:
            return estudiantes.copy()
        
        pivote = estudiantes[-1]
        mayores = [e for e in estudiantes[:-1] if e.promedio >= pivote.promedio]
        menores = [e for e in estudiantes[:-1] if e.promedio < pivote.promedio]
        
        return (AlgoritmosOrdenamiento.quicksort_por_promedio(mayores) +
                [pivote] +
                AlgoritmosOrdenamiento.quicksort_por_promedio(menores))
    
    @staticmethod
    def mergesort_por_codigo(estudiantes):
        """
        MergeSort - Ordena por CÓDIGO (ascendente alfabético)
        Complejidad: O(n log n) siempre, estable, O(n) espacio
        """
        if len(estudiantes) <= 1:
            return estudiantes.copy()
        
        medio = len(estudiantes) // 2
        izquierda = AlgoritmosOrdenamiento.mergesort_por_codigo(estudiantes[:medio])
        derecha = AlgoritmosOrdenamiento.mergesort_por_codigo(estudiantes[medio:])
        
        return AlgoritmosOrdenamiento._merge(izquierda, derecha)
    
    @staticmethod
    def _merge(izquierda, derecha):
        """Fusiona dos listas ordenadas por código"""
        resultado = []
        i = j = 0
        while i < len(izquierda) and j < len(derecha):
            if izquierda[i].codigo <= derecha[j].codigo:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1
        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])
        return resultado


class CalculosRecursivos:
    """Funciones recursivas para cálculos estadísticos (sin bucles)"""
    
    @staticmethod
    def suma_promedios(estudiantes, indice=0):
        """
        Suma recursiva de promedios
        Complejidad: O(n) tiempo, O(n) espacio por recursión
        """
        if indice >= len(estudiantes):
            return 0.0
        return estudiantes[indice].promedio + CalculosRecursivos.suma_promedios(estudiantes, indice + 1)
    
    @staticmethod
    def promedio_general(estudiantes):
        """Promedio general usando recursividad"""
        if not estudiantes:
            return 0.0
        return CalculosRecursivos.suma_promedios(estudiantes) / len(estudiantes)
    
    @staticmethod
    def contar_aprobados(estudiantes, indice=0, umbral=10.5):
        """
        Cuenta estudiantes aprobados usando recursividad
        Umbral: promedio >= 10.5
        """
        if indice >= len(estudiantes):
            return 0
        aprobado = 1 if estudiantes[indice].promedio >= umbral else 0
        return aprobado + CalculosRecursivos.contar_aprobados(estudiantes, indice + 1, umbral)