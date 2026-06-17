import streamlit as st
from algoritmos.arboles import ArbolABB, ArbolAVL, ArbolRojoNegro, ArbolB, ArbolBMas
from visualizacion.arbol_visual import dibujar_arbol
from visualizacion.info_arbol import mostrar_info_arbol, mostrar_info_nodo
from visualizacion.explicacion_arboles import mostrar_explicacion_metodo

st.set_page_config(page_title="AlgoVision - Árboles", page_icon="🌳", layout="wide")

st.title("🌳 Simulador de Árboles")
st.markdown("---")

# ========== INICIALIZAR ESTADO ==========
if "tipo_arbol" not in st.session_state:
    st.session_state.tipo_arbol = "ABB"
if "arbol" not in st.session_state:
    st.session_state.arbol = ArbolABB()
if "generador" not in st.session_state:
    st.session_state.generador = None
if "pasos" not in st.session_state:
    st.session_state.pasos = []
if "paso_actual" not in st.session_state:
    st.session_state.paso_actual = 0
if "nodo_seleccionado" not in st.session_state:
    st.session_state.nodo_seleccionado = None
if "ultima_operacion" not in st.session_state:
    st.session_state.ultima_operacion = None
if "info_extra" not in st.session_state:
    st.session_state.info_extra = None

# ========== SIDEBAR ==========
with st.sidebar:
    st.header("🌳 Tipo de árbol")
    
    tipo_arbol = st.selectbox(
        "Seleccionar tipo",
        ["ABB", "AVL", "Rojo-Negro", "Árbol B", "Árbol B+"],
        index=0
    )
    
    if tipo_arbol != st.session_state.tipo_arbol:
        st.session_state.tipo_arbol = tipo_arbol
        if tipo_arbol == "ABB":
            st.session_state.arbol = ArbolABB()
        elif tipo_arbol == "AVL":
            st.session_state.arbol = ArbolAVL()
        elif tipo_arbol == "Rojo-Negro":
            st.session_state.arbol = ArbolRojoNegro()
        elif tipo_arbol == "Árbol B":
            st.session_state.arbol = ArbolB(t=3)
        else:
            st.session_state.arbol = ArbolBMas(t=3)
        st.session_state.pasos = []
        st.session_state.paso_actual = 0
        st.session_state.nodo_seleccionado = None
        st.rerun()
    
    st.markdown("---")
    st.header("🎮 Operaciones")
    
    valor = st.number_input("Valor", value=0, step=1)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Insertar", use_container_width=True):
            st.session_state.ultima_operacion = "insertar"
            st.session_state.generador = st.session_state.arbol.insertar(valor)
            st.session_state.pasos = []
            st.session_state.paso_actual = 0
            st.session_state.nodo_seleccionado = None
            st.session_state.info_extra = {"Valor insertado": valor}
            for estado in st.session_state.generador:
                st.session_state.pasos.append(estado)
            st.rerun()
    
    with col2:
        if st.button("🔍 Buscar", use_container_width=True):
            st.session_state.ultima_operacion = "buscar"
            st.session_state.generador = st.session_state.arbol.buscar(valor)
            st.session_state.pasos = []
            st.session_state.paso_actual = 0
            st.session_state.nodo_seleccionado = None
            st.session_state.info_extra = {"Valor buscado": valor}
            for estado in st.session_state.generador:
                st.session_state.pasos.append(estado)
            st.rerun()
    
    with col3:
        if st.button("🗑️ Eliminar", use_container_width=True):
            st.session_state.ultima_operacion = "eliminar"
            st.session_state.generador = st.session_state.arbol.eliminar(valor)
            st.session_state.pasos = []
            st.session_state.paso_actual = 0
            st.session_state.nodo_seleccionado = None
            st.session_state.info_extra = {"Valor eliminado": valor}
            for estado in st.session_state.generador:
                st.session_state.pasos.append(estado)
            st.rerun()
    
    st.markdown("---")
    
    if st.button("🗑️ Limpiar árbol", use_container_width=True):
        if tipo_arbol == "ABB":
            st.session_state.arbol = ArbolABB()
        elif tipo_arbol == "AVL":
            st.session_state.arbol = ArbolAVL()
        elif tipo_arbol == "Rojo-Negro":
            st.session_state.arbol = ArbolRojoNegro()
        elif tipo_arbol == "Árbol B":
            st.session_state.arbol = ArbolB(t=3)
        else:
            st.session_state.arbol = ArbolBMas(t=3)
        st.session_state.pasos = []
        st.session_state.paso_actual = 0
        st.session_state.nodo_seleccionado = None
        st.session_state.info_extra = None
        st.rerun()
    
    st.markdown("---")
    
    # ========== INFO DEL ÁRBOL ==========
    if st.session_state.arbol.raiz:
        info_arbol = mostrar_info_arbol(
            st.session_state.arbol.raiz,
            f"📊 Información del {tipo_arbol}"
        )

