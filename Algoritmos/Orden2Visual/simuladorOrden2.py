# -*- coding: utf-8 -*-
import pandas as pd

# --- 1. ALGORITMOS NO COMPARATIVOS (SEMANA 4) ---
def counting_sort(arr):
    if not arr: return arr
    max_val, min_val = int(max(arr)), int(min(arr))
    range_elements = max_val - min_val + 1
    count = [0] * range_elements
    output = [0] * len(arr)
    for i in arr: count[int(i) - min_val] += 1
    for i in range(1, len(count)): count[i] += count[i-1]
    for i in range(len(arr) - 1, -1, -1):
        output[count[int(arr[i]) - min_val] - 1] = arr[i]
        count[int(arr[i]) - min_val] -= 1
    return output

def radix_sort(arr):
    if not arr: return arr
    def counting_for_radix(a, exp):
        n = len(a)
        out, count = [0] * n, [0] * 10
        for i in range(n):
            index = int((a[i] // exp) % 10)
            count[index] += 1
        for i in range(1, 10): count[i] += count[i-1]
        for i in range(n - 1, -1, -1):
            index = int((a[i] // exp) % 10)
            out[count[index] - 1] = a[i]
            count[index] -= 1
        return out
    max_v = int(max(arr))
    exp, res = 1, list(arr)
    while max_v // exp > 0:
        res = counting_for_radix(res, exp)
        exp *= 10
    return res

def bucket_sort(arr):
    if not arr: return arr
    n, max_v = len(arr), max(arr)
    buckets = [[] for _ in range(n)]
    for x in arr:
        idx = int(n * x / (max_v + 1))
        buckets[idx].append(x)
    for b in buckets: b.sort()
    return [item for b in buckets for item in b]

# --- 2. ALGORITMOS COMPARATIVOS ---
def quick_sort(arr):
    if len(arr) <= 1: return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left, right = merge_sort(arr[:mid]), merge_sort(arr[mid:])
    res, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]: res.append(left[i]); i += 1
        else: res.append(right[j]); j += 1
    res.extend(left[i:]); res.extend(right[j:])
    return res

def shell_sort(arr):
    res = list(arr)
    n, gap = len(res), len(res) // 2
    while gap > 0:
        for i in range(gap, n):
            temp, j = res[i], i
            while j >= gap and res[j - gap] > temp:
                res[j] = res[j - gap]
                j -= gap
            res[j] = temp
        gap //= 2
    return res

# --- 3. IMPLEMENTACIÓN MANUAL DE TIMSORT (Híbrido) ---
MIN_MERGE = 32

def calc_min_run(n):
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r

def insertion_sort_timsort(arr, left, right):
    for i in range(left + 1, right + 1):
        temp, j = arr[i], i - 1
        while j >= left and arr[j] > temp:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = temp

def merge_timsort(arr, l, m, r):
    len1, len2 = m - l + 1, r - m
    left = [arr[l + i] for i in range(len1)]
    right = [arr[m + 1 + i] for i in range(len2)]
    i, j, k = 0, 0, l
    while i < len1 and j < len2:
        if left[i] <= right[j]: arr[k] = left[i]; i += 1
        else: arr[k] = right[j]; j += 1
        k += 1
    while i < len1: arr[k] = left[i]; k += 1; i += 1
    while j < len2: arr[k] = right[j]; k += 1; j += 1

def timsort_manual(arr_original):
    """
    Timsort Manual: Combina Insertion Sort (para bloques pequeños) 
    con Merge Sort (para combinar bloques ordenados).
    """
    arr = list(arr_original)
    n = len(arr)
    min_run = calc_min_run(n)

    # 1. Crear y ordenar 'runs' (bloques) usando Inserción
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion_sort_timsort(arr, start, end)

    # 2. Mezclar los bloques ordenados usando Merge Sort
    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
            if mid < right:
                merge_timsort(arr, left, mid, right)
        size *= 2
    return arr

# --- 4. CSV ---
def cargar_datos_csv(archivo, columna):
    try:
        df = pd.read_csv(archivo)
        return df[columna].dropna().tolist() if columna in df.columns else None
    except Exception as e:
        print(f"Error: {e}")
        return None