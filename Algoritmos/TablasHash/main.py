import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import os
from logica import TablaHashEncadenamiento, TablaHashSondeo

# Configuración de página según criterios de calidad
st.set_page_config(page_title=" Lab 3: Tablas Hash", layout="wide")

st.title("📊 Laboratorio 3: Análisis de Tablas Hash con Datos de Kaggle")
st.write("Estudiante: JMP EliteSnow")

# --- MANUAL DE USUARIO EN APP ---
with st.expander("📖 Guía Rápida - Práctica Lab 3"):
    st.markdown("""
    1. **Configuración:** cargue el archivo CSV y seleccione las columnas clave y valor.
    2. **Métodos:** Comparamos Encadenamiento Separado vs Sondeo (Lineal/Cuadrático).
    3. **Análisis:** El sistema medirá cuántas **colisiones** ocurren y el tiempo de inserción.
    """)

# --- 1. CARGA Y VISTA PREVIA DE DATOS  ---
st.sidebar.header("Configuración de Datos")
archivo_subido = st.sidebar.file_uploader("Cargar Dataset CSV (Ej. ecommerce_data.csv)", type=["csv"])

if archivo_subido:
    # Carga y limpieza inicial
    df = pd.read_csv(archivo_subido, low_memory=False, encoding='unicode_escape')
    
    st.subheader("👀 Vista Previa del Dataset (Verificación de Carga)")
    st.dataframe(df.head(10)) # Muestra los primeros 10 para verificar si es el correcto
    
    # Selección de columnas clave y valor
    columnas = df.columns.tolist()
    col_clave = st.sidebar.selectbox("Selecciona Columna CLAVE (CustomerID)", columnas, index=columnas.index('CustomerID') if 'CustomerID' in columnas else 0)
    col_valor = st.sidebar.selectbox("Selecciona Columna VALOR (Country)", columnas, index=columnas.index('Country') if 'Country' in columnas else 0)

    # Limpieza: eliminar nulos y normalizar [cite: 63]
    df_clean = df[[col_clave, col_valor]].dropna().drop_duplicates(subset=[col_clave])
    df_clean[col_clave] = df_clean[col_clave].astype(str).str.strip()
    
    st.info(f"Registros únicos listos para procesar: {len(df_clean)}")

    # --- 2. BENCHMARK Y COMPARACIÓN ---
    tamanios_m = [1009, 2003, 4001, 8009] # Tamaños primos sugeridos
    
    if st.button("🚀 Ejecutar Análisis Comparativo (Sección 10)"):
        resultados = []
        progress_bar = st.progress(0)
        
        for i, m in enumerate(tamanios_m):
            # Usamos un factor de carga cercano al 0.65 para la prueba
            n_actual = int(m * 0.65)
            batch = df_clean.head(n_actual)
            claves = batch[col_clave].tolist()
            valores = batch[col_valor].tolist()

            # --- Encadenamiento ---
            t_enc = TablaHashEncadenamiento(m)
            start = time.perf_counter()
            for c, v in zip(claves, valores): t_enc.insertar(c, v)
            time_enc = (time.perf_counter() - start) * 1000

            # --- Sondeo Lineal ---
            t_sl = TablaHashSondeo(m, tipo="lineal")
            start = time.perf_counter()
            for c, v in zip(claves, valores): t_sl.insertar(c, v)
            time_sl = (time.perf_counter() - start) * 1000

            # --- Dict Nativo Python (Referencia) ---
            t_py = {}
            start = time.perf_counter()
            for c, v in zip(claves, valores): t_py[c] = v
            time_py = (time.perf_counter() - start) * 1000

            resultados.append({
                "m (Tamaño)": m,
                "n (Elementos)": len(claves),
                "λ (Factor Carga)": round(len(claves)/m, 3), # 
                "Colisiones Enc.": t_enc.colisiones,
                "Colisiones Sondeo": t_sl.colisiones,
                "Tiempo Enc. (ms)": round(time_enc, 4),
                "Tiempo Sondeo (ms)": round(time_sl, 4),
                "Tiempo Dict Python (ms)": round(time_py, 4)
            })
            progress_bar.progress((i + 1) / len(tamanios_m))

        # --- 3. PRESENTACIÓN DE RESULTADOS ---
        df_res = pd.DataFrame(resultados)
        st.subheader("📋 Tabla Comparativa de Resultados")
        st.table(df_res)

        # Gráficos requeridos
        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            st.write("**Colisiones vs. Tamaño de Tabla**")
            fig1, ax1 = plt.subplots()
            ax1.plot(df_res["m (Tamaño)"], df_res["Colisiones Enc."], label="Encadenamiento", marker='o')
            ax1.plot(df_res["m (Tamaño)"], df_res["Colisiones Sondeo"], label="Sondeo Lineal", marker='s')
            ax1.set_xlabel("Capacidad (m)")
            ax1.set_ylabel("N° Colisiones")
            ax1.legend()
            st.pyplot(fig1)

        with col_graf2:
            st.write("**Tiempo de Inserción Comparativo**")
            fig2, ax2 = plt.subplots()
            ax2.bar(["Encadenamiento", "Sondeo Lineal", "Python Dict"], 
                   [df_res["Tiempo Enc. (ms)"].mean(), df_res["Tiempo Sondeo (ms)"].mean(), df_res["Tiempo Dict Python (ms)"].mean()],
                   color=['blue', 'orange', 'green'])
            ax2.set_ylabel("Tiempo Promedio (ms)")
            st.pyplot(fig2)

        st.success("✅ Análisis finalizado. Se cumple con el análisis asintótico promedio O(1).")
else:
    st.warning("Por favor, sube el archivo 'ecommerce_data.csv' de Kaggle para comenzar.")