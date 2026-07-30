# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
from hash_logic import HashTableChaining, HashTableLinearProbing, HashTableDoubleHash

st.set_page_config(page_title="Simulador de Estructuras Hash", layout="wide")

st.title("🛡️ Simulador de Tablas Hashing")
st.markdown("### Basado en la Práctica")

# --- MANUAL DE USUARIO ---
with st.expander("📖 Guía Rápida"):
    st.markdown("""
    1. **Configuración:** cargue el archivo CSV y seleccione la columna clave.
    2. **Ahuste**:** Elija el tamaño de la tabla (m) para ver el factor de carga y las colisiones.
    3. **Métodos:** Comparamos Encadenamiento Separado vs Sondeo (Lineal) vs Doble Hashing.
    4. **Análisis:** El sistema medirá cuántas **colisiones** ocurren y el tiempo de inserción.
    
    ⚠️ *Nota: m no puede ser menor a n o entrara en un bucle infinito. en este caso se puso un seguro que solo ejecuta hasta 90% de la capacidad*
    """)

# --- Configuración Lateral ---
st.sidebar.header("⚙️ Parámetros del configuracion")
archivo = st.sidebar.file_uploader("Cargar Dataset (ecomm.data.csv)", type=["csv"])

m_size = st.sidebar.number_input("Tamaño de Tabla (m)", value=20011)
n_records = st.sidebar.slider("Registros a procesar (n)", 500, 20000, 5000)

if archivo:
    df = pd.read_csv(archivo).dropna()
    st.subheader("👀 Vista Previa del Dataset (Verificación de Carga)")
    st.dataframe(df.head(10)) 
    col_clave = st.sidebar.selectbox("Seleccionar Clave (ID)", df.columns)
    keys = df[col_clave].astype(str).head(n_records).tolist()

    if st.button("🚀 Iniciar Análisis Experimental"):
        # Instanciar modelos
        modelos = {
            "Encadenamiento": HashTableChaining(m_size),
            "Sondeo Lineal": HashTableLinearProbing(m_size),
            "Doble Hashing": HashTableDoubleHash(m_size)
        }
        
        datos_finales = []

        # Barra de progreso para estética de simulador
        progreso = st.progress(0)
        
        for i, (nombre, obj) in enumerate(modelos.items()):
            # Medir Inserción
            t_start = time.perf_counter()
            for k in keys:
                obj.insert(k, k)
            t_ins = (time.perf_counter() - t_start) * 1000 # ms

            # Medir Búsqueda (1000 aleatorias)
            t_start = time.perf_counter()
            for k in keys[:1000]:
                obj.search(k)
            t_bus = (time.perf_counter() - t_start) * 1000 # ms

            datos_finales.append({
                "Método": nombre,
                "Colisiones": obj.collisions,
                "Factor de Carga (λ)": round(obj.load_factor(), 4),
                "Inserción (ms)": round(t_ins, 4),
                "Búsqueda (ms)": round(t_bus, 4)
            })
            progreso.progress((i + 1) / len(modelos))

        # --- Resultados ---
        st.subheader("📋 Tabla Comparativa de Resultados")
        res_df = pd.DataFrame(datos_finales)
        st.dataframe(res_df.style.highlight_max(axis=0, subset=['Colisiones'], color='#ff4b4b22'))

        # --- Gráficos Requeridos ---
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Colisiones por Método**")
            st.bar_chart(res_df.set_index("Método")["Colisiones"])
        with col2:
            st.write("**Tiempo de Búsqueda (ms)**")
            st.line_chart(res_df.set_index("Método")["Búsqueda (ms)"])

        st.success("✅ Simulación completada según requerimientos de la Parte 12.")
else:
    st.warning("Esperando dataset para inicializar el simulador...")