# -*- coding: utf-8 -*-
import pygame
import random
import asyncio
from ordenamientoVIsual import bubble_sort, selection_sort, insertion_sort, shell_sort

# Configuración de pantalla
WIDTH, HEIGHT = 1000, 920
BLANCO = (255, 255, 255)
GRIS_FONDO = (240, 242, 245)
AZUL_MARINO = (44, 62, 80)
AZUL_BARRAS = (52, 152, 219)

def generar_datos_unap(n=15):
    return [{"id": i+1, "prod": random.randint(1, 99), "ent": random.randint(5, 99), "prio": random.randint(1, 5)} for i in range(n)]

async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulador de Ordenamiento (15 Datos)")
    
    fuente = pygame.font.SysFont("Consolas", 14)
    fuente_b = pygame.font.SysFont("Segoe UI", 16, bold=True)
    
    array = generar_datos_unap(15)
    stats = {'comp': 0, 'swap': 0}
    columna_actual = 'prod'
    sentido_desc = False

    async def draw_ui(arr, color_map={}, msg=""):
        screen.fill(GRIS_FONDO)
        bar_x_inicio = 50
        bar_y_base = 350
        bar_w = 35
        
        titulo_grafica = fuente_b.render(f"VISUALIZACIÓN DE {columna_actual.upper()}", True, AZUL_MARINO)
        screen.blit(titulo_grafica, (bar_x_inicio, 40))

        for i, fila in enumerate(arr):
            val = fila[columna_actual]
            h_bar = val * 45 if columna_actual == 'prio' else val * 2.5
            color_bar = AZUL_BARRAS
            if i in color_map: color_bar = (230, 126, 34) # Naranja activo
            
            pygame.draw.rect(screen, color_bar, (bar_x_inicio + i*(bar_w+15), bar_y_base - h_bar, bar_w, h_bar))
            # Valor encima de la barra
            v_txt = fuente.render(str(val), True, AZUL_MARINO)
            screen.blit(v_txt, (bar_x_inicio + i*(bar_w+15) + 10, bar_y_base - h_bar - 20))

        # --- PARTE 2: TABLA DE DATOS (ABAJO) ---
        y_tabla = 420
        headers = ["# ID", "Producción", "Entrega", "Prioridad"]
        x_pts = [50, 120, 250, 380]
        
        # Encabezado tabla
        pygame.draw.rect(screen, AZUL_MARINO, (45, y_tabla, 500, 30))
        for i, h in enumerate(headers):
            screen.blit(fuente_b.render(h, True, BLANCO), (x_pts[i], y_tabla + 5))

        # Filas de la tabla
        for i, fila in enumerate(arr):
            color_f = (255, 255, 255)
            if i in color_map: color_f = (255, 235, 200)
            
            pygame.draw.rect(screen, color_f, (45, y_tabla + 35 + i*22, 500, 20))
            
            screen.blit(fuente.render(f"{fila['id']:02}", True, AZUL_MARINO), (x_pts[0]+10, y_tabla + 37 + i*22))
            screen.blit(fuente.render(f"{fila['prod']} min", True, AZUL_MARINO), (x_pts[1]+10, y_tabla + 37 + i*22))
            screen.blit(fuente.render(f"{fila['ent']} min", True, AZUL_MARINO), (x_pts[2]+10, y_tabla + 37 + i*22))
            screen.blit(fuente.render(f"Nivel {fila['prio']}", True, AZUL_MARINO), (x_pts[3]+10, y_tabla + 37 + i*22))

        # --- PANEL DE ESTADÍSTICAS Y CONTROL ---
        pygame.draw.rect(screen, BLANCO, (600, 420, 450, 330))
        pygame.draw.rect(screen, AZUL_MARINO, (600, 420, 450, 5), 0)
        
        screen.blit(fuente_b.render("ESTADÍSTICAS (Elija las opciones de cambio desde este panel)", True, AZUL_MARINO), (620, 440))
        screen.blit(fuente.render(f"Comparaciones (IFs): {stats['comp']}", True, (200, 0, 0)), (620, 480))
        screen.blit(fuente.render(f"Intercambios (SWAPs): {stats['swap']}", True, (0, 0, 200)), (620, 510))
        
        screen.blit(fuente_b.render(f"MODO: {columna_actual.upper()} | {('DESC' if sentido_desc else 'ASC')}", True, (39, 174, 96)), (620, 560))
        
        # Guía de teclas
        inst = ["[P]rod, [E]ntrega, [I]prio: Columna", "[A]sc, [D]esc: Sentido", "[1] Bubble, [2] Selection, [3] Insertion, [4] Shell: Método", "R: Generar 15 Nuevos"]
        for idx, t in enumerate(inst):
            screen.blit(fuente.render(t, True, (100, 100, 100)), (620, 600 + idx*25))

        msg_t = fuente_b.render(msg, True, (230, 126, 34))
        screen.blit(msg_t, (50, 10))

        pygame.display.update()
        # VELOCIDAD REDUCIDA A 0.2 SEGUNDOS
        await asyncio.sleep(0.2)

    running = True
    while running:
        await draw_ui(array, {}, "LISTO - Selecciona parámetros y presiona un número")
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: columna_actual = 'prod'
                if event.key == pygame.K_e: columna_actual = 'ent'
                if event.key == pygame.K_i: columna_actual = 'prio'
                if event.key == pygame.K_a: sentido_desc = False
                if event.key == pygame.K_d: sentido_desc = True
                if event.key == pygame.K_r: 
                    array = generar_datos_unap(15)
                    stats = {'comp': 0, 'swap': 0}
                
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    stats = {'comp': 0, 'swap': 0}
                    if event.key == pygame.K_1: await bubble_sort(array, draw_ui, stats, columna_actual, sentido_desc)
                    if event.key == pygame.K_2: await selection_sort(array, draw_ui, stats, columna_actual, sentido_desc)
                    if event.key == pygame.K_3: await insertion_sort(array, draw_ui, stats, columna_actual, sentido_desc)
                    if event.key == pygame.K_4: await shell_sort(array, draw_ui, stats, columna_actual, sentido_desc)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())