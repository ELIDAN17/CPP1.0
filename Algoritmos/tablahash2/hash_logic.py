# -*- coding: utf-8 -*-
import pandas as pd
import time

class HashTableBase:
    def __init__(self, size):
        self.size = size
        self.collisions = 0
        self.elements = 0
    
    def hash_polinomial(self, key):
        """Función hash manual para cadenas (p=31) sugerida para nivel avanzado."""
        h = 0
        for char in str(key):
            h = (h * 31 + ord(char)) % self.size
        return h

    def load_factor(self):
        return self.elements / self.size

class HashTableChaining(HashTableBase):
    def __init__(self, size):
        super().__init__(size)
        self.table = [[] for _ in range(size)]

    def insert(self, key, value):
        if self.elements >= self.size*0.9: return False
        idx = self.hash_polinomial(key)
        if self.table[idx]: self.collisions += 1
        self.table[idx].append((key, value))
        self.elements += 1

    def search(self, key):
        idx = self.hash_polinomial(key)
        for k, v in self.table[idx]:
            if k == key: return v
        return None

class HashTableLinearProbing(HashTableBase):
    def __init__(self, size):
        super().__init__(size)
        self.table = [None] * size

    def insert(self, key, value):
        if self.elements >= self.size*0.9: return False
        idx = self.hash_polinomial(key)
        while self.table[idx] is not None:
            self.collisions += 1
            idx = (idx + 1) % self.size
        self.table[idx] = (key, value)
        self.elements += 1

    def search(self, key):
        idx = self.hash_polinomial(key)
        start = idx
        while self.table[idx] is not None:
            if self.table[idx][0] == key: return self.table[idx][1]
            idx = (idx + 1) % self.size
            if idx == start: break
        return None

class HashTableDoubleHash(HashTableBase):
    def __init__(self, size):
        super().__init__(size)
        self.table = [None] * size
        # Primo menor a size para h2(k)
        self.prime = 10007 

    def hash2(self, key):
        return self.prime - (hash(str(key)) % self.prime)

    def insert(self, key, value):
        if self.elements >= self.size*0.9: return False
        idx = self.hash_polinomial(key)
        if self.table[idx] is not None:
            step = self.hash2(key)
            while self.table[idx] is not None:
                self.collisions += 1
                idx = (idx + step) % self.size
        self.table[idx] = (key, value)
        self.elements += 1

    def search(self, key):
        idx = self.hash_polinomial(key)
        step = self.hash2(key)
        start = idx
        while self.table[idx] is not None:
            if self.table[idx][0] == key: return self.table[idx][1]
            idx = (idx + step) % self.size
            if idx == start: break
        return None


""""
import pandas as pd
import time
import matplotlib.pyplot as plt

# --- 1. ENCADENAMIENTO SEPARADO ---
class HashTableChaining:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.collisions = 0

    def hash_function(self, key):
        return hash(str(key)) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        if len(self.table[index]) > 0:
            self.collisions += 1
        self.table[index].append((key, value))

    def search(self, key):
        index = self.hash_function(key)
        for k, v in self.table[index]:
            if k == key: return v
        return None

    def load_factor(self, n):
        return n / self.size

# --- 2. SONDEO LINEAL ---
class HashTableLinearProbing:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.collisions = 0

    def hash_function(self, key):
        return hash(str(key)) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        while self.table[index] is not None:
            self.collisions += 1
            index = (index + 1) % self.size
        self.table[index] = (key, value)

    def search(self, key):
        index = self.hash_function(key)
        start = index
        while self.table[index] is not None:
            if self.table[index][0] == key: return self.table[index][1]
            index = (index + 1) % self.size
            if index == start: break
        return None

# --- 3. DOBLE HASHING (REQUERIDO POR EL PDF) ---
class HashTableDoubleHash:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.collisions = 0
        # Primo menor al tamaño de la tabla para la segunda función
        self.prime = 10007 

    def hash1(self, key):
        return hash(str(key)) % self.size

    def hash2(self, key):
        return self.prime - (hash(str(key)) % self.prime)

    def insert(self, key, value):
        index = self.hash1(key)
        if self.table[index] is not None:
            step = self.hash2(key)
            while self.table[index] is not None:
                self.collisions += 1
                index = (index + step) % self.size
        self.table[index] = (key, value)

    def search(self, key):
        index = self.hash1(key)
        step = self.hash2(key)
        start = index
        while self.table[index] is not None:
            if self.table[index][0] == key: return self.table[index][1]
            index = (index + step) % self.size
            if index == start: break
        return None

# --- EJECUCIÓN DEL EXPERIMENTO ---

# 1. Cargar Datos
try:
    df = pd.read_csv("ecommerce_sample.csv").dropna()
    # Usamos product_id o user_id según disponibilidad
    col_name = "user_id" if "user_id" in df.columns else df.columns[0]
    keys = df[col_name].astype(str).head(10000).tolist()
except FileNotFoundError:
    print("Error: No se encontró el archivo CSV.")
    keys = []

if keys:
    table_size = 20011
    results_list = []

    # Diccionario de modelos para iterar
    modelos = {
        "Encadenamiento": HashTableChaining(table_size),
        "Sondeo Lineal": HashTableLinearProbing(table_size),
        "Doble Hashing": HashTableDoubleHash(table_size),
        "Dict Nativo": dict()
    }

    for nombre, objeto in modelos.items():
        # Medir Inserción
        t0 = time.time()
        for k in keys:
            if nombre == "Dict Nativo": objeto[k] = k
            else: objeto.insert(k, k)
        t_ins = time.time() - t0

        # Medir Búsqueda (1000 elementos)
        t0 = time.time()
        for k in keys[:1000]:
            if nombre == "Dict Nativo": _ = objeto.get(k)
            else: _ = objeto.search(k)
        t_bus = time.time() - t0

        # Guardar resultados
        cols = objeto.collisions if nombre != "Dict Nativo" else 0
        results_list.append({
            "Metodo": nombre,
            "Insercion (s)": t_ins,
            "Busqueda (s)": t_bus,
            "Colisiones": cols,
            "Factor Carga": len(keys)/table_size
        })

    # Mostrar Tabla
    df_res = pd.DataFrame(results_list)
    print(df_res)

    # Graficar
    df_res.set_index("Metodo")[["Insercion (s)", "Busqueda (s)"]].plot(kind="bar", figsize=(10,5))
    plt.title("Rendimiento de Estructuras Hash")
    plt.ylabel("Segundos")
    plt.show() 
    """