# simulacion_biblioteca.py
"""
Simulación del catálogo de la Biblioteca Central UNA-PUNO
80,000 volúmenes indexados con árbol B
"""

import random
import time
from arbol_b import ArbolBBiblioteca, Libro


def generar_codigos_cdu(cantidad: int = 80000) -> list:
    """
    Genera códigos topográficos simulando el sistema CDU
    Formato: 'XXX.YYY LNN' donde:
        - XXX: número de clase (000-999)
        - YYY: número de subclase (000-999)
        - L: letra de autor (A-Z)
        - NN: número de autor (01-99)
    """
    codigos = set()
    
    while len(codigos) < cantidad:
        clase = f"{random.randint(0, 999):03d}"
        subclase = f"{random.randint(0, 999):03d}"
        letra = chr(65 + random.randint(0, 25))
        numero = f"{random.randint(1, 99):02d}"
        codigo = f"{clase}.{subclase} {letra}{numero}"
        codigos.add(codigo)
    
    return list(codigos)


def simular_catalogo():
    """Simula el catálogo completo de la biblioteca"""
    print("=" * 60)
    print("📚 BIBLIOTECA CENTRAL UNA-PUNO - ÁRBOL B")
    print("=" * 60)
    
    # Inicializar árbol B con t=50 (bloque de disco real)
    biblioteca = ArbolBBiblioteca(t=50)
    
    # 1. GENERAR 80,000 CÓDIGOS
    print("\n📝 Generando 80,000 códigos topográficos...")
    codigos = generar_codigos_cdu(80000)
    random.shuffle(codigos)
    
    # 2. INDEXAR LOS LIBROS
    print("📥 Indexando 80,000 volúmenes en el árbol B...")
    inicio = time.time()
    
    for i, cod in enumerate(codigos):
        libro = Libro(
            codigo_topo=cod,
            titulo=f"Obra académica {i+1}",
            autor=f"Autor {i % 500 + 1}"
        )
        biblioteca.insertar(cod, libro)
        
        if (i + 1) % 10000 == 0:
            print(f"  → {i+1} libros indexados...")
    
    fin = time.time()
    print(f"✅ Indexación completada en {fin - inicio:.2f} segundos")
    print(f"📊 Altura del árbol: {biblioteca.altura()}")
    
    # 3. SIMULAR PRÉSTAMOS (eliminaciones)
    print("\n📤 Simulando 500 préstamos (eliminación temporal)...")
    prestamos = random.sample(codigos, 500)
    
    for cod in prestamos:
        biblioteca.eliminar(cod)
    
    print(f"✅ {len(prestamos)} libros prestados (retirados del índice)")
    
    # 4. SIMULAR DEVOLUCIONES (reinserciones)
    print("\n📥 Simulando 300 devoluciones (reinserción)...")
    devoluciones = prestamos[:300]
    
    for cod in devoluciones:
        libro = Libro(
            codigo_topo=cod,
            titulo="(Reinsertado)",
            autor="(Reinsertado)"
        )
        biblioteca.insertar(cod, libro)
    
    print(f"✅ {len(devoluciones)} libros devueltos (reinsertados)")
    
    # 5. VERIFICAR INTEGRIDAD
    print("\n🔍 Verificando integridad del catálogo...")
    encontrados = 0
    for cod in codigos:
        if biblioteca.buscar(cod):
            encontrados += 1
    
    print(f"📊 Libros verificados: {encontrados}/{len(codigos)}")
    
    # 6. ESTADÍSTICAS FINALES
    print("\n📊 ESTADÍSTICAS FINALES")
    print("=" * 40)
    print(f"  Orden del árbol B (t): {biblioteca.t}")
    print(f"  Altura del árbol:      {biblioteca.altura()}")
    print(f"  Total de libros:       {len(codigos)}")
    print(f"  Libros disponibles:    {encontrados}")
    print(f"  Libros prestados:      {len(prestamos) - len(devoluciones)}")
    
    # 7. VERIFICAR ORDENAMIENTO
    print("\n📋 Verificando ordenamiento (In-Order)...")
    claves_ordenadas = biblioteca.recorrido_inorder()
    if claves_ordenadas == sorted(claves_ordenadas):
        print("✅ El catálogo está correctamente ordenado")
    else:
        print("❌ ERROR: El catálogo NO está ordenado")


if __name__ == "__main__":
    simular_catalogo()