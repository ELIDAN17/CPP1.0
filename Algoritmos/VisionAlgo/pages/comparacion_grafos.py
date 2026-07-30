"""
Pestaña de Comparación de Algoritmos de Grafos
Ejecuta todos los algoritmos de grafos sobre el mismo grafo y compara estadísticas.
"""

import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt
from algoritmos.grafos import bfs_generator, dfs_generator, dijkstra_generator, prim_generator
from visualizacion.grafo_visual import dibujar_grafo

st.set_page_config(page_title="AlgoVision - Comparación Grafos", page_icon="🏆", layout="wide")

st.title("🏆 Comparación de Algoritmos de Grafos")
st.markdown("### ¿Cuál algoritmo recorre el grafo más eficientemente?")
st.markdown("---")

# ========== GRAFOS DE EJEMPLO ==========
GRAFOS_EJEMPLO = {
    "🌟 Grafo simple (4 nodos)": {
        "descripcion": "Grafo básico con 4 nodos y 4 aristas.",
        "grafo": {
            "A": [("B", 1), ("C", 2)],
            "B": [("A", 1), ("D", 3)],
            "C": [("A", 2), ("D", 4)],
            "D": [("B", 3), ("C", 4)]
        }
    },
    "⭐ Grafo con 6 nodos (RECOMENDADO)": {
        "descripcion": "Grafo más complejo con 6 nodos. Perfecto para comparar todos los algoritmos.",
        "grafo": {
            "A": [("B", 4), ("C", 2)],
            "B": [("A", 4), ("C", 1), ("D", 5)],
            "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
            "D": [("B", 5), ("C", 8), ("E", 2), ("F", 6)],
            "E": [("C", 10), ("D", 2), ("F", 3)],
            "F": [("D", 6), ("E", 3)]
        }
    },
    "🌳 Grafo en árbol": {
        "descripcion": "Estructura jerárquica sin ciclos.",
        "grafo": {
            "A": [("B", 1), ("C", 2)],
            "B": [("A", 1), ("D", 3), ("E", 4)],
            "C": [("A", 2), ("F", 5)],
            "D": [("B", 3)],
            "E": [("B", 4)],
            "F": [("C", 5)]
        }
    },
    "🚀 Grafo con 10 nodos (DESAFÍO)": {
        "descripcion": "Grafo grande con 10 nodos y muchas conexiones.",
        "grafo": {
            "A": [("B", 2), ("C", 4), ("D", 1)],
            "B": [("A", 2), ("E", 3), ("F", 5)],
            "C": [("A", 4), ("G", 2), ("H", 6)],
            "D": [("A", 1), ("I", 4)],
            "E": [("B", 3), ("J", 2)],
            "F": [("B", 5), ("G", 1), ("J", 3)],
            "G": [("C", 2), ("F", 1), ("H", 3)],
            "H": [("C", 6), ("G", 3), ("I", 2)],
            "I": [("D", 4), ("H", 2), ("J", 5)],
            "J": [("E", 2), ("F", 3), ("I", 5)]
        }
    }
}

# ========== INICIALIZAR ESTADO ==========
if "grafo_comparacion" not in st.session_state:
    st.session_state.grafo_comparacion = None
if "resultados_grafos" not in st.session_state:
    st.session_state.resultados_grafos = None

# ========== SIDEBAR ==========
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Seleccionar grafo
    st.markdown("### 📊 Grafo de prueba")
    
    nombre_grafo = st.selectbox(
        "Selecciona un grafo",
        list(GRAFOS_EJEMPLO.keys()),
        index=1
    )
    
    descripcion = GRAFOS_EJEMPLO[nombre_grafo]["descripcion"]
    st.info(f"💡 {descripcion}")
    
    if st.button("📥 Cargar grafo", use_container_width=True):
        st.session_state.grafo_comparacion = GRAFOS_EJEMPLO[nombre_grafo]["grafo"]
        st.session_state.resultados_grafos = None
        st.success(f"✅ Grafo cargado correctamente")
        st.rerun()
    
    st.markdown("---")
    
    # Nodo de inicio
    if st.session_state.grafo_comparacion:
        nodos = list(st.session_state.grafo_comparacion.keys())
        nodo_inicio = st.selectbox("🚀 Nodo de inicio", nodos, index=0)
        nodo_destino = st.selectbox("🎯 Nodo destino (para Dijkstra)", nodos, index=min(1, len(nodos)-1))
    else:
        nodo_inicio = None
        nodo_destino = None
    
    st.markdown("---")
    st.markdown("### Algoritmos a comparar")
    
    algoritmos_seleccionados = st.multiselect(
        "Selecciona los algoritmos",
        ["BFS", "DFS", "Dijkstra", "PRIM"],
        default=["BFS", "DFS", "Dijkstra", "PRIM"]
    )
    
    st.markdown("---")
    ejecutar = st.button("🏁 ¡INICIAR COMPARACIÓN!", use_container_width=True, type="primary")

