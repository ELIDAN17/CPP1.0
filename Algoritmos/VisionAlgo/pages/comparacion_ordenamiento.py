"""
Pestaña de Comparación de Algoritmos de Ordenamiento
Ejecuta todos los algoritmos de ordenamiento con estadísticas detalladas.
"""

import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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
st.markdown("### ¿Cuál algoritmo ordena más rápido?")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Configuración")
    tipo_datos = st.selectbox(
        "Tipo de datos",
        ["Aleatoria", "Ordenada", "Inversa", "Casi ordenada"],
        index=0,
        help="El tipo de datos afecta drásticamente el rendimiento"
    )
    num_elementos = st.slider(
        "Elementos",
        10, 500, 100, 10,
        help="Para más de 300 elementos, Bubble Sort puede tardar"
    )
    
    st.markdown("---")
    st.markdown("### Algoritmos a comparar")
    
    todos_algoritmos = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Shell Sort",
                        "Quick Sort", "Merge Sort", "Counting Sort", "Radix Sort", "Bucket Sort"]
    
    seleccionados = st.multiselect(
        "Selecciona los algoritmos",
        todos_algoritmos,
        default=["Quick Sort", "Merge Sort", "Insertion Sort", "Shell Sort"]
    )
    
    st.markdown("---")
    ejecutar = st.button("🚀 Iniciar comparación", type="primary", use_container_width=True)

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

def medir_tiempo_y_operaciones(nombre, gen_func, lista):
    """
    Ejecuta un algoritmo y mide tiempo, comparaciones e intercambios.
    """
    lista_copia = lista.copy()
    inicio = time.time()
    gen = gen_func(lista_copia) if nombre != "Bucket Sort" else gen_func(lista_copia, 5)
    
    comparaciones = 0
    intercambios = 0
    elementos = len(lista_copia)
    
    try:
        while True:
            estado = next(gen)
            
            # Extraer operación del estado
            if len(estado) >= 4:
                operacion = estado[-2] if len(estado) >= 5 else estado[-1]
                
                if operacion in ["comparing", "comparando"]:
                    comparaciones += 1
                elif operacion in ["swapping", "swapping_pivot", "shifting", "intercambiando"]:
                    intercambios += 1
    except StopIteration:
        pass
    
    fin = time.time()
    tiempo_ms = (fin - inicio) * 1000
    
    return {
        "tiempo_ms": tiempo_ms,
        "comparaciones": comparaciones,
        "intercambios": intercambios,
        "elementos": elementos
    }

if ejecutar:
    if not seleccionados:
        st.error("⚠️ Selecciona al menos un algoritmo para comparar")
    else:
        with st.spinner("🔄 Ejecutando algoritmos... Esto puede tomar unos segundos"):
            lista_prueba = generar_lista(tipo_datos, num_elementos)
            resultados = []
            barra = st.progress(0)
            
            for i, algo in enumerate(seleccionados):
                stats = medir_tiempo_y_operaciones(algo, GENERADORES[algo], lista_prueba)
                resultados.append({
                    "Algoritmo": algo,
                    "Tiempo (ms)": stats["tiempo_ms"],
                    "Comparaciones": stats["comparaciones"],
                    "Intercambios": stats["intercambios"],
                    "Elementos": stats["elementos"]
                })
                barra.progress((i + 1) / len(seleccionados))
            
            barra.empty()
            
            # Ordenar por tiempo
            resultados.sort(key=lambda x: x["Tiempo (ms)"])
            
            # Guardar en session_state
            st.session_state.resultados_ordenamiento = resultados
            st.session_state.lista_ordenamiento = lista_prueba

