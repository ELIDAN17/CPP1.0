from collections import defaultdict, deque
import numpy as np
import sys

class GrafoPuno:
    CIUDADES = {0:'Puno',1:'Juliaca',2:'Ilave',3:'Desaguadero',4:'Yunguyo',
    5:'Juli',6:'Lampa',7:'Azangaro',8:'Huancane',9:'Moho',
    10:'Putina',11:'Ayaviri',12:'Macusani',13:'Sandia'}
    RIESGO = {0:'bajo',1:'bajo',2:'bajo',3:'bajo',4:'medio',5:'bajo',
    6:'medio',7:'medio',8:'alto',9:'alto',10:'alto',
    11:'medio',12:'alto',13:'alto'}
    def __init__(self, n):
        self.n = n
        self.adj = defaultdict(list)
        self.naristas = 0
    def agregar_arista(self, u, v, peso):
        self.adj[u].append((v, peso))
        self.adj[v].append((u, peso))
        self.naristas += 1
    def grado(self, u): return len(self.adj[u])
    def densidad(self): return 2*self.naristas / (self.n*(self.n-1))

g = GrafoPuno(14)
rutas = [
    (0,1,44),(0,2,55),(0,5,80),(1,6,37),(1,7,70),(1,11,90),
    (2,3,50),(2,4,45),(3,4,25),(5,4,60),(7,8,95),(7,10,110),
    (7,11,75),(8,9,40),(11,12,140),(11,13,180),
]
for u,v,p in rutas: g.agregar_arista(u,v,p)
print("=== ACTIVIDAD 1 ===")
print(f'|V|={g.n} |E|={g.naristas} densidad={g.densidad():.3f}')
for c in range(g.n):
    print(f' {g.CIUDADES[c]:15} grado={g.grado(c)}')

print()
print("=== ACTIVIDAD 2 ===")
def construir_matriz(g):
    M = np.full((g.n, g.n), np.inf)
    np.fill_diagonal(M, 0)
    for u in g.adj:
        for v, peso in g.adj[u]:
            M[u][v] = peso
    return M

matriz = construir_matriz(g)
print('Matriz de adyacencia (km, inf = sin ruta directa):')
np.set_printoptions(linewidth=200, precision=0, suppress=True)
print(matriz)

tam_lista = sys.getsizeof(g.adj) + sum(sys.getsizeof(v) for v in g.adj.values())
tam_matriz = matriz.nbytes
print(f'Memoria lista de adyacencia: {tam_lista} bytes')
print(f'Memoria matriz de adyacencia: {tam_matriz} bytes')
print(f'Razon matriz/lista: {tam_matriz/tam_lista:.1f}x')

print()
print("=== ACTIVIDAD 3 ===")
class GrafoDirigidoPuno:
    def __init__(self, n):
        self.n = n; self.adj = defaultdict(list)
    def agregar_arista_dirigida(self, u, v, peso):
        self.adj[u].append((v, peso))
    def es_alcanzable(self, origen, destino):
        visitados = set()
        def dfs(u):
            if u == destino: return True
            visitados.add(u)
            return any(dfs(v) for v,_ in self.adj[u] if v not in visitados)
        return dfs(origen)

gd = GrafoDirigidoPuno(6)
restricciones_candelaria = [
    (0,1,'solo bajada hacia el malecon'),
    (1,5,'flujo unico hacia el lago durante el corso'),
    (2,0,'acceso unico a la plaza desde Av. El Sol'),
    (3,2,'desvio obligatorio'),
    (4,3,'sentido unico zona comercial'),
]
for u,v,_ in restricciones_candelaria: gd.agregar_arista_dirigida(u,v,1)
print('Se puede ir del Jr. Tacna (4) a la Plaza de Armas (0)?', gd.es_alcanzable(4,0))
print('Se puede ir de la Plaza de Armas (0) al Jr. Tacna (4)?', gd.es_alcanzable(0,4))

print()
print("=== ACTIVIDAD 4 ===")
def componentes_conexas(g, vertices_excluidos=None):
    excluidos = vertices_excluidos or set()
    visitados = set(excluidos)
    componentes = []
    for inicio in range(g.n):
        if inicio in visitados: continue
        componente = []
        cola = deque([inicio]); visitados.add(inicio)
        while cola:
            u = cola.popleft(); componente.append(u)
            for v,_ in g.adj[u]:
                if v not in visitados and v not in excluidos:
                    visitados.add(v); cola.append(v)
        componentes.append(componente)
    return componentes

print('=== Red vial COMPLETA (sin lluvias) ===')
comp_normal = componentes_conexas(g)
print(f'Componentes conexas: {len(comp_normal)}')
for c in comp_normal:
    print(f' {[g.CIUDADES[v] for v in c]}')
print()
print('=== Simulacion: trochas de Macusani(12) y Sandia(13) bloqueadas ===')
ciudades_aisladas = {12, 13}
comp_lluvia = componentes_conexas(g, vertices_excluidos=ciudades_aisladas)
print(f'Componentes conexas restantes: {len(comp_lluvia)}')
for c in comp_lluvia:
    print(f' {[g.CIUDADES[v] for v in c]}')
print(f'Ciudades completamente aisladas: {[g.CIUDADES[v] for v in ciudades_aisladas]}')

print()
print("=== Bonus: solo Macusani(12) bloqueada ===")
comp_solo12 = componentes_conexas(g, vertices_excluidos={12})
print(f'Componentes: {len(comp_solo12)}')
for c in comp_solo12:
    print(f' {[g.CIUDADES[v] for v in c]}')