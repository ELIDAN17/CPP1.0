import asyncio

# Colores
NARANJA = (230, 126, 34)
VERDE = (46, 204, 113)
AZUL = (52, 152, 219)

async def bubble_sort(arr, draw_func, stats, key, reverse=False):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            stats['comp'] += 1
            # Lógica de comparación dinámica
            condition = arr[j][key] < arr[j+1][key] if reverse else arr[j][key] > arr[j+1][key]
            if condition:
                stats['swap'] += 1
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                await draw_func(arr, {j: NARANJA, j+1: NARANJA}, f"Burbuja: Ordenando {key}")
    await draw_func(arr, {k: VERDE for k in range(n)}, "¡Completado!")

async def selection_sort(arr, draw_func, stats, key, reverse=False):
    n = len(arr)
    for i in range(n):
        idx_extremo = i
        for j in range(i + 1, n):
            stats['comp'] += 1
            condition = arr[j][key] > arr[idx_extremo][key] if reverse else arr[j][key] < arr[idx_extremo][key]
            if condition:
                idx_extremo = j
            await draw_func(arr, {i: VERDE, j: NARANJA, idx_extremo: NARANJA}, f"Selección: Ordenando {key}")
        stats['swap'] += 1
        arr[i], arr[idx_extremo] = arr[idx_extremo], arr[i]
    await draw_func(arr, {k: VERDE for k in range(n)}, "¡Completado!")

async def insertion_sort(arr, draw_func, stats, key, reverse=False):
    for i in range(1, len(arr)):
        val_actual = arr[i]
        j = i - 1
        while j >= 0:
            stats['comp'] += 1
            condition = arr[j][key] < val_actual[key] if reverse else arr[j][key] > val_actual[key]
            if condition:
                stats['swap'] += 1
                arr[j + 1] = arr[j]
                j -= 1
                await draw_func(arr, {j+1: NARANJA, i: AZUL}, f"Inserción: Ordenando {key}")
            else:
                break
        arr[j + 1] = val_actual
    await draw_func(arr, {k: VERDE for k in range(len(arr))}, "¡Inserción Completada!")

async def shell_sort(arr, draw_func, stats, key, reverse=False):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap:
                stats['comp'] += 1
                condition = arr[j - gap][key] < temp[key] if reverse else arr[j - gap][key] > temp[key]
                if condition:
                    stats['swap'] += 1
                    arr[j] = arr[j - gap]
                    j -= gap
                    await draw_func(arr, {j: NARANJA, j+gap: NARANJA}, f"Shell Sort: Gap {gap}")
                else:
                    break
            arr[j] = temp
        gap //= 2
    await draw_func(arr, {k: VERDE for k in range(n)}, "¡Shell Sort Completado!")