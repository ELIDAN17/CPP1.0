# src/main.py
"""
PUNTO DE ENTRADA PRINCIPAL
Mini Hoja de Cálculo Académica - Estructuras de Datos y Algoritmos
"""

import sys
import os

# Agregar el directorio padre al path para imports relativos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui import MiniExcelAcademico


def main():
    """
    Función principal que inicia la aplicación.
    Muestra información de las estructuras implementadas.
    """
    print("=" * 70)
    print("🏫 MINI HOJA DE CÁLCULO ACADÉMICA - ESTRUCTURAS DE DATOS")
    print("=" * 70)
    print("\n📊 ESTRUCTURAS IMPLEMENTADAS:")
    print("  ✓ Lista Dinámica (almacenamiento secuencial)")
    print("  ✓ Tabla Hash (búsqueda O(1) por código)")
    print("  ✓ Pila/Stack (sistema Deshacer - LIFO)")
    print("  ✓ Cola/Queue (atención FIFO)")
    print("  ✓ QuickSort (ordenamiento por promedio - O(n log n))")
    print("  ✓ MergeSort (ordenamiento por código - O(n log n))")
    print("  ✓ Recursividad (cálculos estadísticos - O(n))")
    print("\n" + "=" * 70)
    print("🖱️ Iniciando interfaz gráfica...")
    print("=" * 70 + "\n")
    
    # Iniciar la aplicación
    app = MiniExcelAcademico()


if __name__ == "__main__":
    main()