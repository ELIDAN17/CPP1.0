"""
Radix Sort con generador para animación paso a paso.
Ordena dígito por dígito usando Counting Sort como subrutina.
Es ideal para números enteros positivos.
"""

def radix_sort_generator(arr):
    """
    Generador que produce el estado del array durante el ordenamiento Radix Sort.
    
    Radix Sort funciona así:
    1. Encuentra el número máximo para saber cuántos dígitos tiene
    2. Para cada dígito (unidades, decenas, centenas...):
       a. Aplica Counting Sort basado en ese dígito
       b. Muestra el estado después de cada pasada
    
    Args:
        arr: Lista de números a ordenar (se modifica in-place)
    
    Yields:
        tuple: (lista_actual, idx_actual, digito_actual, operacion, datos_extra)
    """
    lista = arr.copy()
    n = len(lista)
    
    if n == 0:
        yield lista, -1, -1, "finished", None
        return
    
    # Asegurar que todos los números son no negativos para este ejemplo
    # (Se puede extender para negativos)
    if any(x < 0 for x in lista):
        yield lista, -1, -1, "error_negative", None
        return
    
    # Paso 1: Encontrar el número máximo
    max_val = max(lista)
    yield lista, -1, max_val, "finding_max", {"max": max_val}
    
    # Paso 2: Determinar número de dígitos
    num_digitos = len(str(max_val))
    yield lista, -1, num_digitos, "digits_count", {"digitos": num_digitos}
    
    # Paso 3: Procesar cada dígito
    for digito_pos in range(num_digitos):
        # Mostrar qué dígito estamos procesando
        yield lista, -1, digito_pos, "processing_digit", {"digito": digito_pos, "valor_posicional": 10 ** digito_pos}
        
        # Counting Sort para este dígito
        # Crear arreglo de salida
        salida = [0] * n
        # Arreglo de frecuencias para dígitos 0-9
        conteo = [0] * 10
        
        # Paso 3a: Contar frecuencias de cada dígito
        for i, valor in enumerate(lista):
            digito = (valor // (10 ** digito_pos)) % 10
            conteo[digito] += 1
            yield lista, i, digito, "counting_digit", {
                "digito_pos": digito_pos,
                "valor": valor,
                "digito_actual": digito,
                "conteo_parcial": conteo.copy()
            }
        
        yield lista, -1, -1, "counts_done", {"conteo": conteo.copy(), "digito_pos": digito_pos}
        
        # Paso 3b: Convertir conteo a posiciones acumuladas
        for i in range(1, 10):
            conteo[i] += conteo[i - 1]
        
        yield lista, -1, -1, "cumulative", {"conteo_acum": conteo.copy(), "digito_pos": digito_pos}
        
        # Paso 3c: Construir arreglo de salida (de atrás a adelante para estabilidad)
        for i in range(n - 1, -1, -1):
            valor = lista[i]
            digito = (valor // (10 ** digito_pos)) % 10
            pos = conteo[digito] - 1
            salida[pos] = valor
            conteo[digito] -= 1
            yield lista, i, valor, "placing", {
                "digito_pos": digito_pos,
                "digito": digito,
                "posicion": pos,
                "salida_parcial": salida.copy()
            }
        
        # Paso 3d: Copiar de vuelta a la lista original
        for i in range(n):
            lista[i] = salida[i]
            yield lista, i, salida[i], "copying", {"digito_pos": digito_pos}
        
        # Mostrar resultado después de esta pasada
        yield lista, -1, digito_pos, "pass_complete", {"digito_pos": digito_pos, "lista_parcial": lista.copy()}
    
    # Estado final
    yield lista, -1, -1, "finished", None