import pandas as pd

def calcular_fcfs(df_procesos):
    # Asegurar que los datos estén ordenados por tiempo de llegada
    df = df_procesos.sort_values(by='T. llegada').copy()
    
    tiempos_inicio = []
    tiempos_fin = []
    
    tiempo_actual = 0
    for index, fila in df.iterrows():
        # El proceso inicia cuando llega o cuando la CPU se libera
        inicio = max(fila['T. llegada'], tiempo_actual)
        fin = inicio + fila['Duración']
        
        tiempos_inicio.append(inicio)
        tiempos_fin.append(fin)
        tiempo_actual = fin
        
    df['T. Inicio'] = tiempos_inicio
    df['T. Final'] = tiempos_fin
    df['T. Retorno'] = df['T. Final'] - df['T. llegada']
    df['T. Espera'] = df['T. Retorno'] - df['Duración']
    
    return df

def calcular_spn(df_procesos):
    df = df_procesos.copy()
    n = len(df)
    procesos_finalizados = []
    tiempo_actual = 0
    pendientes = df.to_dict('records')
    lista_final = []

    while len(lista_final) < n:
        # Filtrar procesos que ya han llegado al tiempo actual y no han terminado
        disponibles = [p for p in pendientes if p['T. llegada'] <= tiempo_actual]
        
        if disponibles:
            # Seleccionar el proceso con la menor duración (Criterio SPN)
            proceso_elegido = min(disponibles, key=lambda x: x['Duración'])
            pendientes.remove(proceso_elegido)
            
            proceso_elegido['T. Inicio'] = tiempo_actual
            proceso_elegido['T. Final'] = tiempo_actual + proceso_elegido['Duración']
            proceso_elegido['T. Retorno'] = proceso_elegido['T. Final'] - proceso_elegido['T. llegada']
            proceso_elegido['T. Espera'] = proceso_elegido['T. Retorno'] - proceso_elegido['Duración']
            
            tiempo_actual = proceso_elegido['T. Final']
            lista_final.append(proceso_elegido)
        else:
            # Si nadie ha llegado, avanzar el reloj al tiempo de llegada del siguiente
            tiempo_actual += 1
            
    return pd.DataFrame(lista_final)

def imprimir_resultados(df, nombre_algoritmo):
    print(f"\n--- RESULTADOS {nombre_algoritmo} ---")
    # Mostrar la tabla completa
    print(df.to_string(index=False))
    
    # Calcular promedios
    tmr = df['T. Retorno'].mean()
    tme = df['T. Espera'].mean()
    
    print("-" * 30)
    print(f"Tiempo Medio de Retorno (TMR): {tmr:.2f}")
    print(f"Tiempo Medio de Espera (TME): {tme:.2f}")
    print("-" * 30)

# Para probarlo con los datos de la Fase 1:
if __name__ == "__main__":
    datos = {
        'Proceso': ['A', 'B', 'C', 'D', 'E'],
        'T. llegada': [0, 1, 3, 9, 12],
        'Duración': [3, 5, 2, 5, 5]
    }
    df_input = pd.DataFrame(datos)
    
    # Ejecutar y mostrar FCFS
    resultado_fcfs = calcular_fcfs(df_input)
    imprimir_resultados(resultado_fcfs, "FCFS")
    
    # Ejecutar y mostrar SPN
    resultado_spn = calcular_spn(df_input)
    imprimir_resultados(resultado_spn, "SPN")