# ========== FUNCIONES ==========
def ejecutar_algoritmo_grafo(nombre, generador, grafo, inicio, destino=None):
    """Ejecuta un algoritmo de grafos y mide estadísticas."""
    inicio_tiempo = time.time()
    
    visitados = []
    camino = []
    pasos = 0
    nodos_visitados = 0
    
    try:
        if nombre == "Dijkstra":
            gen = generador(grafo, inicio, destino)
        else:
            gen = generador(grafo, inicio)
        
        for estado in gen:
            pasos += 1
            if len(estado) >= 2:
                # Extraer información según el algoritmo
                if nombre in ["BFS", "DFS"]:
                    if len(estado) >= 3:
                        if isinstance(estado[1], list):
                            visitados = estado[1]
                        if len(estado) >= 4 and isinstance(estado[2], list):
                            camino = estado[2]
                elif nombre == "Dijkstra":
                    if len(estado) >= 4:
                        if isinstance(estado[2], list):
                            visitados = estado[2]
                        if len(estado) >= 5 and isinstance(estado[3], list):
                            camino = estado[3]
                elif nombre == "PRIM":
                    if len(estado) >= 3:
                        if isinstance(estado[2], list):
                            visitados = estado[2]
        
        nodos_visitados = len(set(visitados)) if visitados else 0
        
    except Exception as e:
        st.warning(f"⚠️ Error en {nombre}: {e}")
        return {
            "nombre": nombre,
            "tiempo_ms": 0,
            "pasos": 0,
            "nodos_visitados": 0,
            "camino": [],
            "visitados": []
        }
    
    fin_tiempo = time.time()
    tiempo_ms = (fin_tiempo - inicio_tiempo) * 1000
    
    return {
        "nombre": nombre,
        "tiempo_ms": tiempo_ms,
        "pasos": pasos,
        "nodos_visitados": nodos_visitados,
        "camino": camino,
        "visitados": visitados
    }

# ========== GENERADORES ==========
GENERADORES = {
    "BFS": bfs_generator,
    "DFS": dfs_generator,
    "Dijkstra": dijkstra_generator,
    "PRIM": prim_generator,
}

# ========== EJECUTAR COMPARACIÓN ==========
if ejecutar:
    if st.session_state.grafo_comparacion is None:
        st.warning("⚠️ Primero carga un grafo con el botón 'Cargar grafo'")
    elif not algoritmos_seleccionados:
        st.error("⚠️ Selecciona al menos un algoritmo para comparar")
    else:
        with st.spinner("🔄 Ejecutando algoritmos..."):
            grafo = st.session_state.grafo_comparacion
            resultados = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, algo in enumerate(algoritmos_seleccionados):
                status_text.text(f"Ejecutando {algo}...")
                resultado = ejecutar_algoritmo_grafo(
                    algo, 
                    GENERADORES[algo], 
                    grafo, 
                    nodo_inicio, 
                    nodo_destino
                )
                resultados.append(resultado)
                progress_bar.progress((i + 1) / len(algoritmos_seleccionados))
            
            progress_bar.empty()
            status_text.empty()
            
            resultados.sort(key=lambda x: x["tiempo_ms"])
            st.session_state.resultados_grafos = resultados