# ========== MOSTRAR RESULTADOS ==========
if "resultados_ordenamiento" in st.session_state and st.session_state.resultados_ordenamiento:
    resultados = st.session_state.resultados_ordenamiento
    lista_original = st.session_state.lista_ordenamiento
    
    # ========== MOSTRAR LISTA ==========
    st.subheader("📋 Datos de prueba")
    if len(lista_original) <= 30:
        st.markdown(f"**Lista:** `{lista_original}`")
    else:
        preview = lista_original[:30]
        st.markdown(f"**Lista:** `{preview}...` (total: {len(lista_original)})")
    st.markdown(f"**Tipo:** {tipo_datos} | **Elementos:** {num_elementos}")
    st.markdown("---")
    
    # ========== TARJETA DEL GANADOR ==========
    ganador = resultados[0]
    st.markdown(f"""
    <div style='text-align:center; background: linear-gradient(135deg, #ffd700, #ffb347); 
                padding:20px; border-radius:20px; margin:10px 0;'>
        <h1 style='margin:0; font-size:3em;'>🏆 GANADOR 🏆</h1>
        <h2 style='margin:0; color:#fff;'>{ganador['Algoritmo']}</h2>
        <h3 style='margin:0; color:#fff;'>⚡ {ganador['Tiempo (ms)']:.2f} ms</h3>
        <p style='margin:0; color:#fff;'>Comparaciones: {ganador['Comparaciones']} | Intercambios: {ganador['Intercambios']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== TABLA DE RESULTADOS ==========
    st.subheader("📊 Tabla comparativa")
    
    df = pd.DataFrame(resultados)
    df["Tiempo (ms)"] = df["Tiempo (ms)"].map(lambda x: f"{x:.2f}")
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # ========== GRÁFICO DE BARRAS (TIEMPO) ==========
    st.subheader("📈 Comparación de tiempos")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    nombres = [r["Algoritmo"] for r in resultados]
    tiempos = [r["Tiempo (ms)"] for r in resultados]
    
    colores = ["#ffd700" if i == 0 else "#1f77b4" for i in range(len(tiempos))]
    bars = ax.barh(nombres, tiempos, color=colores, edgecolor="black", height=0.6)
    ax.set_xlabel("Tiempo (ms)", fontsize=12)
    ax.set_title(f"Comparación de tiempos - {num_elementos} elementos", fontsize=14, fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    
    for bar, tiempo in zip(bars, tiempos):
        ax.text(bar.get_width() + max(tiempos) * 0.01, bar.get_y() + bar.get_height()/2, 
                f"{tiempo:.2f} ms", va="center", fontsize=10)
    
    st.pyplot(fig)
    plt.close(fig)
    
    # ========== GRÁFICO DE COMPARACIONES ==========
    st.subheader("📊 Comparaciones vs Intercambios")
    
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    
    x = range(len(resultados))
    width = 0.35
    
    comps = [r["Comparaciones"] for r in resultados]
    intercambios = [r["Intercambios"] for r in resultados]
    
    bars1 = ax2.bar([i - width/2 for i in x], comps, width, label='Comparaciones', color='#ff7f0e')
    bars2 = ax2.bar([i + width/2 for i in x], intercambios, width, label='Intercambios', color='#1f77b4')
    
    ax2.set_xlabel('Algoritmo', fontsize=12)
    ax2.set_ylabel('Cantidad', fontsize=12)
    ax2.set_title('Comparaciones vs Intercambios', fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([r["Algoritmo"] for r in resultados], rotation=15, ha='right')
    ax2.legend()
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Agregar valores encima de las barras
    for bar in bars1:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, height + max(comps) * 0.01,
                f'{int(height)}', ha='center', va='bottom', fontsize=8)
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, height + max(intercambios) * 0.01,
                f'{int(height)}', ha='center', va='bottom', fontsize=8)
    
    st.pyplot(fig2)
    plt.close(fig2)
    
    # ========== GRÁFICO DE RADAR ==========
    st.subheader("📊 Perfil de eficiencia")
    
    # Normalizar valores para el radar
    max_tiempo = max(r["Tiempo (ms)"] for r in resultados) if resultados else 1
    max_comps = max(r["Comparaciones"] for r in resultados) if resultados else 1
    max_intercambios = max(r["Intercambios"] for r in resultados) if resultados else 1
    
    fig3, ax3 = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    
    categorias = ['Tiempo\n(menor mejor)', 'Comparaciones\n(menor mejor)', 'Intercambios\n(menor mejor)']
    num_vars = len(categorias)
    
    angulos = [n / float(num_vars) * 2 * 3.14159 for n in range(num_vars)]
    angulos += angulos[:1]
    
    for resultado in resultados:
        valores_radar = [
            1 - (resultado["Tiempo (ms)"] / max_tiempo) if max_tiempo > 0 else 0,
            1 - (resultado["Comparaciones"] / max_comps) if max_comps > 0 else 0,
            1 - (resultado["Intercambios"] / max_intercambios) if max_intercambios > 0 else 0
        ]
        valores_radar += valores_radar[:1]
        ax3.plot(angulos, valores_radar, 'o-', linewidth=2, label=resultado["Algoritmo"])
    
    ax3.set_xticks(angulos[:-1])
    ax3.set_xticklabels(categorias, fontsize=10)
    ax3.set_ylim(0, 1)
    ax3.set_title("Perfil de eficiencia (más cerca del borde = mejor)", fontsize=12, fontweight="bold")
    ax3.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax3.grid(True)
    
    st.pyplot(fig3)
    plt.close(fig3)
    
    # ========== RESUMEN ==========
    st.subheader("📝 Análisis de resultados")
    
    col_analisis1, col_analisis2 = st.columns(2)
    
    with col_analisis1:
        st.markdown("**🏆 Podio de campeones**")
        st.markdown(f"🥇 **1er lugar:** {resultados[0]['Algoritmo']} - {resultados[0]['Tiempo (ms)']:.2f} ms")
        if len(resultados) > 1:
            st.markdown(f"🥈 **2do lugar:** {resultados[1]['Algoritmo']} - {resultados[1]['Tiempo (ms)']:.2f} ms")
        if len(resultados) > 2:
            st.markdown(f"🥉 **3er lugar:** {resultados[2]['Algoritmo']} - {resultados[2]['Tiempo (ms)']:.2f} ms")
    
    with col_analisis2:
        st.markdown("**📊 Estadísticas**")
        st.markdown(f"📋 **Tipo:** {tipo_datos}")
        st.markdown(f"🔢 **Elementos:** {num_elementos}")
        st.markdown(f"⚡ **Algoritmos evaluados:** {len(seleccionados)}")
    
    # ========== COMPARACIÓN TEÓRICA ==========
    with st.expander("📖 Comparación teórica de complejidades"):
        st.markdown("""
        | Algoritmo | Mejor caso | Caso promedio | Peor caso | Espacio | Estable |
        |-----------|------------|---------------|-----------|---------|---------|
        | **Bubble Sort** | O(n) | O(n²) | O(n²) | O(1) | ✅ Sí |
        | **Selection Sort** | O(n²) | O(n²) | O(n²) | O(1) | ❌ No |
        | **Insertion Sort** | O(n) | O(n²) | O(n²) | O(1) | ✅ Sí |
        | **Shell Sort** | O(n log n) | O(n log² n) | O(n²) | O(1) | ❌ No |
        | **Quick Sort** | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ No |
        | **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ Sí |
        | **Counting Sort** | O(n+k) | O(n+k) | O(n+k) | O(k) | ✅ Sí |
        | **Radix Sort** | O(d·n) | O(d·n) | O(d·n) | O(n) | ✅ Sí |
        | **Bucket Sort** | O(n+k) | O(n+k) | O(n²) | O(n+k) | ✅ Sí |
        """)
    
    # ========== BOTÓN LIMPIAR ==========
    if st.button("🗑️ Limpiar resultados", use_container_width=True):
        st.session_state.resultados_ordenamiento = None
        st.session_state.lista_ordenamiento = None
        st.rerun()

# ========== MENSAJE INICIAL ==========
else:
    st.info("👈 **Configura la competencia y presiona 'Iniciar comparación'**")
    
    col_ejemplo1, col_ejemplo2, col_ejemplo3 = st.columns(3)
    with col_ejemplo1:
        st.markdown("""
        ### 💡 ¿Qué hace esta herramienta?
        Ejecuta **todos los algoritmos seleccionados** sobre la **misma lista** y mide:
        - ⏱️ Tiempo de ejecución
        - 🔢 Número de comparaciones
        - 🔄 Número de intercambios
        """)
    with col_ejemplo2:
        st.markdown("""
        ### 🏆 ¿Cómo se determina el ganador?
        El ganador es el algoritmo con **menor tiempo de ejecución**.
        
        En caso de empate, se considera el que tiene **menos comparaciones**.
        """)
    with col_ejemplo3:
        st.markdown("""
        ### 📊 ¿Qué tipo de datos probar?
        - **Aleatoria:** El caso más común
        - **Ordenada:** Mejor caso para Insertion Sort
        - **Inversa:** Peor caso para Quick Sort
        - **Casi ordenada:** Ideal para Shell Sort
        """)

st.markdown("---")
st.caption("🏆 Comparación de algoritmos de ordenamiento | SIS210 - Algoritmos y Estructuras de Datos")