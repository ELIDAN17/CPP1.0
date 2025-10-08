

import matplotlib.pyplot as plt
import numpy as np

# --- 1. Definición de la función de simulación de rendimiento del servidor ---

def simular_rendimiento_servidor(
    max_solicitudes,  # Número máximo de solicitudes a simular
    capacidad_servidor, # Solicitudes por segundo que el servidor puede procesar
    tiempo_base_procesamiento, # Tiempo mínimo para procesar una solicitud (segundos)
    constante_congestión # Ajusta cuán rápido empeora el rendimiento con la carga
):
    """
    Simula el tiempo de respuesta y la probabilidad de rechazo de un servidor
    en función del número de solicitudes concurrentes.

    Args:
        max_solicitudes (int): El número máximo de solicitudes concurrentes a evaluar.
        capacidad_servidor (float): La capacidad del servidor en solicitudes por segundo.
        tiempo_base_procesamiento (float): El tiempo mínimo de procesamiento por solicitud (en segundos).
        constante_congestión (float): Un factor que ajusta la sensibilidad del tiempo de respuesta
                                     a la congestión (cuanto mayor, más rápido empeora).

    Returns:
        tuple: Listas de solicitudes, tiempos de respuesta promedio y probabilidades de rechazo.
    """
    solicitudes_range = np.arange(1, max_solicitudes + 1, 1) # Rango de 1 a max_solicitudes
    tiempos_respuesta = []
    probabilidades_rechazo = []

    # Umbral de capacidad para empezar a considerar rechazo, ej. 80% de la capacidad
    umbral_rechazo = capacidad_servidor * 0.8

    print(f"Simulando servidor con Capacidad={capacidad_servidor} req/s, Tiempo Base={tiempo_base_procesamiento}s")

    for n_solicitudes in solicitudes_range:
        # --- CÁLCULO DE TIEMPO DE RESPUESTA (Función de varias variables) ---
        if n_solicitudes >= capacidad_servidor:
            # El servidor está sobrecargado, el tiempo tiende a infinito
            tiempo_actual = float('inf')
        else:
            # Tiempo de respuesta aumenta con la carga
            tiempo_actual = tiempo_base_procesamiento + \
                            (constante_congestión * n_solicitudes) / \
                            (capacidad_servidor - n_solicitudes)

        tiempos_respuesta.append(tiempo_actual)

        # --- CÁLCULO DE PROBABILIDAD DE RECHAZO (Función de varias variables) ---
        if n_solicitudes <= umbral_rechazo:
            prob_rechazo = 0.0
        elif n_solicitudes >= capacidad_servidor:
            prob_rechazo = 1.0 # Rechazo total
        else:
            # Aumenta linealmente después del umbral hasta la capacidad total
            prob_rechazo = (n_solicitudes - umbral_rechazo) / (capacidad_servidor - umbral_rechazo)
            prob_rechazo = max(0.0, min(1.0, prob_rechazo)) # Asegura que esté entre 0 y 1

        probabilidades_rechazo.append(prob_rechazo)

    return solicitudes_range, tiempos_respuesta, probabilidades_rechazo

# --- 2. Parámetros de la simulación ---
# Parámetros del servidor (puedes ajustarlos)
CAPACIDAD_SERVIDOR = 150.0          # Solicitudes por segundo que el servidor puede procesar
TIEMPO_BASE_PROCESAMIENTO = 0.1    # 50 ms por solicitud sin congestión
CONSTANTE_CONGESTION = 0.5          # Qué tan sensible es el tiempo de respuesta a la congestión

# Rango de solicitudes a simular
MAX_SOLICITUDES_SIMULADAS = 120     # Simular hasta 120 solicitudes concurrentes

# --- 3. Ejecutar la simulación ---
solicitudes, tiempos_resp, probs_rechazo = simular_rendimiento_servidor(
    MAX_SOLICITUDES_SIMULADAS,
    CAPACIDAD_SERVIDOR,
    TIEMPO_BASE_PROCESAMIENTO,
    CONSTANTE_CONGESTION
)

# --- 4. Visualización de resultados ---
plt.figure(figsize=(14, 6))

# Gráfico del Tiempo de Respuesta Promedio
plt.subplot(1, 2, 1)
plt.plot(solicitudes, tiempos_resp, label='Tiempo de Respuesta Promedio')
plt.axvline(x=CAPACIDAD_SERVIDOR, color='r', linestyle='--', label=f'Capacidad del Servidor ({CAPACIDAD_SERVIDOR:.0f} req/s)')
plt.title('Tiempo de Respuesta del Servidor vs. Carga')
plt.xlabel('Número de Solicitudes Concurrentes')
plt.ylabel('Tiempo de Respuesta (segundos)')
plt.grid(True)
plt.legend()
plt.ylim(0, np.nanmax(np.array(tiempos_resp)[np.array(tiempos_resp) != np.inf]) * 1.5) # Ajusta el límite Y

# Gráfico de la Probabilidad de Rechazo
plt.subplot(1, 2, 2)
plt.plot(solicitudes, probs_rechazo, label='Probabilidad de Rechazo', color='orange')
plt.axvline(x=CAPACIDAD_SERVIDOR * 0.8, color='g', linestyle=':', label=f'Umbral de Rechazo ({CAPACIDAD_SERVIDOR * 0.8:.0f} req/s)')
plt.axvline(x=CAPACIDAD_SERVIDOR, color='r', linestyle='--', label=f'Capacidad del Servidor ({CAPACIDAD_SERVIDOR:.0f} req/s)')
plt.title('Probabilidad de Rechazo vs. Carga')
plt.xlabel('Número de Solicitudes Concurrentes')
plt.ylabel('Probabilidad de Rechazo (0-1)')
plt.grid(True)
plt.legend()
plt.ylim(-0.1, 1.1)

plt.tight_layout()
plt.show()

# Imprimir algunos resultados clave
print(f"\nResultados clave de la simulación:")
idx_50_req = 50 - 1 # Índice para 50 solicitudes
if idx_50_req < len(solicitudes):
    print(f"Para {solicitudes[idx_50_req]} solicitudes: TR={tiempos_resp[idx_50_req]:.3f}s, PR={probs_rechazo[idx_50_req]:.2f}")

idx_90_req = 90 - 1 # Índice para 90 solicitudes
if idx_90_req < len(solicitudes):
    print(f"Para {solicitudes[idx_90_req]} solicitudes: TR={tiempos_resp[idx_90_req]:.3f}s, PR={probs_rechazo[idx_90_req]:.2f}")

idx_100_req = 100 - 1 # Índice para 100 solicitudes (o capacidad)
if idx_100_req < len(solicitudes):
    print(f"Para {solicitudes[idx_100_req]} solicitudes: TR={tiempos_resp[idx_100_req]:.3f}s, PR={probs_rechazo[idx_100_req]:.2f}")

'''


edad =10
mide=1.55
nombre='Johan'
aprobar=True
nota=15.5
print(f'habia una vez un niño llamado {nombre} que tenia {edad} años. ')
print(f'El niño mide {mide} metros y esta {aprobar} (aprobado) en el curso. ')
print(f'saco {nota} en el examen final.')

'''