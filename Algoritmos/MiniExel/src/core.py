# src/core.py
"""
ESTRUCTURAS DE DATOS PRINCIPALES
Basado en el documento original:
- Lista Dinámica (hoja)
- Tabla Hash (indice_hash)
- Pila/Stack (historial)
- Cola/Queue (cola_atencion)
"""

from collections import deque
from copy import deepcopy
from src.models import Estudiante


class HojaCalculoAcademica:
    def __init__(self):
        # 1. LISTA DINÁMICA - almacenamiento secuencial
        self.hoja = []
        
        # 2. TABLA HASH - índice para búsqueda O(1)
        self.indice_hash = {}
        
        # 3. PILA (STACK) - para deshacer (LIFO)
        self.historial = []
        
        # 4. COLA (QUEUE) - atención FIFO
        self.cola_atencion = deque()
    
    # ==================== MÉTODOS AUXILIARES ====================
    
    def actualizar_hash(self):
        """Reconstruye el índice hash - O(n)"""
        self.indice_hash.clear()
        for idx, estudiante in enumerate(self.hoja):
            self.indice_hash[estudiante.codigo] = idx
    
    def guardar_historial(self):
        """Guarda el estado actual en la pila"""
        self.historial.append(deepcopy(self.hoja))
    
    # ==================== CRUD ====================
    
    def registrar_estudiante(self, codigo, nombre, nota1, nota2, nota3):
        """Registra nuevo estudiante - valida clave duplicada"""
        if codigo in self.indice_hash:
            return False, "❌ El código ya existe"
        
        estudiante = Estudiante(codigo, nombre, nota1, nota2, nota3)
        self.guardar_historial()
        self.hoja.append(estudiante)
        self.actualizar_hash()
        return True, f"✅ Estudiante {codigo} registrado"
    
    def buscar_estudiante(self, codigo):
        """Búsqueda por código usando Tabla Hash - O(1)"""
        if codigo in self.indice_hash:
            pos = self.indice_hash[codigo]
            if 0 <= pos < len(self.hoja):
                return self.hoja[pos]
        return None
    
    def actualizar_estudiante(self, codigo, nombre=None, nota1=None, nota2=None, nota3=None):
        """Actualiza datos de un estudiante"""
        estudiante = self.buscar_estudiante(codigo)
        if not estudiante:
            return False, "❌ Estudiante no encontrado"
        
        self.guardar_historial()
        if nombre:
            estudiante.nombre = nombre
        if nota1 is not None:
            estudiante.nota1 = nota1
        if nota2 is not None:
            estudiante.nota2 = nota2
        if nota3 is not None:
            estudiante.nota3 = nota3
        estudiante.promedio = estudiante.calcular_promedio()
        return True, f"✅ Estudiante {codigo} actualizado"
    
    def eliminar_estudiante(self, codigo):
        """Elimina un estudiante"""
        if codigo not in self.indice_hash:
            return False, "❌ Estudiante no encontrado"
        
        self.guardar_historial()
        pos = self.indice_hash[codigo]
        self.hoja.pop(pos)
        self.actualizar_hash()
        return True, f"✅ Estudiante {codigo} eliminado"
    
    # ==================== DESHACER (STACK) ====================
    
    def deshacer(self):
        """Restaura el estado anterior desde la pila (LIFO)"""
        if self.historial:
            self.hoja = self.historial.pop()
            self.actualizar_hash()
            return True, "↩️ Estado restaurado"
        return False, "⚠️ No hay acciones para deshacer"
    
    # ==================== COLA (QUEUE FIFO) ====================
    
    def agregar_cola_atencion(self, codigo):
        """Agrega estudiante a la cola FIFO"""
        if codigo not in self.indice_hash:
            return False, "❌ Código no registrado"
        self.cola_atencion.append(codigo)
        return True, "👤 Estudiante agregado a la cola"
    
    def atender_estudiante(self):
        """Atiende al siguiente estudiante en la cola FIFO"""
        if self.cola_atencion:
            codigo = self.cola_atencion.popleft()
            estudiante = self.buscar_estudiante(codigo)
            if estudiante:
                return True, f"🎓 Atendiendo: {estudiante.nombre}", estudiante
        return False, "📭 Cola vacía", None
    
    def obtener_cola(self):
        """Obtiene la lista de estudiantes en cola"""
        resultado = []
        for codigo in self.cola_atencion:
            est = self.buscar_estudiante(codigo)
            if est:
                resultado.append((codigo, est.nombre))
        return resultado
    
    def limpiar_cola(self):
        """Limpia toda la cola de atención"""
        self.cola_atencion.clear()
    
    # ==================== ORDENAMIENTO ====================
    
    def quickSort(self, lista):
        """QuickSort por promedio (descendente) - O(n log n) promedio"""
        if len(lista) <= 1:
            return lista
        pivote = lista[-1]
        mayores = [x for x in lista[:-1] if x.promedio >= pivote.promedio]
        menores = [x for x in lista[:-1] if x.promedio < pivote.promedio]
        return self.quickSort(mayores) + [pivote] + self.quickSort(menores)
    
    def mergeSort(self, lista):
        """MergeSort por código (ascendente) - O(n log n) garantizado"""
        if len(lista) <= 1:
            return lista
        medio = len(lista) // 2
        izquierda = self.mergeSort(lista[:medio])
        derecha = self.mergeSort(lista[medio:])
        return self._merge(izquierda, derecha)
    
    def _merge(self, izquierda, derecha):
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
    
    def ordenar_por_promedio(self):
        """Ordena por promedio usando QuickSort"""
        if not self.hoja:
            return False, "⚠️ No hay datos para ordenar"
        self.guardar_historial()
        self.hoja = self.quickSort(self.hoja)
        self.actualizar_hash()
        return True, "📊 Ordenado por PROMEDIO (QuickSort)"
    
    def ordenar_por_codigo(self):
        """Ordena por código usando MergeSort"""
        if not self.hoja:
            return False, "⚠️ No hay datos para ordenar"
        self.guardar_historial()
        self.hoja = self.mergeSort(self.hoja)
        self.actualizar_hash()
        return True, "🔤 Ordenado por CÓDIGO (MergeSort)"
    
    # ==================== RECURSIVIDAD ====================
    
    def suma_promedios_recursiva(self, i=0):
        """Suma recursiva de promedios - O(n) tiempo, O(n) espacio"""
        if i == len(self.hoja):
            return 0.0
        return self.hoja[i].promedio + self.suma_promedios_recursiva(i + 1)
    
    def contar_aprobados_recursiva(self, i=0, umbral=10.5):
        """Cuenta aprobados recursivamente"""
        if i == len(self.hoja):
            return 0
        aprobado = 1 if self.hoja[i].promedio >= umbral else 0
        return aprobado + self.contar_aprobados_recursiva(i + 1, umbral)
    
    def obtener_estadisticas(self):
        """Estadísticas usando recursividad"""
        if not self.hoja:
            return {
                'total': 0,
                'promedio_general': 0.0,
                'aprobados': 0,
                'desaprobados': 0,
                'nota_maxima': 0.0,
                'nota_minima': 0.0
            }
        
        suma = self.suma_promedios_recursiva()
        total = len(self.hoja)
        promedio_general = suma / total
        aprobados = self.contar_aprobados_recursiva()
        notas = [e.promedio for e in self.hoja]
        nota_maxima = max(notas)
        nota_minima = min(notas)
        
        return {
            'total': total,
            'promedio_general': round(promedio_general, 2),
            'aprobados': aprobados,
            'desaprobados': total - aprobados,
            'nota_maxima': round(nota_maxima, 2),
            'nota_minima': round(nota_minima, 2)
        }
    
    # ==================== UTILIDADES ====================
    
    def obtener_todos(self):
        """Retorna copia de la lista de estudiantes"""
        return self.hoja.copy()
    
    def vaciar(self):
        """Limpia todas las estructuras"""
        self.hoja.clear()
        self.indice_hash.clear()
        self.historial.clear()
        self.cola_atencion.clear()
        
    def columna_a_numero(self, letra_columna):
        """Convierte letra de columna (A, B, C, AA, AB) a número (1, 2, 3, 27, 28)"""
        numero = 0
        for letra in letra_columna.upper():
            numero = numero * 26 + (ord(letra) - ord('A') + 1)
        return numero
    
    def buscar_por_coordenada(self, coordenada):
        """
        Busca el valor de una celda por coordenada estilo Excel (ej: "B3", "F10")
    
        Args:
            coordenada: string como "B3" o "F10"
    
        Returns:
            El valor en esa celda
        """
        # Separar letras y números (ej: "B3" → letras="B", numero="3")
        letras = ''
        numeros = ''
        for c in coordenada:
            if c.isalpha():
                letras += c
            else:
                numeros += c
    
        if not letras or not numeros:
            return None
    
        # Convertir letras a número de columna
        num_columna = self.columna_a_numero(letras)
        num_fila = int(numeros) - 1  # Excel empieza en 1, nosotros en 0
    
        # Verificar que la fila existe
        if num_fila >= len(self.hoja):
            return f"[ERROR] Fila {num_fila+1} no existe"
    
        estudiante = self.hoja[num_fila]
    
        # Mapear columna a campo del estudiante
        columnas = {
            1: "codigo",      # Columna A
            2: "nombre",      # Columna B
            3: "nota1",       # Columna C
            4: "nota2",       # Columna D
            5: "nota3",       # Columna E
            6: "promedio"     # Columna F
        }
    
        if num_columna in columnas:
            campo = columnas[num_columna]
            return getattr(estudiante, campo)
        else:
            return f"[ERROR] Columna {letras} fuera de rango (solo A-F)"
    
    def __len__(self):
        return len(self.hoja)