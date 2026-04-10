import pygame
import random
import sys
from BusquedaVisual import *

pygame.init()
ANCHO, ALTO = 1100, 750 
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulador de Ingenieria: Analizador de Algoritmos (n=15)")

# Colores
FONDO = (18, 18, 24)
AZUL_SOFT = (50, 120, 220)
NARANJA = (255, 140, 0)
VERDE = (40, 180, 100)
ROJO = (220, 60, 60)
TEXTO = (240, 240, 240)

# Fuentes
FUENTE_TITULO = pygame.font.SysFont("Segoe UI", 30, bold=True)
FUENTE_DATOS = pygame.font.SysFont("Consolas", 18)
FUENTE_UI = pygame.font.SysFont("Segoe UI", 20)

def dibujar_interfaz(arr, objetivo, resaltados={}, info="ESPERANDO COMANDO", resultado=None):
    VENTANA.fill(FONDO)
    
    # 1. Cabecera Informativa
    pygame.draw.rect(VENTANA, (30, 30, 40), (40, 20, 1020, 110), border_radius=15)
    t_obj = FUENTE_TITULO.render(f"OBJETIVO: {objetivo}", True, NARANJA)
    VENTANA.blit(t_obj, (70, 35))
    
    arr_str = f"Arreglo (n=15): {arr}"
    t_arr = FUENTE_DATOS.render(arr_str if len(arr_str) < 95 else arr_str[:92] + "...", True, (160, 160, 180))
    VENTANA.blit(t_arr, (70, 85))

    # 2. Área de Barras (Optimizada para n=15)
    n = len(arr)
    if n > 0:
        ancho_disponible = 1000
        ancho_b = ancho_disponible // n
        max_v = max(arr) if max(arr) > 0 else 1
        
        for i, val in enumerate(arr):
            color = AZUL_SOFT
            if i in resaltados: color = resaltados[i]
            
            altura = (val * 350) // max_v
            x, y = 50 + (i * ancho_b), 550 - altura
            
            # Dibujar Barra
            pygame.draw.rect(VENTANA, color, (x, y, ancho_b - 10, altura), border_radius=4)
            
            # Valores (Encima) e Índices (Debajo)
            v_t = FUENTE_DATOS.render(str(val), True, TEXTO)
            VENTANA.blit(v_t, (x + (ancho_b//4) - 5, y - 30))
            
            i_t = FUENTE_DATOS.render(f"[{i}]", True, (110, 110, 120))
            VENTANA.blit(i_t, (x + (ancho_b//4) - 5, 560))

    # 3. Log de Estado
    pygame.draw.rect(VENTANA, (10, 10, 15), (50, 600, 1000, 45), border_radius=8)
    t_status = FUENTE_UI.render(f">>> {info}", True, (0, 255, 180))
    VENTANA.blit(t_status, (70, 610))

    # 4. Controles
    controles = "[1]Lineal  [2]Binaria  [3]Exponencial  [4]Interpolación  [E]Ingresar Datos  [R]Reset"
    t_ctrl = FUENTE_UI.render(controles, True, (200, 200, 200))
    VENTANA.blit(t_ctrl, (50, 670))

    # 5. PANEL DE RESULTADO
    if resultado is not None:
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        VENTANA.blit(overlay, (0,0))
        
        box_color = VERDE if resultado[0] else ROJO
        pygame.draw.rect(VENTANA, box_color, (350, 250, 400, 200), border_radius=20)
        pygame.draw.rect(VENTANA, TEXTO, (350, 250, 400, 200), 3, border_radius=20)
        
        res_t = "¡ENCONTRADO!" if resultado[0] else "NO ENCONTRADO"
        res_sub = f"Posición en Memoria: {resultado[1]}" if resultado[0] else "El valor no existe"
        
        txt1 = FUENTE_TITULO.render(res_t, True, TEXTO)
        txt2 = FUENTE_UI.render(res_sub, True, TEXTO)
        txt3 = FUENTE_DATOS.render("Presiona cualquier tecla para continuar", True, TEXTO)
        
        VENTANA.blit(txt1, (ANCHO//2 - txt1.get_width()//2, 290))
        VENTANA.blit(txt2, (ANCHO//2 - txt2.get_width()//2, 340))
        VENTANA.blit(txt3, (ANCHO//2 - txt3.get_width()//2, 400))

    pygame.display.update()
    
def esta_ordenado(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

def ejecutar(alg, arr, obj):
    nombre_alg = alg.__name__ # validacion algoitmo desordenado
    if "lineal" not in nombre_alg and not esta_ordenado(arr):
        dibujar_interfaz(arr, obj, {}, "ERROR: El arreglo debe estar ORDENADO para este algoritmo", (False, "Falla de Requisito"))
        esperando = True
        while esperando:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN or e.type == pygame.MOUSEBUTTONDOWN: esperando = False
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        return
    def callback(a, col, msg):
        dibujar_interfaz(a, obj, col, msg)
        pygame.time.delay(1000) # Mantengo el delay para análisis paso a paso
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()

    res = alg(arr, obj, callback)
    dibujar_interfaz(arr, obj, {res: VERDE} if res != -1 else {}, "Búsqueda finalizada", (res != -1, res))
    
    esperando = True
    while esperando:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN or e.type == pygame.MOUSEBUTTONDOWN: esperando = False
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()

def main():
    # Inicialización con 15 elementos
    datos = sorted(random.sample(range(10, 500), 15))
    objetivo = random.choice(datos)
    
    corriendo = True
    while corriendo:
        dibujar_interfaz(datos, objetivo)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: corriendo = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1: ejecutar(busqueda_lineal, datos, objetivo)
                elif e.key == pygame.K_2: ejecutar(busqueda_binaria, datos, objetivo)
                elif e.key == pygame.K_3: ejecutar(busqueda_exponencial, datos, objetivo)
                elif e.key == pygame.K_4: ejecutar(busqueda_interpolacion, datos, objetivo)
                elif e.key == pygame.K_r:
                    datos = sorted(random.sample(range(10, 500), 15))
                    objetivo = random.choice(datos)
                elif e.key == pygame.K_e:
                    print("\n--- INGRESO DE DATOS ---")
                    try:
                        entrada = input("Ingresa números separados por comas: ")
                        datos = [int(x.strip()) for x in entrada.split(",")] # sorted(...) para asegurar ordenamiento si no hay validacion
                        objetivo = int(input("Número a buscar: "))
                    except: print("Error en el formato.")

    pygame.quit()

if __name__ == "__main__": main()