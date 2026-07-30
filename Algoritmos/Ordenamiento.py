import time
import random
import sys
sys.setrecursionlimit(10000)

# ------------------------- BUBBLE SORT -------------------------
def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

# ------------------------- INSERTION SORT -------------------------
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# ------------------------- MERGE SORT -------------------------
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# ------------------------- QUICK SORT -------------------------
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[-1]
    left = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x > pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)

# ------------------------- FUNCIÓN PARA MEDIR TIEMPO -------------------------
def medir_tiempo(func, arr, nombre):
    inicio = time.time()
    if nombre == "Merge" or nombre == "Quick":
        resultado = func(arr.copy())
    else:
        arr_copy = arr.copy()
        func(arr_copy)
        resultado = arr_copy
    fin = time.time()
    return (fin - inicio) * 1000  # milisegundos

# ------------------------- GENERAR DATOS -------------------------
def generar_aleatorio(n):
    return [random.randint(1, 10000) for _ in range(n)]

def generar_ordenado(n):
    return list(range(1, n + 1))

def generar_inverso(n):
    return list(range(n, 0, -1))

# ------------------------- MENÚ PRINCIPAL -------------------------
def main():
    print("\n" + "=" * 50)
    print("   ANÁLISIS DE ALGORITMOS DE ORDENAMIENTO (PYTHON)")
    print("=" * 50)
    
    tamanos = [1000, 5000, 10000]
    
    for n in tamanos:
        print(f"\n🔹 TAMAÑO: {n} elementos")
        print("-" * 40)
        
        aleatorio = generar_aleatorio(n)
        ordenado = generar_ordenado(n)
        inverso = generar_inverso(n)
        
        # Bubble Sort (solo para 1000)
        if n == 1000:
            print("Bubble Sort:")
            print(f"  Aleatoria: {medir_tiempo(bubble_sort, aleatorio, 'Bubble'):.2f} ms")
            print(f"  Ordenada: {medir_tiempo(bubble_sort, ordenado, 'Bubble'):.2f} ms")
            print(f"  Inversa: {medir_tiempo(bubble_sort, inverso, 'Bubble'):.2f} ms")
        else:
            print("Bubble Sort: [DEMASIADO LENTO, no se ejecutó]")
        
        # Insertion Sort
        print("Insertion Sort:")
        print(f"  Aleatoria: {medir_tiempo(insertion_sort, aleatorio, 'Insertion'):.2f} ms")
        print(f"  Ordenada: {medir_tiempo(insertion_sort, ordenado, 'Insertion'):.2f} ms")
        print(f"  Inversa: {medir_tiempo(insertion_sort, inverso, 'Insertion'):.2f} ms")
        
        # Merge Sort
        print("Merge Sort:")
        print(f"  Aleatoria: {medir_tiempo(merge_sort, aleatorio, 'Merge'):.2f} ms")
        print(f"  Ordenada: {medir_tiempo(merge_sort, ordenado, 'Merge'):.2f} ms")
        print(f"  Inversa: {medir_tiempo(merge_sort, inverso, 'Merge'):.2f} ms")
        
        # Quick Sort
        print("Quick Sort:")
        print(f"  Aleatoria: {medir_tiempo(quick_sort, aleatorio, 'Quick'):.2f} ms")
        print(f"  Ordenada: {medir_tiempo(quick_sort, ordenado, 'Quick'):.2f} ms")
        print(f"  Inversa: {medir_tiempo(quick_sort, inverso, 'Quick'):.2f} ms")

if __name__ == "__main__":
    main()