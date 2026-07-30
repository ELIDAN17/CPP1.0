import pygame

async def busqueda_lineal(arr, x, draw_func):
    for i in range(len(arr)):
        await draw_func(arr, {i: (255, 149, 0)}, f"Lineal: ¿Indice [{i}] (Valor {arr[i]}) == {x}?")
        if arr[i] == x: return i
    return -1

async def busqueda_binaria(arr, x, draw_func):
    l, r = 0, len(arr) - 1
    while l <= r:
        m = l + (r - l) // 2
        await draw_func(arr, {m: (255, 149, 0), l: (255, 255, 0), r: (255, 255, 0)}, 
                  f"Binaria: m={m} (Val:{arr[m]}). Rango actual: [{l} a {r}]")
        if arr[m] == x: return m
        if arr[m] < x: l = m + 1
        else: r = m - 1
    return -1

async def busqueda_interpolacion(arr, x, draw_func):
    low, high = 0, len(arr) - 1
    while low <= high and x >= arr[low] and x <= arr[high]:
        if low == high: return low if arr[low] == x else -1
        pos = low + int(((float(high - low) / (arr[high] - arr[low])) * (x - arr[low])))
        await draw_func(arr, {pos: (255, 149, 0), low: (255, 255, 0), high: (255, 255, 0)}, 
                  f"Interp: Estimando posicion pos={pos} (Val:{arr[pos]})")
        if arr[pos] == x: return pos
        if arr[pos] < x: low = pos + 1
        else: high = pos - 1
    return -1

async def busqueda_exponencial(arr, x, draw_func):
    if not arr: return -1
    if arr[0] == x: return 0
    n, i = len(arr), 1
    while i < n and arr[i] < x:
        await draw_func(arr, {i: (255, 255, 0)}, f"Exponencial: Saltando al indice {i}...")
        i <<= 1
    l, r = i // 2, min(i, n - 1)
    return await busqueda_binaria_rango(arr, x, l, r, draw_func)

async def busqueda_binaria_rango(arr, x, l, r, draw_func):
    while l <= r:
        m = l + (r - l) // 2
        await draw_func(arr, {m: (255, 149, 0), l: (255, 255, 0), r: (255, 255, 0)}, f"Fase Binaria: m={m}")
        if arr[m] == x: return m
        if arr[m] < x: l = m + 1
        else: r = m - 1
    return -1