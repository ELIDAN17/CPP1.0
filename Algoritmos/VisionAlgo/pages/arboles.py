import streamlit as st
import time  # <--- IMPORTANTE: para el delay en Auto
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
if "resultado_recorrido" not in st.session_state:
    st.session_state.resultado_recorrido = []

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
            st.session_state.resultado_recorrido = []
            for estado in st.session_state.generador:
                st.session_state.pasos.append(estado)
            st.rerun()
    
    with col2:
        if st.button("🔍 Buscar", use_container_width=True):
            st.session_state.ultima_operacion = "buscar"
            st.session_state.generador = st.session_state.arbol.buscar(valor)
            st.session_state.pasos = []
            st.session_state.paso_actual = 0
            st.session_state.resultado_recorrido = []
            for estado in st.session_state.generador:
                st.session_state.pasos.append(estado)
            st.rerun()
    
    with col3:
        if st.button("🗑️ Eliminar", use_container_width=True):
            st.session_state.ultima_operacion = "eliminar"
            st.session_state.generador = st.session_state.arbol.eliminar(valor)
            st.session_state.pasos = []
            st.session_state.paso_actual = 0
            st.session_state.resultado_recorrido = []
            for estado in st.session_state.generador:
                st.session_state.pasos.append(estado)
            st.rerun()
    
    st.markdown("---")
    
    # ========== RECORRIDOS (SOLO PARA ÁRBOLES BINARIOS) ==========
    if tipo_arbol in ["ABB", "AVL", "Rojo-Negro"]:
        st.markdown("### 🔄 Recorridos")
        
        recorrido = st.selectbox(
            "Tipo de recorrido",
            ["In-Order", "Pre-Order", "Post-Order", "BFS (por niveles)"],
            index=0
        )
        
        if st.button("▶️ Ejecutar recorrido", use_container_width=True):
            st.session_state.ultima_operacion = "recorrido"
            if recorrido == "In-Order":
                st.session_state.generador = st.session_state.arbol.in_order()
            elif recorrido == "Pre-Order":
                st.session_state.generador = st.session_state.arbol.pre_order()
            elif recorrido == "Post-Order":
                st.session_state.generador = st.session_state.arbol.post_order()
            else:
                st.session_state.generador = st.session_state.arbol.bfs()
            
            st.session_state.pasos = []
            st.session_state.paso_actual = 0
            st.session_state.resultado_recorrido = []
            for estado in st.session_state.generador:
                st.session_state.pasos.append(estado)
                if len(estado) >= 3:
                    st.session_state.resultado_recorrido.append(estado[0].valor)
            st.rerun()
    else:
        # Mensaje informativo para árboles B
        st.info("ℹ️ Los árboles B y B+ no tienen recorridos tradicionales (in-order, pre-order, post-order) porque son estructuras multi-clave. En su lugar, usa la búsqueda y visualización.")
    
    st.markdown("---")
    
    # ========== BOTÓN LIMPIAR ==========
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
        st.session_state.resultado_recorrido = []
        st.rerun()
    
    st.markdown("---")
    
    # ========== INFORMACIÓN DEL ÁRBOL ==========
    if st.session_state.arbol.raiz:
        mostrar_info_arbol(st.session_state.arbol.raiz, f"📊 Información del {tipo_arbol}")

# ========== ÁREA PRINCIPAL ==========
st.markdown(f"### 🌳 {tipo_arbol}")

# ========== CONTROLES DE NAVEGACIÓN (MOVIDOS ARRIBA - AQUÍ ESTÁ EL CAMBIO) ==========
if st.session_state.pasos:
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
            st.rerun()
    with col_auto:
        if st.button("▶️ Auto", use_container_width=True):
            if st.session_state.paso_actual < len(st.session_state.pasos) - 1:
                # Crear un contenedor para la animación
                contenedor = st.empty()
                
                # Reproducir todos los pasos automáticamente
                for i in range(st.session_state.paso_actual + 1, len(st.session_state.pasos)):
                    st.session_state.paso_actual = i
                    
                    # Obtener el paso actual
                    paso = st.session_state.pasos[i]
                    if len(paso) == 3:
                        nodo, operacion, info = paso
                    else:
                        nodo, operacion = paso
                        info = {"mensaje": operacion}
                    
                    # Dibujar el árbol en el contenedor
                    with contenedor:
                        fig = dibujar_arbol(st.session_state.arbol.raiz, nodo, operacion, info)
                        st.plotly_chart(fig, use_container_width=True, key=f"auto_{i}")
                        mensaje = info.get("mensaje", operacion)
                        st.info(f"📌 **Paso {i + 1}/{len(st.session_state.pasos)}:** {mensaje}")
                    
                    # Pausa para ver la animación
                    time.sleep(0.3)
                
                # Limpiar el contenedor y mostrar el último paso
                contenedor.empty()
                st.session_state.paso_actual = len(st.session_state.pasos) - 1
                st.success("✅ Animación completada")
                st.rerun()
            else:
                st.warning("⚠️ Ya estás en el último paso")

