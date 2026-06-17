import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt
from algoritmos.ordenamiento import (
    bubble_sort_generator,
    selection_sort_generator,
    insertion_sort_generator,
    shell_sort_generator,
    quick_sort_generator,
    merge_sort_generator,
    counting_sort_generator,
    radix_sort_generator,
    bucket_sort_generator
)
from utils import lista_aleatoria, lista_ordenada, lista_inversa, lista_casi_ordenada

st.set_page_config(page_title="Comparación Ordenamiento", page_icon="🏆", layout="wide")

st.title("🏆 Comparación de Algoritmos de Ordenamiento")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Configuración")
    tipo_datos = st.selectbox("Tipo de datos", ["Aleatoria", "Ordenada", "Inversa", "Casi ordenada"])
    num_elementos = st.slider("Elementos", 10, 500, 100, 10)
    
    # Todos los algoritmos seleccionables
    todos_algoritmos = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Shell Sort",
                        "Quick Sort", "Merge Sort", "Counting Sort", "Radix Sort", "Bucket Sort"]
    
    seleccionados = st.multiselect("Algoritmos a comparar", todos_algoritmos, default=todos_algoritmos)
    ejecutar = st.button("🚀 Iniciar", type="primary", use_container_width=True)

GENERADORES = {
    "Bubble Sort": bubble_sort_generator,
    "Selection Sort": selection_sort_generator,
    "Insertion Sort": insertion_sort_generator,
    "Shell Sort": shell_sort_generator,
    "Quick Sort": quick_sort_generator,
    "Merge Sort": merge_sort_generator,
    "Counting Sort": counting_sort_generator,
    "Radix Sort": radix_sort_generator,
    "Bucket Sort": bucket_sort_generator,
}

def generar_lista(tipo, n):
    if tipo == "Aleatoria":
        return lista_aleatoria(n, 10, 1000)
    elif tipo == "Ordenada":
        return lista_ordenada(n)
    elif tipo == "Inversa":
        return lista_inversa(n)
    else:
        return lista_casi_ordenada(n, n//10)

def medir_tiempo(nombre, gen_func, lista):
    lista_copia = lista.copy()
    inicio = time.time()
    gen = gen_func(lista_copia) if nombre != "Bucket Sort" else gen_func(lista_copia, 5)
    try:
        while True:
            next(gen)
    except StopIteration:
        pass
    return (time.time() - inicio) * 1000

if ejecutar:
    if not seleccionados:
        st.error("Selecciona al menos un algoritmo")
    else:
        lista_prueba = generar_lista(tipo_datos, num_elementos)
        resultados = []
        barra = st.progress(0)
        
        for i, algo in enumerate(seleccionados):
            ms = medir_tiempo(algo, GENERADORES[algo], lista_prueba)
            resultados.append({"Algoritmo": algo, "Tiempo (ms)": ms})
            barra.progress((i + 1) / len(seleccionados))
        
        resultados.sort(key=lambda x: x["Tiempo (ms)"])
        
        # Ganador
        ganador = resultados[0]
        st.markdown(f"""
        <div style='text-align:center; background:gold; padding:20px; border-radius:20px'>
            <h1>🏆 GANADOR 🏆</h1>
            <h2>{ganador['Algoritmo']}</h2>
            <h3>{ganador['Tiempo (ms)']:.2f} ms</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabla
        df = pd.DataFrame(resultados)
        df["Tiempo (ms)"] = df["Tiempo (ms)"].map(lambda x: f"{x:.2f}")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        nombres = [r["Algoritmo"] for r in resultados]
        tiempos = [r["Tiempo (ms)"] for r in resultados]
        colores = ["gold" if i == 0 else "steelblue" for i in range(len(tiempos))]
        ax.barh(nombres, tiempos, color=colores)
        ax.set_xlabel("ms")
        ax.set_title(f"{num_elementos} elementos - {tipo_datos}")
        st.pyplot(fig)
        
        st.success(f"🏁 Más rápido: {ganador['Algoritmo']} ({ganador['Tiempo (ms)']:.2f} ms)")