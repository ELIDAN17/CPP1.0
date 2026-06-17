"""
Pestaña de Comparación de Algoritmos de Búsqueda
Ejecuta todos los algoritmos de búsqueda sobre la misma lista.
"""

import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt
from algoritmos.busqueda import (
    busqueda_lineal_generator,
    busqueda_binaria_generator,
    busqueda_interpolacion_generator,
    busqueda_exponencial_generator
)
from utils import lista_aleatoria, lista_ordenada, lista_inversa, lista_casi_ordenada

st.set_page_config(page_title="AlgoVision - Comparación Búsqueda", page_icon="🏆", layout="wide")

st.title("🏆 Comparación de Algoritmos de Búsqueda")
st.markdown("### ¿Cuál algoritmo encuentra el elemento más rápido?")
st.markdown("---")

# ========== SIDEBAR ==========
with st.sidebar:
    st.header("⚙️ Configuración")
    
    tipo_datos = st.selectbox(
        "Tipo de datos",
        ["Ordenada", "Aleatoria", "Inversa", "Casi ordenada"],
        index=0,
        help="Para búsqueda binaria, interpolación y exponencial, la lista debe estar ORDENADA"
    )
    
    num_elementos = st.slider(
        "Cantidad de elementos",
        min_value=10,
        max_value=200,
        value=50,
        step=10
    )
    
    # Rango de valores
    col_min, col_max = st.columns(2)
    with col_min:
        min_valor = st.number_input("Valor mínimo", value=10, step=1)
    with col_max:
        max_valor = st.number_input("Valor máximo", value=200, step=1)
    
    if min_valor >= max_valor:
        st.error("⚠️ El valor mínimo debe ser menor que el máximo")
    
    st.markdown("---")
    
    # Botón para generar lista
    generar_lista = st.button("🔄 Generar lista de prueba", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 🎯 Configurar valor a buscar")
    
    modo_busqueda = st.radio(
        "Modo de búsqueda",
        ["Valor existente", "Valor aleatorio", "Valor personalizado"],
        index=0
    )
    
    if modo_busqueda == "Valor personalizado":
        valor_buscar = st.number_input("Valor a buscar", value=42, step=1)
    else:
        valor_buscar = None
    
    st.markdown("---")
    st.markdown("### Algoritmos participantes")
    
    algoritmos_seleccionados = st.multiselect(
        "Selecciona los algoritmos a comparar",
        ["Búsqueda Lineal", "Búsqueda Binaria", "Búsqueda por Interpolación", "Búsqueda Exponencial"],
        default=["Búsqueda Lineal", "Búsqueda Binaria", "Búsqueda por Interpolación", "Búsqueda Exponencial"]
    )
    
    st.markdown("---")
    ejecutar = st.button("🏁 ¡INICIAR COMPARACIÓN!", use_container_width=True, type="primary")

# ========== DICCIONARIO DE GENERADORES ==========
GENERADORES = {
    "Búsqueda Lineal": busqueda_lineal_generator,
    "Búsqueda Binaria": busqueda_binaria_generator,
    "Búsqueda por Interpolación": busqueda_interpolacion_generator,
    "Búsqueda Exponencial": busqueda_exponencial_generator,
}

def generar_lista_y_valor(tipo, n, min_val, max_val, modo_busqueda, valor_personalizado=None):
    """
    Genera lista según el tipo seleccionado y un valor para buscar.
    """
    # Generar lista
    if tipo == "Aleatoria":
        lista = lista_aleatoria(n, min_val=min_val, max_val=max_val)
    elif tipo == "Ordenada":
        lista = lista_ordenada(n, min_val=min_val, max_val=max_val)
    elif tipo == "Inversa":
        lista = lista_inversa(n, min_val=min_val, max_val=max_val)
    else:  # Casi ordenada
        lista = lista_casi_ordenada(n, min_val=min_val, max_val=max_val)
    
    # Si es ordenada, mantenerla ordenada
    if tipo != "Aleatoria":
        lista.sort()
    
    # Generar valor a buscar
    if modo_busqueda == "Valor personalizado":
        valor = valor_personalizado
        # Si el valor no está en la lista, lo agregamos
        if valor not in lista:
            lista[0] = valor
            if tipo != "Aleatoria":
                lista.sort()
    elif modo_busqueda == "Valor existente":
        import random
        valor = random.choice(lista)
    else:  # "Valor aleatorio"
        import random
        valor = random.randint(min_val, max_val)
    
    return lista, valor

def ejecutar_algoritmo_busqueda(nombre, generador_func, lista, objetivo):
    """
    Ejecuta un algoritmo de búsqueda y mide tiempo, comparaciones y elementos revisados.
    """
    lista_copia = lista.copy()
    inicio = time.time()
    generador = generador_func(lista_copia, objetivo)
    
    comparaciones = 0
    elementos_revisados = 0
    encontrado = False
    posicion = -1
    
    try:
        while True:
            estado = next(generador)
            elementos_revisados += 1
            
            if len(estado) == 4:
                idx_actual = estado[1]
                operacion = estado[3]
            elif len(estado) == 5:
                idx_actual = estado[3]
                operacion = estado[4]
            else:
                operacion = "desconocido"
                idx_actual = -1
            
            if operacion in ["comparing", "buscando", "expandiendo", "actualizando"]:
                comparaciones += 1
            elif operacion == "encontrado":
                encontrado = True
                posicion = idx_actual
                break
            elif operacion == "no_encontrado":
                encontrado = False
                break
    except StopIteration:
        pass
    
    fin = time.time()
    tiempo_ms = (fin - inicio) * 1000
    
    return {
        "nombre": nombre,
        "tiempo_ms": tiempo_ms,
        "comparaciones": comparaciones,
        "elementos_revisados": elementos_revisados,
        "encontrado": encontrado,
        "posicion": posicion,
        "valor_buscado": objetivo
    }

# ========== INICIALIZAR ESTADO ==========
if "lista_generada_busqueda" not in st.session_state:
    st.session_state.lista_generada_busqueda = None
if "valor_generado_busqueda" not in st.session_state:
    st.session_state.valor_generado_busqueda = None
if "resultados_busqueda" not in st.session_state:
    st.session_state.resultados_busqueda = None

# ========== GENERAR LISTA ==========
if generar_lista:
    if min_valor >= max_valor:
        st.error("⚠️ El valor mínimo debe ser menor que el máximo")
    else:
        lista, valor = generar_lista_y_valor(
            tipo_datos, 
            num_elementos, 
            min_valor, 
            max_valor, 
            modo_busqueda, 
            valor_buscar if modo_busqueda == "Valor personalizado" else None
        )
        st.session_state.lista_generada_busqueda = lista
        st.session_state.valor_generado_busqueda = valor
        st.session_state.resultados_busqueda = None
        st.rerun()

# ========== MOSTRAR LISTA GENERADA ==========
if st.session_state.lista_generada_busqueda is not None:
    lista_mostrar = st.session_state.lista_generada_busqueda
    valor_mostrar = st.session_state.valor_generado_busqueda
    
    st.subheader("📋 Lista de prueba generada")
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("Tipo", tipo_datos)
    with col_info2:
        st.metric("Elementos", len(lista_mostrar))
    with col_info3:
        st.metric("Valor a buscar", valor_mostrar)
    
    # Mostrar lista completa con scroll
    st.markdown("**Lista completa:**")
    st.text_area(
        "",
        value=f"[{', '.join(map(str, lista_mostrar))}]",
        height=100,
        disabled=True,
        label_visibility="collapsed"
    )
    
    # Indicar si el valor existe
    if valor_mostrar in lista_mostrar:
        pos = lista_mostrar.index(valor_mostrar)
        st.success(f"✅ El valor **{valor_mostrar}** existe en la lista (posición {pos})")
    else:
        st.warning(f"⚠️ El valor **{valor_mostrar}** NO existe en la lista")
    
    st.markdown("---")

# ========== EJECUTAR COMPARACIÓN ==========
if ejecutar:
    if st.session_state.lista_generada_busqueda is None:
        st.warning("⚠️ Primero genera una lista de prueba con el botón 'Generar lista de prueba'")
    elif not algoritmos_seleccionados:
        st.error("⚠️ Selecciona al menos un algoritmo para comparar")
    else:
        with st.spinner("🔄 Ejecutando todos los algoritmos de búsqueda..."):
            lista_prueba = st.session_state.lista_generada_busqueda.copy()
            valor = st.session_state.valor_generado_busqueda
            
            resultados = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, algo in enumerate(algoritmos_seleccionados):
                status_text.text(f"Ejecutando {algo}...")
                resultado = ejecutar_algoritmo_busqueda(
                    algo, 
                    GENERADORES[algo], 
                    lista_prueba, 
                    valor
                )
                resultados.append(resultado)
                progress_bar.progress((i + 1) / len(algoritmos_seleccionados))
            
            progress_bar.empty()
            status_text.empty()
            
            resultados.sort(key=lambda x: x["tiempo_ms"])
            st.session_state.resultados_busqueda = resultados

# ========== MOSTRAR RESULTADOS ==========
if st.session_state.resultados_busqueda:
    resultados = st.session_state.resultados_busqueda
    lista_original = st.session_state.lista_generada_busqueda
    valor_buscado = st.session_state.valor_generado_busqueda
    
    # ========== TARJETA DEL GANADOR ==========
    ganador = resultados[0]
    
    st.markdown("---")
    col_ganador1, col_ganador2, col_ganador3 = st.columns([1, 2, 1])
    with col_ganador2:
        st.markdown(f"""
        <div style='text-align: center; background: linear-gradient(135deg, #ffd700, #ffb347); 
                    padding: 20px; border-radius: 20px; margin: 10px 0;'>
            <h1 style='margin: 0; font-size: 3em;'>🏆</h1>
            <h2 style='margin: 0; color: #fff;'>ALGORITMO GANADOR</h2>
            <h1 style='margin: 10px 0 0 0; color: #fff; font-size: 2.5em;'>{ganador['nombre']}</h1>
            <p style='margin: 5px 0 0 0; color: #fff; font-size: 1.2em;'>⚡ {ganador['tiempo_ms']:.2f} ms</p>
            <p style='margin: 0; color: #fff;'>Comparaciones: {ganador['comparaciones']}</p>
            <p style='margin: 0; color: #fff;'>Posición: {ganador['posicion'] if ganador['encontrado'] else 'No encontrado'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== TABLA DE RESULTADOS ==========
    st.subheader("📊 Tabla comparativa de resultados")
    
    df = pd.DataFrame(resultados)
    df = df.rename(columns={
        "nombre": "Algoritmo",
        "tiempo_ms": "Tiempo (ms)",
        "comparaciones": "Comparaciones",
        "elementos_revisados": "Elementos revisados",
        "encontrado": "Encontrado",
        "posicion": "Posición"
    })
    
    df["Tiempo (ms)"] = df["Tiempo (ms)"].map(lambda x: f"{x:.2f}")
    df["Encontrado"] = df["Encontrado"].map(lambda x: "✅ Sí" if x else "❌ No")
    df["Posición"] = df["Posición"].map(lambda x: f"Índice {x}" if x != -1 else "N/A")
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # ========== GRÁFICO DE BARRAS (MÁS GRANDE) ==========
    st.subheader("📈 Comparación visual de tiempos")
    
    fig, ax = plt.subplots(figsize=(12, 7))  # Más grande
    
    nombres = [r["nombre"] for r in resultados]
    tiempos = [r["tiempo_ms"] for r in resultados]
    
    colores_barras = []
    for i, tiempo in enumerate(tiempos):
        if i == 0:
            colores_barras.append("#ffd700")
        elif i == 1:
            colores_barras.append("#c0c0c0")
        elif i == 2:
            colores_barras.append("#cd7f32")
        else:
            colores_barras.append("#1f77b4")
    
    bars = ax.barh(nombres, tiempos, color=colores_barras, edgecolor="black", height=0.6)
    ax.set_xlabel("Tiempo (ms)", fontsize=14)
    ax.set_title(f"Comparación de tiempos - {num_elementos} elementos", fontsize=16, fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    
    for bar, tiempo in zip(bars, tiempos):
        ax.text(bar.get_width() + max(tiempos) * 0.01, bar.get_y() + bar.get_height()/2, 
                f"{tiempo:.2f} ms", va="center", fontsize=11)
    
    st.pyplot(fig)
    plt.close(fig)
    
    # ========== GRÁFICO DE EFICIENCIA (MÁS PEQUEÑO) ==========
    st.subheader("📊 Eficiencia: Comparaciones vs Elementos revisados")
    
    fig2, ax2 = plt.subplots(figsize=(8, 5))  # Más pequeño
    
    nombres2 = [r["nombre"] for r in resultados]
    comparaciones = [r["comparaciones"] for r in resultados]
    elementos = [r["elementos_revisados"] for r in resultados]
    
    x = range(len(nombres2))
    width = 0.35
    
    ax2.bar([i - width/2 for i in x], comparaciones, width, label='Comparaciones', color='#ff7f0e')
    ax2.bar([i + width/2 for i in x], elementos, width, label='Elementos revisados', color='#1f77b4')
    
    ax2.set_xlabel('Algoritmo', fontsize=12)
    ax2.set_ylabel('Cantidad', fontsize=12)
    ax2.set_title('Comparaciones vs Elementos revisados', fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(nombres2, rotation=15, ha='right')
    ax2.legend()
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    
    st.pyplot(fig2)
    plt.close(fig2)
    
    # ========== RESUMEN ==========
    st.subheader("📝 Análisis de resultados")
    
    col_analisis1, col_analisis2 = st.columns(2)
    
    with col_analisis1:
        st.markdown("**🏆 Podio de campeones**")
        st.markdown(f"🥇 **1er lugar:** {resultados[0]['nombre']} - {resultados[0]['tiempo_ms']:.2f} ms")
        if len(resultados) > 1:
            st.markdown(f"🥈 **2do lugar:** {resultados[1]['nombre']} - {resultados[1]['tiempo_ms']:.2f} ms")
        if len(resultados) > 2:
            st.markdown(f"🥉 **3er lugar:** {resultados[2]['nombre']} - {resultados[2]['tiempo_ms']:.2f} ms")
    
    with col_analisis2:
        st.markdown("**📊 Estadísticas de la prueba**")
        st.markdown(f"📋 **Tipo:** {tipo_datos}")
        st.markdown(f"🔢 **Elementos:** {num_elementos}")
        st.markdown(f"🎯 **Valor:** {valor_buscado}")
        st.markdown(f"✅ **Existente:** {'Sí' if valor_buscado in lista_original else 'No'}")
    
    # ========== BOTÓN PARA LIMPIAR ==========
    if st.button("🗑️ Limpiar resultados", use_container_width=True):
        st.session_state.resultados_busqueda = None
        st.rerun()

# ========== MENSAJE INICIAL ==========
else:
    st.info("👈 **Configura la competencia y presiona 'Generar lista de prueba' para ver los datos**")
    
    col_ejemplo1, col_ejemplo2, col_ejemplo3 = st.columns(3)
    with col_ejemplo1:
        st.markdown("""
        ### 💡 ¿Qué hace esta herramienta?
        Ejecuta **todos los algoritmos seleccionados** sobre la **misma lista** y mide:
        - ⏱️ Tiempo de ejecución
        - 🔢 Número de comparaciones
        - 📊 Elementos revisados
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
        - **Ordenada:** Mejor caso para binaria/interpolación
        - **Aleatoria:** Búsqueda lineal compite mejor
        - **Inversa:** Prueba de rendimiento
        - **Casi ordenada:** Comportamiento mixto
        """)

# ========== FOOTER ==========
st.markdown("---")
st.caption("🏆 Comparación de algoritmos de búsqueda | SIS210 - Algoritmos y Estructuras de Datos")