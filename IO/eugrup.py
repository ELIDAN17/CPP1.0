import numpy as np
import matplotlib.pyplot as plt

def noroest(c, s, d):
    asignacion = np.zeros_like(c)
    i, j, o, de = 0, 0, s.copy(), d.copy()
    while i < len(o) and j < len(de):
        cant = min(o[i], de[j])
        asignacion[i][j] = cant
        o[i] -= cant; de[j] -= cant
        if o[i] == 0: i += 1
        else: j += 1
    return np.sum(asignacion * c)

def costo_minimo(c, s, d):
    asignacion = np.zeros_like(c)
    o, de, temp_c = s.copy(), d.copy(), c.copy().astype(float)
    while np.any(o > 0) and np.any(de > 0):
        temp_c[o == 0, :] = np.inf
        temp_c[:, de == 0] = np.inf
        if np.all(temp_c == np.inf): break
        idx = np.unravel_index(np.argmin(temp_c), temp_c.shape)
        i, j = idx
        cant = min(o[i], de[j])
        asignacion[i][j] = cant
        o[i] -= cant; de[j] -= cant
        temp_c[i, j] = np.inf
    return np.sum(asignacion * c)

def vogel(c, s, d):
    o, de = s.copy(), d.copy()
    M, N = c.shape
    asignacion = np.zeros((M, N))
    
    # CONVERSIÓN CRÍTICA: Convertimos a arrays de numpy para permitir la indexación
    fila_out = np.zeros(M, dtype=bool)
    col_out = np.zeros(N, dtype=bool)
    
    while np.any(o > 0) and np.any(de > 0):
        # Creamos una máscara de costos donde los inactivos son "infinitos"
        costos_mask = c.copy().astype(float)
        costos_mask[fila_out, :] = np.inf
        costos_mask[:, col_out] = np.inf
        # Ahora sí, buscamos el mínimo con seguridad
        if np.all(costos_mask == np.inf): break
        
        i, j = np.unravel_index(np.argmin(costos_mask), costos_mask.shape)
        
        cant = min(o[i], de[j])
        asignacion[i][j] = cant
        o[i] -= cant
        de[j] -= cant
        
        if o[i] == 0: fila_out[i] = True
        if de[j] == 0: col_out[j] = True
        
    return np.sum(asignacion * c)

def vda(c, s, d):
    M, N = c.shape
    vulnerabilidad = np.sum(c, axis=0)
    orden = np.argsort(vulnerabilidad)[::-1]
    asignacion = np.zeros((M, N))
    o, de, f_out = s.copy(), d.copy(), np.zeros(M, dtype=bool)
    for j in orden:
        filas = np.argsort(c[:, j])
        for i in filas:
            if not f_out[i] and o[i] > 0 and de[j] > 0:
                cant = min(o[i], de[j])
                asignacion[i][j] = cant
                o[i] -= cant; de[j] -= cant
                if o[i] == 0: f_out[i] = True
    return np.sum(asignacion * c)

# --- 2. DATOS (Ejemplos BTP) ---
casos = {
    "BTP-1": {"c": np.array([[4,2,1],[3,8,4],[6,5,2]]), "s": np.array([50,70,45]), "d": np.array([40,65,60])},
    "BTP-2": {"c": np.array([[6,4,1],[3,8,7],[4,4,2]]), "s": np.array([50,40,60]), "d": np.array([20,95,35])},
    "BTP-3": {"c": np.array([[9,8,5,7],[4,6,8,7],[5,8,9,5]]), "s": np.array([12,14,16]), "d": np.array([8,18,13,3])},
    "BTP-4": {"c": np.array([[3,1,7,4],[2,6,5,9],[8,3,3,2]]), "s": np.array([300,400,500]), "d": np.array([250,350,400,200])},
    "BTP-5": {"c": np.array([[7,5,9,11],[4,3,8,6],[3,8,10,5],[2,6,7,3]]), "s": np.array([30,25,20,15]), "d": np.array([30,30,20,10])},
    "BTP-6": {"c": np.array([[50,60,100,50],[80,40,70,50],[90,70,30,50]]), "s": np.array([20,38,16]), "d": np.array([10,18,22,24])},
    "BTP-7": {"c": np.array([[4,3,5],[6,5,4],[8,10,7]]), "s": np.array([90,80,100]), "d": np.array([70,120,80])},
    "BTP-8": {"c": np.array([[5,7,8],[4,4,6],[6,7,7]]), "s": np.array([70,30,50]), "d": np.array([65,42,43])},
    "BTP-9": {"c": np.array([[1,8,6],[3,7,8],[4,9,10]]), "s": np.array([50,45,40]), "d": np.array([35,55,45])},
    "BTP-10": {"c": np.array([[1,2,1,4,5,2],[3,3,2,1,4,3],[4,2,5,9,6,2],[3,1,7,3,4,6]]), "s": np.array([30,50,75,20]), "d": np.array([20,40,30,10,50,25])},
    "BTP-11": {"c": np.array([[12,7,3,8,10,6,6],[6,9,7,12,8,12,4],[10,12,8,4,9,9,3],[8,5,11,6,7,9,3],[7,6,8,11,9,5,6]]), "s": np.array([60,80,70,100,90]), "d": np.array([20,30,40,70,60,80,100])},
    "BTP-12": {"c": np.array([[2,2,2,1],[10,8,5,4],[7,6,6,8]]), "s": np.array([3,7,5]), "d": np.array([4,3,4,4])}
}

# --- 3. PROCESAMIENTO Y GRÁFICO ---
print(f"{'Caso':<10} | {'Noroeste':<10} | {'CostoMin':<10} | {'Vogel':<10} | {'VDA':<10}")
print("-" * 60)
resultados = []
nombres = list(casos.keys())

for n in nombres:
    data = casos[n]
    z_nor = noroest(data['c'], data['s'], data['d'])
    z_min = costo_minimo(data['c'], data['s'], data['d'])
    z_vog = vogel(data['c'], data['s'], data['d'])
    z_vda = vda(data['c'], data['s'], data['d'])
    resultados.append([z_nor, z_min, z_vog, z_vda])
    print(f"{n:<10} | {z_nor:<10} | {z_min:<10} | {z_vog:<10} | {z_vda:<10}")

# Grafico de barras comparativo
res = np.array(resultados)
x = np.arange(len(nombres))
width = 0.2
fig, ax = plt.subplots(figsize=(10, 5))
labels = ['Noroeste', 'Costo Min', 'Vogel', 'VDA']
for i in range(4):
    ax.bar(x + (i-1.5)*width, res[:, i], width, label=labels[i])

ax.set_title("Comparativa de Costo Total (Z) por Heurística")
ax.set_ylabel("Costo Total (Z)")
ax.set_xticks(x)
ax.set_xticklabels(nombres)
ax.legend()
plt.show()