from collections import deque
from copy import deepcopy

# Estructuras de datos globales
hoja = []
indice_hash = {}
historial = []
cola_atencion = deque()

def calcular_promedio(n1, n2, n3):
    return (n1 + n2 + n3) / 3.0

def actualizar_hash():
    indice_hash.clear()
    for idx, estudiante in enumerate(hoja):
        indice_hash[estudiante["codigo"]] = idx

def guardar_historial():
    historial.append(deepcopy(hoja))

def registrar_estudiante():
    print("\n--- REGISTRAR NUEVO ESTUDIANTE ---")
    codigo = input("Codigo unico: ").strip()
    
    if codigo in indice_hash:
        print("[ERROR] Llave primaria duplicada. El codigo ya existe.")
        return
    
    nombre = input("Apellidos y Nombres: ").strip()
    
    try:
        nota1 = float(input("Nota 1 (0-20): "))
        nota2 = float(input("Nota 2 (0-20): "))
        nota3 = float(input("Nota 3 (0-20): "))
    except ValueError:
        print("[ERROR] Valores numericos incorrectos en calificaciones.")
        return
    
    # VALIDACIÓN DE NOTAS (AGREGADO)
    if not (0 <= nota1 <= 20 and 0 <= nota2 <= 20 and 0 <= nota3 <= 20):
        print("[ERROR] Las notas deben estar entre 0 y 20")
        return
    
    estudiante = {
        "codigo": codigo,
        "nombre": nombre,
        "nota1": nota1,
        "nota2": nota2,
        "nota3": nota3,
        "promedio": round(calcular_promedio(nota1, nota2, nota3), 2)
    }
    
    guardar_historial()
    hoja.append(estudiante)
    actualizar_hash()
    print("[EXITO] Estudiante registrado e indexado en la estructura asociativa.")

def mostrar_hoja():
    if not hoja:
        print("\n[AVISO] La hoja de calculo no contiene registros activos.")
        return
    
    print("\n" + "="*70)
    print(f"{'MINI HOJA DE CALCULO ACADEMICA':^70}")
    print("="*70)
    print(f"{'Codigo':<12}{'Nombre Completo':<25}{'N1':<8}{'N2':<8}{'N3':<8}{'Promedio':<10}")
    print("-"*70)
    for e in hoja:
        print(f"{e['codigo']:<12}{e['nombre']:<25}{e['nota1']:<8.1f}{e['nota2']:<8.1f}{e['nota3']:<8.1f}{e['promedio']:<10.2f}")
    print("="*70)

def buscar_estudiante():
    codigo = input("\nIngrese codigo a buscar en la estructura asociativa: ").strip()
    if codigo in indice_hash:
        pos = indice_hash[codigo]
        e = hoja[pos]
        print(f"\n[ENCONTRADO O(1)] {e['nombre']} | Promedio Evaluado: {e['promedio']:.2f}")
    else:
        print("[AVISO] El codigo buscado no existe en la base indexada.")

def quicksort(lista):
    if len(lista) <= 1:
        return lista
    pivote = lista[-1]
    mayores = [x for x in lista[:-1] if x["promedio"] >= pivote["promedio"]]
    menores = [x for x in lista[:-1] if x["promedio"] < pivote["promedio"]]
    return quicksort(mayores) + [pivote] + quicksort(menores)

def merge_sort(lista):
    if len(lista) <= 1:
        return lista
    medio = len(lista) // 2
    izquierda = merge_sort(lista[:medio])
    derecha = merge_sort(lista[medio:])
    return merge(izquierda, derecha)

def merge(izquierda, derecha):
    resultado = []
    i = j = 0
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i]["codigo"] <= derecha[j]["codigo"]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado

def ordenar_por_promedio():
    global hoja
    if not hoja: 
        print("[AVISO] No hay datos para ordenar")
        return
    guardar_historial()
    hoja = quicksort(hoja)
    actualizar_hash()
    print("[OK] Matriz ordenada por Promedio via QuickSort Funcional.")

def ordenar_por_codigo():
    global hoja
    if not hoja: 
        print("[AVISO] No hay datos para ordenar")
        return
    guardar_historial()
    hoja = merge_sort(hoja)
    actualizar_hash()
    print("[OK] Matriz ordenada por Codigo via MergeSort Estable.")

def deshacer():
    global hoja
    if historial:
        hoja = historial.pop()
        actualizar_hash()
        print("[REVERSION] Estado de memoria restaurado a la version previa.")
    else:
        print("[INFO] El historial de modificaciones esta vacio.")

def agregar_cola_atencion():
    codigo = input("\nIngrese codigo del estudiante en espera: ").strip()
    if codigo in indice_hash:
        cola_atencion.append(codigo)
        print("[COLA] Estudiante insertado en la cola FIFO institucional.")
    else:
        print("[ERROR] Codigo no registrado en las celdas vigentes.")

def atender_estudiante():
    if cola_atencion:
        codigo = cola_atencion.popleft()
        pos = indice_hash[codigo]
        print(f"[ATENCION] Despachando requerimiento de: {hoja[pos]['nombre']}")
    else:
        print("[INFO] No se registran estudiantes pendientes en la cola.")

def suma_promedios_recursiva(i):
    if i == len(hoja):
        return 0.0
    return hoja[i]["promedio"] + suma_promedios_recursiva(i + 1)

def estadisticas():
    if not hoja:
        print("[AVISO] Datos insuficientes para el analisis.")
        return
    
    suma = suma_promedios_recursiva(0)
    promedio_general = suma / len(hoja)
    
    # NOTA MÁXIMA Y MÍNIMA (AGREGADO)
    notas = [e["promedio"] for e in hoja]
    nota_maxima = max(notas)
    nota_minima = min(notas)
    
    print("\n" + "="*40)
    print(f" Estudiantes Registrados : {len(hoja)}")
    print(f" Promedio General Cohorte: {promedio_general:.2f}")
    print(f" Nota Máxima             : {nota_maxima:.2f}")
    print(f" Nota Mínima             : {nota_minima:.2f}")
    print("="*40)

def menu():
    while True:
        print("\n" + "="*45)
        print(" MENU PRINCIPAL - PYTHON CORE SYSTEMS ")
        print("="*45)
        print("1. Registrar estudiante (Fila)")
        print("2. Mostrar hoja de calculo")
        print("3. Buscar estudiante por codigo (Hash)")
        print("4. Ordenar por promedio (QuickSort)")
        print("5. Ordenar por codigo (MergeSort)")
        print("6. Deshacer ultima accion (Stack)")
        print("7. Agregar a cola de espera (Queue)")
        print("8. Atender siguiente estudiante (FIFO)")
        print("9. Analitica y Estadisticas generales")
        print("10. Salir del programa")
        print("-" * 45)
        
        opcion = input("Seleccione una opcion (1-10): ").strip()
        
        if opcion == "1": registrar_estudiante()
        elif opcion == "2": mostrar_hoja()
        elif opcion == "3": buscar_estudiante()
        elif opcion == "4": ordenar_por_promedio()
        elif opcion == "5": ordenar_por_codigo()
        elif opcion == "6": deshacer()
        elif opcion == "7": agregar_cola_atencion()
        elif opcion == "8": atender_estudiante()
        elif opcion == "9": estadisticas()
        elif opcion == "10":
            print("Finalizando subprocesos interpretados... Salida.")
            break
        else:
            print("[ERROR] Codigo numerico no asignado en el menu.")

if __name__ == "__main__":
    menu()