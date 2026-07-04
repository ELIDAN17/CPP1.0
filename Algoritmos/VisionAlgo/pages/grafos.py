import streamlit as st
import time
from algoritmos.grafos import bfs_generator, dfs_generator, dijkstra_generator, prim_generator
from visualizacion.grafo_visual import dibujar_grafo

st.set_page_config(page_title="AlgoVision - Grafos", page_icon="🔗", layout="wide")

st.title("🔗 Simulador de Grafos")
st.markdown("### Aprende cómo funcionan los algoritmos de grafos paso a paso")
st.markdown("---")

# ========== GRAFOS DE EJEMPLO ==========
GRAFOS_EJEMPLO = {
    "🌟 Grafo simple (4 nodos)": {
        "descripcion": "Grafo básico con 4 nodos y 4 aristas. Ideal para entender BFS y DFS.",
        "grafo": {
            "A": [("B", 1), ("C", 2)],
            "B": [("A", 1), ("D", 3)],
            "C": [("A", 2), ("D", 4)],
            "D": [("B", 3), ("C", 4)]
        }
    },
    "🌟 Grafo completo (4 nodos)": {
        "descripcion": "Todos los nodos están conectados entre sí.",
        "grafo": {
            "A": [("B", 2), ("C", 5), ("D", 1)],
            "B": [("A", 2), ("C", 3), ("D", 4)],
            "C": [("A", 5), ("B", 3), ("D", 6)],
            "D": [("A", 1), ("B", 4), ("C", 6)]
        }
    },
    "⭐ Grafo con 6 nodos (RECOMENDADO)": {
        "descripcion": "Grafo más complejo con 6 nodos. Perfecto para ver Dijkstra y PRIM.",
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
    "📊 Grafo con pesos grandes": {
        "descripcion": "Pesos variados para ver cómo Dijkstra elige el camino más corto.",
        "grafo": {
            "A": [("B", 10), ("C", 3)],
            "B": [("A", 10), ("C", 2), ("D", 8)],
            "C": [("A", 3), ("B", 2), ("D", 15), ("E", 5)],
            "D": [("B", 8), ("C", 15), ("E", 1), ("F", 7)],
            "E": [("C", 5), ("D", 1), ("F", 4)],
            "F": [("D", 7), ("E", 4)]
        }
    },
    "🔗 Grafo con 8 nodos": {
        "descripcion": "Grafo más grande con 8 nodos.",
        "grafo": {
            "A": [("B", 3), ("C", 5)],
            "B": [("A", 3), ("D", 2), ("E", 4)],
            "C": [("A", 5), ("F", 6)],
            "D": [("B", 2), ("G", 3)],
            "E": [("B", 4), ("G", 5), ("H", 2)],
            "F": [("C", 6), ("H", 4)],
            "G": [("D", 3), ("E", 5)],
            "H": [("E", 2), ("F", 4)]
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
if "grafo_actual" not in st.session_state:
    st.session_state.grafo_actual = GRAFOS_EJEMPLO["⭐ Grafo con 6 nodos (RECOMENDADO)"]["grafo"]
if "nombre_grafo_actual" not in st.session_state:
    st.session_state.nombre_grafo_actual = "⭐ Grafo con 6 nodos (RECOMENDADO)"
if "generador" not in st.session_state:
    st.session_state.generador = None
if "pasos" not in st.session_state:
    st.session_state.pasos = []
if "paso_actual" not in st.session_state:
    st.session_state.paso_actual = 0
if "auto_ejecutando" not in st.session_state:
    st.session_state.auto_ejecutando = False

# ========== FUNCION PARA DIBUJAR ==========
def dibujar_estado_actual(algoritmo, estado):
    """Dibuja el grafo según el algoritmo y estado."""
    algo_nombre = algoritmo.split(" ")[0]
    
    if algo_nombre in ["BFS", "DFS"]:
        if len(estado) == 5:
            nodo_actual, visitados, camino, estructura, operacion = estado
            return dibujar_grafo(
                st.session_state.grafo_actual,
                nodo_destacado=nodo_actual,
                visitados=visitados,
                camino=camino,
                operacion=operacion
            )
    elif algo_nombre == "Dijkstra":
        if len(estado) == 5:
            nodo_actual, distancias, visitados, camino, operacion = estado
            return dibujar_grafo(
                st.session_state.grafo_actual,
                nodo_destacado=nodo_actual,
                visitados=visitados,
                camino=camino,
                operacion=operacion
            )
    elif algo_nombre == "PRIM":
        if len(estado) == 5:
            nodo_actual, arbol, visitados, aristas, operacion = estado
            return dibujar_grafo(
                st.session_state.grafo_actual,
                nodo_destacado=nodo_actual,
                visitados=visitados,
                arbol=arbol,
                operacion=operacion
            )
    return None

# ========== SIDEBAR ==========
with st.sidebar:
    st.header("🔗 Configuración")
    
    st.markdown("### 📌 Paso 1: Elige un grafo")
    
    nombre_grafo = st.selectbox(
        "Selecciona un ejemplo",
        list(GRAFOS_EJEMPLO.keys()),
        index=1
    )
    
    descripcion = GRAFOS_EJEMPLO[nombre_grafo]["descripcion"]
    st.info(f"💡 {descripcion}")
    
    if st.button("📥 Cargar este grafo", use_container_width=True):
        st.session_state.grafo_actual = GRAFOS_EJEMPLO[nombre_grafo]["grafo"]
        st.session_state.nombre_grafo_actual = nombre_grafo
        st.session_state.pasos = []
        st.session_state.paso_actual = 0
        st.session_state.auto_ejecutando = False
        st.success(f"✅ Grafo cargado correctamente")
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📌 Paso 2: Elige el algoritmo")
    
    algoritmo = st.selectbox(
        "Selecciona un algoritmo",
        ["BFS (Búsqueda en amplitud)", "DFS (Búsqueda en profundidad)", 
         "Dijkstra (Camino mínimo)", "PRIM (Árbol de expansión mínima)"],
        index=0
    )
    
    ayuda_algoritmos = {
        "BFS (Búsqueda en amplitud)": "🔍 Recorre por niveles (cola). Ideal para caminos cortos.",
        "DFS (Búsqueda en profundidad)": "🔍 Explora en profundidad (pila). Útil para laberintos.",
        "Dijkstra (Camino mínimo)": "📏 Encuentra la ruta más corta.",
        "PRIM (Árbol de expansión mínima)": "🌳 Conecta todos los nodos con mínimo peso."
    }
    st.info(ayuda_algoritmos.get(algoritmo, ""))
    
    nodos = list(st.session_state.grafo_actual.keys())
    
    if not nodos:
        st.error("⚠️ El grafo no tiene nodos.")
        nodo_inicio = None
        nodo_fin = None
    else:
        st.markdown("### 📌 Paso 3: Elige los nodos")
        
        nodo_inicio = st.selectbox("🚀 Nodo de inicio", nodos, index=0)
        
        if algoritmo == "Dijkstra (Camino mínimo)":
            nodo_fin = st.selectbox("🎯 Nodo destino", nodos, index=min(1, len(nodos)-1))
        else:
            nodo_fin = None
    
    st.markdown("---")
    
    st.markdown("### 📌 Paso 4: Ejecutar")
    
    if st.button("▶️ EJECUTAR", use_container_width=True, type="primary"):
        if not nodos:
            st.error("⚠️ No hay nodos en el grafo.")
        else:
            algo_nombre = algoritmo.split(" ")[0]
            if algo_nombre == "BFS":
                st.session_state.generador = bfs_generator(st.session_state.grafo_actual, nodo_inicio)
            elif algo_nombre == "DFS":
                st.session_state.generador = dfs_generator(st.session_state.grafo_actual, nodo_inicio)
            elif algo_nombre == "Dijkstra":
                st.session_state.generador = dijkstra_generator(st.session_state.grafo_actual, nodo_inicio, nodo_fin)
            else:
                st.session_state.generador = prim_generator(st.session_state.grafo_actual, nodo_inicio)
            
            st.session_state.pasos = []
            st.session_state.paso_actual = 0
            st.session_state.auto_ejecutando = False
            for estado in st.session_state.generador:
                st.session_state.pasos.append(estado)
            st.success(f"✅ {algo_nombre} ejecutado ({len(st.session_state.pasos)} pasos)")
            st.rerun()
    
    st.markdown("---")
    if st.button("🗑️ Limpiar", use_container_width=True):
        st.session_state.pasos = []
        st.session_state.paso_actual = 0
        st.session_state.auto_ejecutando = False
        st.rerun()

# ========== ÁREA PRINCIPAL ==========
# Mostrar información
col_info1, col_info2, col_info3, col_info4 = st.columns(4)
with col_info1:
    st.markdown(f"**📊 Grafo:** {st.session_state.nombre_grafo_actual}")
with col_info2:
    st.markdown(f"**🔢 Nodos:** {len(st.session_state.grafo_actual)}")
with col_info3:
    st.markdown(f"**🔗 Algoritmo:** {algoritmo.split(' ')[0]}")
with col_info4:
    if 'nodo_inicio' in locals() and nodo_inicio:
        st.markdown(f"**🚀 Inicio:** {nodo_inicio}")

# ========== CONTROLES DE NAVEGACIÓN (MOVIDOS ARRIBA - AQUÍ ESTÁ EL CAMBIO) ==========
if st.session_state.pasos:
    st.markdown("### 🎮 Controles")
    col_prev, col_next, col_auto, col_reset = st.columns(4)
    with col_prev:
        if st.button("⬅️ Anterior", use_container_width=True) and st.session_state.paso_actual > 0:
            st.session_state.paso_actual -= 1
            st.session_state.auto_ejecutando = False
            st.rerun()
    with col_next:
        if st.button("➡️ Siguiente", use_container_width=True) and st.session_state.paso_actual < len(st.session_state.pasos) - 1:
            st.session_state.paso_actual += 1
            st.session_state.auto_ejecutando = False
            st.rerun()
    with col_auto:
        if st.button("▶️ Auto", use_container_width=True):
            st.session_state.auto_ejecutando = True
            st.rerun()
    with col_reset:
        if st.button("🔄 Reiniciar", use_container_width=True):
            st.session_state.paso_actual = 0
            st.session_state.auto_ejecutando = False
            st.rerun()
    
    # ========== BUCLE AUTO ==========
    if st.session_state.auto_ejecutando and st.session_state.paso_actual < len(st.session_state.pasos) - 1:
        time.sleep(0.3)
        st.session_state.paso_actual += 1
        st.rerun()
    elif st.session_state.auto_ejecutando:
        st.session_state.auto_ejecutando = False
        st.success("✅ Animación completada")
        st.rerun()
    
    st.markdown("---")

# ========== CONTENEDOR PARA EL GRÁFICO ==========
grafico_container = st.empty()

# ========== MOSTRAR PASOS ==========
if st.session_state.pasos:
    paso_idx = st.session_state.paso_actual
    if paso_idx < len(st.session_state.pasos):
        estado = st.session_state.pasos[paso_idx]
        fig = dibujar_estado_actual(algoritmo, estado)
        if fig:
            with grafico_container:
                st.plotly_chart(fig, use_container_width=True)
        
        # Mostrar información del paso
        st.info(f"📌 **Paso {paso_idx + 1}/{len(st.session_state.pasos)}:** {estado[-1] if len(estado) >= 4 else 'normal'}")
        
        # Mostrar detalles según algoritmo
        algo_nombre = algoritmo.split(" ")[0]
        if algo_nombre in ["BFS", "DFS"] and len(estado) >= 3:
            # estado[1] = visitados, estado[2] = camino
            st.markdown(f"**Visitados:** {estado[1]}")
            if len(estado) >= 4 and estado[2]:
                camino_str = " → ".join(str(n) for n in estado[2])
                st.markdown(f"**🛤️ Camino:** {camino_str}")
        elif algo_nombre == "Dijkstra" and len(estado) >= 4:
            if estado[3]:  # camino
                camino_str = " → ".join(str(n) for n in estado[3])
                st.markdown(f"**🛤️ Camino:** {camino_str}")
            st.markdown(f"**📏 Distancias:** {estado[1]}")
        elif algo_nombre == "PRIM" and len(estado) >= 4:
            if estado[1]:  # arbol
                arbol_str = " → ".join(f"{u}→{v}({w})" for u, v, w in estado[1])
                st.markdown(f"**🌳 Árbol:** {arbol_str}")

else:
    # Mostrar grafo inicial
    fig = dibujar_grafo(st.session_state.grafo_actual, operacion="normal")
    with grafico_container:
        st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    ### 🚀 ¿Cómo empezar?
    
    1. **En la barra lateral**, elige un grafo
    2. **Presiona "Cargar este grafo"**
    3. **Selecciona un algoritmo** (BFS, DFS, Dijkstra, PRIM)
    4. **Elige el nodo de inicio** (y destino para Dijkstra)
    5. **Presiona "EJECUTAR"**
    6. **Usa "Siguiente"** para ver el recorrido paso a paso
    
    💡 **Recomendación:** Empieza con "Grafo con 6 nodos" y "BFS".
    """)

# ========== LEYENDA ==========
with st.expander("🎨 Leyenda de colores"):
    st.markdown("""
    | Color | Significado |
    |-------|-------------|
    | 🔵 **Azul** | Nodo no visitado |
    | 🟠 **Naranja** | Nodo actual / visitando |
    | 🟢 **Verde** | Nodo visitado |
    | ⚪ **Gris** | Arista normal |
    | 🔴 **Rojo** | Camino recorrido (BFS/DFS/Dijkstra) / Árbol (PRIM) |
    """)

st.markdown("---")
st.caption("🔗 Simulador de grafos | SIS210 - Algoritmos y Estructuras de Datos")