# ========== MOSTRAR RESULTADOS ==========
if st.session_state.resultados_grafos:
    resultados = st.session_state.resultados_grafos
    grafo = st.session_state.grafo_comparacion
    
    # ========== MOSTRAR INFORMACIÓN DEL GRAFO ==========
    st.subheader("📋 Grafo de prueba")
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("Nodos", len(grafo))
    with col_info2:
        aristas = sum(len(v) for v in grafo.values()) // 2
        st.metric("Aristas", aristas)
    with col_info3:
        st.metric("Nodo inicio", nodo_inicio)
    
    # Mostrar estructura del grafo
    with st.expander("📊 Ver estructura del grafo"):
        st.json(grafo)
    
    st.markdown("---")
    
    # ========== TARJETA DEL GANADOR ==========
    ganador = resultados[0]
    
    col_ganador1, col_ganador2, col_ganador3 = st.columns([1, 2, 1])
    with col_ganador2:
        st.markdown(f"""
        <div style='text-align: center; background: linear-gradient(135deg, #ffd700, #ffb347); 
                    padding: 20px; border-radius: 20px; margin: 10px 0;'>
            <h1 style='margin: 0; font-size: 3em;'>🏆</h1>
            <h2 style='margin: 0; color: #fff;'>ALGORITMO GANADOR</h2>
            <h1 style='margin: 10px 0 0 0; color: #fff; font-size: 2.5em;'>{ganador['nombre']}</h1>
            <p style='margin: 5px 0 0 0; color: #fff; font-size: 1.2em;'>⚡ {ganador['tiempo_ms']:.2f} ms</p>
            <p style='margin: 0; color: #fff;'>Pasos: {ganador['pasos']} | Nodos visitados: {ganador['nodos_visitados']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== TABLA DE RESULTADOS ==========
    st.subheader("📊 Tabla comparativa de resultados")
    
    df = pd.DataFrame(resultados)
    df = df.rename(columns={
        "nombre": "Algoritmo",
        "tiempo_ms": "Tiempo (ms)",
        "pasos": "Pasos",
        "nodos_visitados": "Nodos visitados",
        "camino": "Camino encontrado"
    })
    
    df["Tiempo (ms)"] = df["Tiempo (ms)"].map(lambda x: f"{x:.2f}")
    df["Camino encontrado"] = df["Camino encontrado"].map(
        lambda x: " → ".join(str(n) for n in x) if x else "No encontrado"
    )
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # ========== GRÁFICO DE BARRAS ==========
    st.subheader("📈 Comparación visual de tiempos")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
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
    ax.set_xlabel("Tiempo (ms)", fontsize=12)
    ax.set_title("Comparación de tiempos de ejecución", fontsize=14, fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    
    for bar, tiempo in zip(bars, tiempos):
        ax.text(bar.get_width() + max(tiempos) * 0.01, bar.get_y() + bar.get_height()/2, 
                f"{tiempo:.2f} ms", va="center", fontsize=10)
    
    st.pyplot(fig)
    plt.close(fig)
    
    # ========== GRÁFICO DE EFICIENCIA ==========
    st.subheader("📊 Eficiencia: Pasos vs Nodos visitados")
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    
    nombres2 = [r["nombre"] for r in resultados]
    pasos = [r["pasos"] for r in resultados]
    nodos = [r["nodos_visitados"] for r in resultados]
    
    x = range(len(nombres2))
    width = 0.35
    
    ax2.bar([i - width/2 for i in x], pasos, width, label='Pasos', color='#ff7f0e')
    ax2.bar([i + width/2 for i in x], nodos, width, label='Nodos visitados', color='#1f77b4')
    
    ax2.set_xlabel('Algoritmo', fontsize=12)
    ax2.set_ylabel('Cantidad', fontsize=12)
    ax2.set_title('Pasos vs Nodos visitados', fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(nombres2, rotation=15, ha='right')
    ax2.legend()
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Agregar valores encima de las barras
    for bar in ax2.patches:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, height + 0.5,
                f'{int(height)}', ha='center', va='bottom', fontsize=8)
    
    st.pyplot(fig2)
    plt.close(fig2)
    
    # ========== GRÁFICO DE RADAR ==========
    st.subheader("📊 Perfil de eficiencia")
    
    max_tiempo = max(r["tiempo_ms"] for r in resultados) if resultados else 1
    max_pasos = max(r["pasos"] for r in resultados) if resultados else 1
    max_nodos = max(r["nodos_visitados"] for r in resultados) if resultados else 1
    
    fig3, ax3 = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    
    categorias = ['Tiempo\n(menor mejor)', 'Pasos\n(menor mejor)', 'Nodos\n(menor mejor)']
    num_vars = len(categorias)
    
    angulos = [n / float(num_vars) * 2 * 3.14159 for n in range(num_vars)]
    angulos += angulos[:1]
    
    for resultado in resultados:
        valores_radar = [
            1 - (resultado["tiempo_ms"] / max_tiempo) if max_tiempo > 0 else 0,
            1 - (resultado["pasos"] / max_pasos) if max_pasos > 0 else 0,
            1 - (resultado["nodos_visitados"] / max_nodos) if max_nodos > 0 else 0
        ]
        valores_radar += valores_radar[:1]
        ax3.plot(angulos, valores_radar, 'o-', linewidth=2, label=resultado["nombre"])
    
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
        st.markdown(f"🥇 **1er lugar:** {resultados[0]['nombre']} - {resultados[0]['tiempo_ms']:.2f} ms")
        if len(resultados) > 1:
            st.markdown(f"🥈 **2do lugar:** {resultados[1]['nombre']} - {resultados[1]['tiempo_ms']:.2f} ms")
        if len(resultados) > 2:
            st.markdown(f"🥉 **3er lugar:** {resultados[2]['nombre']} - {resultados[2]['tiempo_ms']:.2f} ms")
    
    with col_analisis2:
        st.markdown("**📊 Estadísticas de la prueba**")
        st.markdown(f"📋 **Nodos:** {len(grafo)}")
        st.markdown(f"🔢 **Aristas:** {sum(len(v) for v in grafo.values()) // 2}")
        st.markdown(f"🚀 **Inicio:** {nodo_inicio}")
        if nodo_destino:
            st.markdown(f"🎯 **Destino:** {nodo_destino}")
    
    # ========== COMPARACIÓN TEÓRICA ==========
    with st.expander("📖 Comparación teórica de complejidades"):
        st.markdown("""
        | Algoritmo | Tiempo | Espacio | Uso principal |
        |-----------|--------|---------|---------------|
        | **BFS** | O(V + E) | O(V) | Camino más corto (sin pesos) |
        | **DFS** | O(V + E) | O(V) | Laberintos, detección de ciclos |
        | **Dijkstra** | O((V + E) log V) | O(V) | Camino más corto (con pesos) |
        | **PRIM** | O((V + E) log V) | O(V) | Árbol de expansión mínima |
        """)
    
    # ========== BOTÓN LIMPIAR ==========
    if st.button("🗑️ Limpiar resultados", use_container_width=True):
        st.session_state.resultados_grafos = None
        st.rerun()

# ========== MENSAJE INICIAL ==========
else:
    st.info("👈 **Configura la competencia y presiona 'Cargar grafo'**")
    
    col_ejemplo1, col_ejemplo2, col_ejemplo3 = st.columns(3)
    with col_ejemplo1:
        st.markdown("""
        ### 💡 ¿Qué hace esta herramienta?
        Ejecuta **todos los algoritmos seleccionados** sobre el **mismo grafo** y mide:
        - ⏱️ Tiempo de ejecución
        - 📊 Pasos realizados
        - 🔢 Nodos visitados
        """)
    with col_ejemplo2:
        st.markdown("""
        ### 🏆 ¿Cómo se determina el ganador?
        El ganador es el algoritmo con **menor tiempo de ejecución**.
        
        En caso de empate, se considera el que tiene **menos pasos**.
        """)
    with col_ejemplo3:
        st.markdown("""
        ### 📊 ¿Qué tipo de grafos probar?
        - **Grafo simple:** Para empezar
        - **Grafo con 6 nodos:** Más completo
        - **Grafo en árbol:** Estructura jerárquica
        - **Grafo con 10 nodos:** Rendimiento
        """)

# ========== FOOTER ==========
st.markdown("---")
st.caption("🏆 Comparación de algoritmos de grafos | SIS210 - Algoritmos y Estructuras de Datos")