# ========== ÁREA PRINCIPAL ==========
st.markdown(f"### 🌳 {tipo_arbol}")

# ========== MOSTRAR ÁRBOL ==========
if st.session_state.pasos:
    paso_idx = st.session_state.paso_actual
    if paso_idx < len(st.session_state.pasos):
        nodo, operacion = st.session_state.pasos[paso_idx]
        
        if operacion in ["encontrado", "insertado", "insertado_izquierdo", "insertado_derecho", "eliminando"]:
            st.session_state.nodo_seleccionado = nodo
        
        # Extraer información del nodo para mostrar en el gráfico
        info_extra_grafico = st.session_state.info_extra.copy() if st.session_state.info_extra else {}
        if nodo and hasattr(nodo, 'valor'):
            info_extra_grafico["Nodo actual"] = nodo.valor
        if paso_idx < len(st.session_state.pasos) - 1:
            info_extra_grafico["Siguiente"] = "→"
        
        fig = dibujar_arbol(
            st.session_state.arbol.raiz, 
            nodo, 
            operacion,
            info_extra_grafico
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Mostrar información del paso
        st.info(f"📌 **Paso {paso_idx + 1}/{len(st.session_state.pasos)}:** {operacion}")
        
        # Mostrar información del nodo destacado
        if nodo and hasattr(nodo, 'valor'):
            with st.expander(f"🔍 Información del nodo {nodo.valor}"):
                mostrar_info_nodo(nodo, st.session_state.arbol.raiz)
        
        # Mostrar explicación del método
        if st.session_state.ultima_operacion:
            with st.expander(f"📖 Explicación de {st.session_state.ultima_operacion}"):
                mostrar_explicacion_metodo(st.session_state.ultima_operacion, st.session_state.tipo_arbol)
    
    # Controles de navegación
    col_prev, col_next, col_reset, col_auto = st.columns(4)
    with col_prev:
        if st.button("⬅️ Anterior", use_container_width=True) and st.session_state.paso_actual > 0:
            st.session_state.paso_actual -= 1
            st.rerun()
    with col_next:
        if st.button("➡️ Siguiente", use_container_width=True) and st.session_state.paso_actual < len(st.session_state.pasos) - 1:
            st.session_state.paso_actual += 1
            st.rerun()
    with col_reset:
        if st.button("🔄 Reiniciar", use_container_width=True):
            st.session_state.paso_actual = 0
            st.session_state.nodo_seleccionado = None
            st.rerun()
    with col_auto:
        if st.button("▶️ Auto", use_container_width=True):
            if st.session_state.paso_actual < len(st.session_state.pasos) - 1:
                for i in range(st.session_state.paso_actual + 1, len(st.session_state.pasos)):
                    st.session_state.paso_actual = i
                    st.rerun()
else:
    # Mostrar árbol vacío o estado actual
    fig = dibujar_arbol(st.session_state.arbol.raiz, None, "normal")
    st.plotly_chart(fig, use_container_width=True)
    
    if st.session_state.arbol.raiz is None:
        st.info("🌱 **Árbol vacío.** Usa Insertar, Buscar o Eliminar para interactuar con el árbol.")
    else:
        st.success(f"✅ Árbol con {len(str(st.session_state.arbol.raiz))} nodos")
        
        with st.expander("📊 Información del árbol"):
            mostrar_info_arbol(st.session_state.arbol.raiz, f"📊 Información del {tipo_arbol}")

# ========== HISTORIAL DE PASOS ==========
if st.session_state.pasos:
    with st.expander("📋 Historial de pasos"):
        for i, (nodo, operacion) in enumerate(st.session_state.pasos):
            valor_nodo = nodo.valor if nodo and hasattr(nodo, 'valor') else "None"
            if i == st.session_state.paso_actual:
                st.markdown(f"**👉 {i+1}. {operacion} - {valor_nodo}**")
            else:
                st.markdown(f"{i+1}. {operacion} - {valor_nodo}")

# ========== LEYENDA DE COLORES ==========
with st.expander("🎨 Leyenda de colores"):
    st.markdown("""
    | Color | Significado |
    |-------|-------------|
    | 🔵 **Azul** | Nodo normal |
    | 🟠 **Naranja** | Nodo visitado / seleccionado |
    | 🟢 **Verde** | Nodo encontrado |
    | 🟣 **Púrpura** | Nodo insertado |
    | 🔴 **Rojo** | Nodo eliminado |
    | 🟦 **Cyan** | Nodo reemplazado / balanceado |
    | 🟪 **Morado** | Rotación |
    | ⚫ **Negro** | Raíz (Rojo-Negro) |
    | 🔴 **Rojo claro** | Nodo rojo (Rojo-Negro) |
    """)