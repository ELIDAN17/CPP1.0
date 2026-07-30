# -*- coding: utf-8 -*-
import asyncio
import pygame
import random
import sys
from BusquedaVisual import *

pygame.init()
ANCHO, ALTO = 1100, 750 
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulador de Algoritmos de Busqueda Visual")

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

    # 2. Area de Barras
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
            pygame.draw.rect(VENTANA, color, (x, y, ancho_b - 10, altura), border_radius=4)
            if n <= 15:
                v_t = FUENTE_DATOS.render(str(val), True, TEXTO)
                VENTANA.blit(v_t, (x + (ancho_b//4) - 5, y - 30))
                i_t = FUENTE_DATOS.render(f"[{i}]", True, (110, 110, 120))
                VENTANA.blit(i_t, (x + (ancho_b//4) - 5, 560))

    # 3. Log de Estado
    pygame.draw.rect(VENTANA, (10, 10, 15), (50, 600, 1000, 45), border_radius=8)
    t_status = FUENTE_UI.render(f">>> {info}", True, (0, 255, 180))
    VENTANA.blit(t_status, (70, 610))

    # 4. Controles
    controles = "[1]Lineal  [2]Binaria  [3]Exponencial  [4]Interpolacion [G]Generar Datos  [E]Editar"
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
        
        res_t = "ENCONTRADO!" if resultado[0] else "NO ENCONTRADO"
        res_sub = f"Posicion en Memoria: {resultado[1]}" if resultado[0] else "El valor no existe"
        
        txt1 = FUENTE_TITULO.render(res_t, True, TEXTO)
        txt2 = FUENTE_UI.render(res_sub, True, TEXTO)
        txt3 = FUENTE_DATOS.render("Presiona cualquier tecla para continuar", True, TEXTO)
        
        VENTANA.blit(txt1, (ANCHO//2 - txt1.get_width()//2, 290))
        VENTANA.blit(txt2, (ANCHO//2 - txt2.get_width()//2, 340))
        VENTANA.blit(txt3, (ANCHO//2 - txt3.get_width()//2, 400))

    pygame.display.update()

def esta_ordenado(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

async def esperar_tecla():
    esperando = True
    while esperando:
        for e in pygame.event.get():
            if e.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]: esperando = False
            #if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        await asyncio.sleep(0)
        
async def ejecutar(alg, arr, obj):
    nombre_alg = alg.__name__ 
    if "lineal" not in nombre_alg and not esta_ordenado(arr):
        dibujar_interfaz(arr, obj, {}, "ERROR: El arreglo debe estar ORDENADO", (False, "Falla de Requisito"))
        await esperar_tecla()
        return
    async def callback(a, col, msg):
        dibujar_interfaz(a, obj, col, msg)
        await asyncio.sleep(1)
        #pygame.time.delay(1000) 
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()

    res = await alg(arr, obj, callback)
    dibujar_interfaz(arr, obj, {res: VERDE} if res != -1 else {}, "Busqueda finalizada", (res != -1, res))
    await esperar_tecla()

async def main():
    # Usamos un diccionario 'estado' para que las variables sean mutables y accesibles
    estado = {
        "datos": sorted(random.sample(range(10, 500), 15)),
        "objetivo": 0,
        "mensaje": "ESPERANDO COMANDO"
    }
    estado["objetivo"] = random.choice(estado["datos"])
    
    corriendo = True
    while corriendo:
        # IMPORTANTE: Pasamos estado["mensaje"] al parámetro 'info'
        dibujar_interfaz(estado["datos"], estado["objetivo"], info=estado["mensaje"])
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: 
                corriendo = False
            
            if e.type == pygame.KEYDOWN:
                # Comandos de búsqueda
                if e.key == pygame.K_1: 
                    await ejecutar(busqueda_lineal, estado["datos"], estado["objetivo"])
                elif e.key == pygame.K_2: 
                    await ejecutar(busqueda_binaria, estado["datos"], estado["objetivo"])
                elif e.key == pygame.K_3: 
                    await ejecutar(busqueda_exponencial, estado["datos"], estado["objetivo"])
                elif e.key == pygame.K_4: 
                    await ejecutar(busqueda_interpolacion, estado["datos"], estado["objetivo"])
                
                # Comando Generar
                elif e.key == pygame.K_g:
                    estado["datos"] = sorted(random.sample(range(10, 500), 15))
                    estado["objetivo"] = random.choice(estado["datos"])
                    estado["mensaje"] = "NUEVOS DATOS GENERADOS"
                
                # Comando Editar
                elif e.key == pygame.K_e:
                    estado["mensaje"] = "INFO: Edicion no disponible en Web (Usa 'G')"
        
        await asyncio.sleep(0) 
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())