# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
import logica_planificacion as lp

# 1. Configuración de la página
st.set_page_config(page_title="Simulador de SO - UNA Puno", layout="wide", page_icon="🖥️")

# Estilo para el título
st.title("🖥️ Simulador Profesional de Sistemas Operativos")
st.markdown("---")

# --- MANUAL DE USUARIO PARA PRINCIPIANTES ---
with st.expander("📖 GUÍA COMPLETA: ¿Cómo entender este simulador?"):
    st.markdown("""
    ### 🧠 Conceptos Básicos
    Este simulador te permite comparar cómo un Sistema Operativo gestiona sus dos recursos más críticos: el **Procesador (CPU)** y la **Memoria RAM**.
    
    #### 1. Planificación de CPU (¿Quién usa el procesador?)
    - **FCFS:** El primero en llegar es el primero en ser atendido. Es justo, pero lento si llega un proceso muy largo primero.
    - **SPN:** El proceso más corto pasa primero. Minimiza el tiempo de espera promedio.
    - **SRT:** Versión expulsiva del SPN. Si llega uno más corto que el que se está ejecutando, lo saca.
    - **Round Robin (RR):** Todos reciben un "pedacito" de tiempo (Quantum). Si no terminan, vuelven al final de la cola.
    
    #### 2. Gestión de Memoria (¿Dónde guardamos los datos?)
    - **Primer Ajuste:** Coloca el proceso en el primer hueco donde quepa. Es el más rápido.
    - **Mejor Ajuste:** Busca el hueco que más se parezca al tamaño del proceso. Minimiza el desperdicio inmediato.
    - **Peor Ajuste:** Coloca el proceso en el hueco más grande disponible. Deja huecos grandes para otros procesos.
    - **Buddy System:** Divide la memoria en potencias de 2 ($2, 4, 8, 16...$). Muy eficiente para sistemas rápidos.
    """)
    

# 2. Barra Lateral
st.sidebar.header("🛠️ Panel de Control")
modulo = st.sidebar.radio("Seleccione el Módulo:", ["Planificación de CPU", "Gestión de Memoria"])
archivo_subido = st.sidebar.file_uploader("Cargar archivo de procesos (CSV)", type=["csv", "txt"])

# --- CONFIGURACIÓN DINÁMICA ---
if modulo == "Planificación de CPU":
    st.sidebar.markdown("---")
    metodo = st.sidebar.selectbox("Algoritmo de CPU:", 
        ["FCFS (First-Come First-Served)", "SPN (Shortest Process Next)", "SRT (Shortest Remaining Time)", "Round Robin (RR)"])
    
    q_val = 2
    if "Round Robin" in metodo:
        q_val = st.sidebar.number_input("Quantum (q):", min_value=1, value=2)
    modo_vista = st.sidebar.radio("Visualización:", ["Estático", "Simulación Animada"])

else:
    st.sidebar.markdown("---")
    st.sidebar.header("💾 Configuración de RAM")
    mem_total = st.sidebar.number_input("Capacidad RAM (K):", min_value=128, value=1024, step=128)
    tam_so = st.sidebar.number_input("Reserva S.O. (K):", min_value=0, value=150)
    metodo_mem = st.sidebar.selectbox("Algoritmo de Asignación:", 
        ["Primer Ajuste", "Mejor Ajuste", "Peor Ajuste", "Buddy System"])

# 3. Funciones Gráficas
def dibujar_gantt(gantt_data, titulo, max_t):
    fig, ax = plt.subplots(figsize=(10, 3))
    colores = plt.cm.get_cmap('tab10', len(gantt_data))
    for i, b in enumerate(gantt_data):
        ax.broken_barh([(b['Inicio'], b['Duración'])], (10, 9), facecolors=colores(i%10), edgecolor='black')
        ax.text(b['Inicio'] + b['Duración']/2, 14.5, b['Proceso'], ha='center', va='center', color='white', fontweight='bold')
    ax.set_xlabel("Tiempo")
    ax.set_yticks([])
    ax.set_title(titulo)
    ax.set_xlim(0, max_t + 1)
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)
    return fig

def dibujar_mapa_memoria_pro(mem_estado, mem_total, tam_so):
    fig, ax = plt.subplots(figsize=(5, 8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, mem_total)
    # S.O.
    ax.add_patch(plt.Rectangle((0.1, 0), 0.8, tam_so, color='#2c3e50', ec='black'))
    ax.text(0.5, tam_so/2, f"S.O.\n{tam_so}K", ha='center', color='white', fontweight='bold')
    # Bloques
    for b in mem_estado:
        color = '#e74c3c' if b['estado'] == 'Ocupado' else '#2ecc71'
        ax.add_patch(plt.Rectangle((0.1, b['base']), 0.8, b['tam'], color=color, ec='black', alpha=0.8))
        label = f"{b['proceso']}\n{b['tam']}K"
        ax.text(0.5, b['base'] + b['tam']/2, label, ha='center', va='center', fontweight='bold', fontsize=9)
        ax.text(0.92, b['base'], f"{int(b['base'])}K", fontsize=7, color='gray')
    ax.set_title("Mapa de Memoria Física", fontweight='bold')
    ax.set_xticks([])
    return fig

# 4. Lógica de Ejecución
if archivo_subido:
    df_input = lp.cargar_procesos(archivo_subido)
    
    if df_input is not None:
        if modulo == "Planificación de CPU":
            # Selección de Algoritmo
            if "FCFS" in metodo: res_df, gantt = lp.calcular_fcfs(df_input)
            elif "SPN" in metodo: res_df, gantt = lp.calcular_spn(df_input)
            elif "SRT" in metodo: res_df, gantt = lp.calcular_srt(df_input)
            else: res_df, gantt = lp.calcular_rr(df_input, q_val)

            st.subheader(f"📊 Resultados: {metodo}")
            
            if modo_vista == "Simulación Animada":
                barra = st.progress(0)
                for i in range(len(gantt)):
                    time.sleep(0.2)
                    barra.progress((i+1)/len(gantt))
            
            st.pyplot(dibujar_gantt(gantt, metodo, res_df['T. Final'].max()))
            st.table(res_df)
            st.info(f"**Tiempo de Espera Promedio:** {res_df['T. Espera'].mean():.2f} unidades.")

        else: # MEMORIA
            st.subheader(f"🧠 Asignación: {metodo_mem}")
            if "Primer" in metodo_mem: mem_res = lp.calcular_primer_ajuste(mem_total, tam_so, df_input)
            elif "Mejor" in metodo_mem: mem_res = lp.calcular_mejor_ajuste(mem_total, tam_so, df_input)
            elif "Peor" in metodo_mem: mem_res = lp.calcular_peor_ajuste(mem_total, tam_so, df_input)
            else: mem_res = lp.calcular_buddy_system(mem_total, tam_so, df_input)

            # Métricas
            met = lp.calcular_metricas_memoria(mem_res, mem_total, tam_so)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Uso Total", met['Uso Total'])
            c2.metric("Fragmentación", met['Fragmentación Externa'])
            c3.metric("% Uso", met['Porcentaje de Uso'])
            c4.metric("Libre", met['Libre Total'])

            col_izq, col_der = st.columns([1, 1.2])
            with col_izq: st.pyplot(dibujar_mapa_memoria_pro(mem_res, mem_total, tam_so))
            with col_der: st.write("### 📝 Particiones"); st.table(pd.DataFrame(mem_res))
    else:
        st.error("Error al leer el archivo.")
else:
    st.info("👈 Cargue un archivo CSV para comenzar.")