# ========== MOSTRAR RESULTADO DEL RECORRIDO ==========
if st.session_state.resultado_recorrido and tipo_arbol in ["ABB", "AVL", "Rojo-Negro"]:
    st.markdown(f"**📋 Orden de visita ({recorrido}):**")
    st.markdown(f"```\n{st.session_state.resultado_recorrido}\n```")

# ========== MOSTRAR ÁRBOL ==========
if st.session_state.pasos:
    paso_idx = st.session_state.paso_actual
    if paso_idx < len(st.session_state.pasos):
        # Extraer información del paso
        if len(st.session_state.pasos[paso_idx]) == 3:
            nodo, operacion, info = st.session_state.pasos[paso_idx]
        else:
            nodo, operacion = st.session_state.pasos[paso_idx]
            info = {"mensaje": operacion}
        
        if operacion in ["encontrado", "insertado", "insertado_izquierdo", "insertado_derecho", "eliminando"]:
            st.session_state.nodo_seleccionado = nodo
        
        # Dibujar árbol
        fig = dibujar_arbol(st.session_state.arbol.raiz, nodo, operacion, info)
        st.plotly_chart(fig, use_container_width=True)
        
        # Mostrar información del paso
        mensaje = info.get("mensaje", operacion)
        st.info(f"📌 **Paso {paso_idx + 1}/{len(st.session_state.pasos)}:** {mensaje}")
        
        # Mostrar información del nodo destacado
        if nodo and hasattr(nodo, 'valor'):
            with st.expander(f"🔍 Información del nodo {nodo.valor}"):
                mostrar_info_nodo(nodo, st.session_state.arbol.raiz)
        
        # Mostrar explicación del método
        if st.session_state.ultima_operacion and st.session_state.ultima_operacion != "recorrido":
            with st.expander(f"📖 Explicación de {st.session_state.ultima_operacion}"):
                mostrar_explicacion_metodo(st.session_state.ultima_operacion, st.session_state.tipo_arbol)
else:
    # Mostrar árbol vacío o estado actual
    fig = dibujar_arbol(st.session_state.arbol.raiz, None, "normal", {"mensaje": "Árbol actual"})
    st.plotly_chart(fig, use_container_width=True)
    
    if st.session_state.arbol.raiz is None:
        st.info("🌱 **Árbol vacío.** Usa Insertar para comenzar a construir el árbol.")
    else:
        st.success(f"✅ Árbol con {st.session_state.arbol.tamaño()} nodos")

# ========== HISTORIAL ==========
if st.session_state.pasos:
    with st.expander("📋 Historial de pasos"):
        for i, paso in enumerate(st.session_state.pasos):
            if len(paso) == 3:
                nodo, operacion, info = paso
                valor_nodo = nodo.valor if nodo and hasattr(nodo, 'valor') else "None"
                mensaje = info.get("mensaje", operacion)
            else:
                nodo, operacion = paso
                valor_nodo = nodo.valor if nodo and hasattr(nodo, 'valor') else "None"
                mensaje = operacion
            
            if i == st.session_state.paso_actual:
                st.markdown(f"**👉 {i+1}. {mensaje} - {valor_nodo}**")
            else:
                st.markdown(f"{i+1}. {mensaje} - {valor_nodo}")

# ========== LEYENDA ==========
with st.expander("🎨 Leyenda de colores"):
    st.markdown("""
    | Color | Significado |
    |-------|-------------|
    | 🔵 **Azul** | Nodo normal |
    | 🟠 **Naranja** | Nodo visitado / seleccionado |
    | 🟢 **Verde** | Nodo encontrado |
    | 🟣 **Púrpura** | Nodo insertado |
    | 🔴 **Rojo** | Nodo eliminado |
    | 🟦 **Cian** | Nodo en recorrido |
    """)