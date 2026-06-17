"""
Bucket Sort con generador para animación paso a paso.
Distribuye elementos en cubetas (buckets) y ordena cada cubeta individualmente.
Ideal para datos con distribución uniforme.
"""

def bucket_sort_generator(arr, num_buckets=5):
    """
    Generador que produce el estado del array durante el ordenamiento Bucket Sort.
    
    Bucket Sort funciona así:
    1. Encuentra el valor mínimo y máximo
    2. Distribuye los elementos en cubetas (buckets)
    3. Ordena cada cubeta individualmente (usando Insertion Sort para simplicidad)
    4. Concatena todas las cubetas
    
    Args:
        arr: Lista de números a ordenar (se modifica in-place)
        num_buckets: Número de cubetas a usar (por defecto 5)
    
    Yields:
        tuple: (lista_actual, idx_actual, valor_actual, operacion, datos_extra)
    """
    lista = arr.copy()
    n = len(lista)
    
    if n == 0:
        yield lista, -1, -1, "finished", None
        return
    
    # Paso 1: Encontrar mínimo y máximo
    min_val = min(lista)
    max_val = max(lista)
    rango = max_val - min_val
    
    yield lista, -1, -1, "finding_range", {"min": min_val, "max": max_val, "rango": rango, "num_buckets": num_buckets}
    
    if rango == 0:
        # Todos los elementos son iguales, ya está ordenado
        yield lista, -1, -1, "all_equal", None
        yield lista, -1, -1, "finished", None
        return
    
    # Paso 2: Crear cubetas (buckets)
    buckets = [[] for _ in range(num_buckets)]
    yield lista, -1, -1, "creating_buckets", {"num_buckets": num_buckets, "buckets": [b.copy() for b in buckets]}
    
    # Paso 3: Distribuir elementos en cubetas
    for i, valor in enumerate(lista):
        # Calcular índice de cubeta
        bucket_idx = int((valor - min_val) / rango * (num_buckets - 1))
        bucket_idx = min(bucket_idx, num_buckets - 1)  # Asegurar que no se salga del rango
        buckets[bucket_idx].append(valor)
        
        yield lista, i, valor, "distributing", {
            "bucket_idx": bucket_idx,
            "valor": valor,
            "buckets": [b.copy() for b in buckets],
            "rangos": [(min_val + (rango * idx / num_buckets), 
                       min_val + (rango * (idx + 1) / num_buckets)) for idx in range(num_buckets)]
        }
    
    yield lista, -1, -1, "distribution_done", {"buckets": [b.copy() for b in buckets]}
    
    # Paso 4: Ordenar cada cubeta individualmente (usando Insertion Sort para mostrar)
    for idx_bucket, bucket in enumerate(buckets):
        if len(bucket) > 0:
            yield lista, -1, idx_bucket, "sorting_bucket", {
                "bucket_idx": idx_bucket,
                "bucket": bucket.copy(),
                "buckets": [b.copy() for b in buckets]
            }
            
            # Mostrar Insertion Sort dentro de la cubeta (versión simplificada)
            for i in range(1, len(bucket)):
                key = bucket[i]
                j = i - 1
                
                # Mostrar que estamos ordenando
                yield lista, -1, idx_bucket, "bucket_comparing", {
                    "bucket_idx": idx_bucket,
                    "i": i, "j": j,
                    "key": key,
                    "bucket": bucket.copy(),
                    "buckets": [b.copy() for b in buckets]
                }
                
                while j >= 0 and bucket[j] > key:
                    bucket[j + 1] = bucket[j]
                    j -= 1
                    
                    yield lista, -1, idx_bucket, "bucket_shifting", {
                        "bucket_idx": idx_bucket,
                        "i": i, "j": j + 1,
                        "bucket": bucket.copy(),
                        "buckets": [b.copy() for b in buckets]
                    }
                
                bucket[j + 1] = key
                
                yield lista, -1, idx_bucket, "bucket_inserted", {
                    "bucket_idx": idx_bucket,
                    "pos": j + 1,
                    "key": key,
                    "bucket": bucket.copy(),
                    "buckets": [b.copy() for b in buckets]
                }
            
            yield lista, -1, idx_bucket, "bucket_sorted", {
                "bucket_idx": idx_bucket,
                "bucket": bucket.copy(),
                "buckets": [b.copy() for b in buckets]
            }
    
    yield lista, -1, -1, "buckets_sorted", {"buckets": [b.copy() for b in buckets]}
    
    # Paso 5: Concatenar todas las cubetas
    ordenado = []
    for idx_bucket, bucket in enumerate(buckets):
        ordenado.extend(bucket)
        yield lista, -1, idx_bucket, "concatenating", {
            "bucket_idx": idx_bucket,
            "bucket": bucket,
            "concatenado": ordenado.copy(),
            "buckets": [b.copy() for b in buckets]
        }
    
    # Paso 6: Copiar de vuelta a la lista original
    for i in range(n):
        lista[i] = ordenado[i]
        yield lista, i, ordenado[i], "copying", {"progress": i + 1, "total": n}
    
    # Estado final
    yield lista, -1, -1, "finished", None