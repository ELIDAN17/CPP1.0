import streamlit as st
import time
from algoritmos.busqueda import (
    busqueda_lineal_generator,
    busqueda_binaria_generator,
    busqueda_interpolacion_generator,
    busqueda_exponencial_generator
)
from visualizacion.busqueda_visual import dibujar_busqueda
from utils import lista_aleatoria, lista_ordenada, lista_inversa, lista_casi_ordenada

st.set_page_config(page_title="AlgoVision - Búsqueda", page_icon="🔍", layout="wide")

# ========== INICIALIZAR ESTADO ==========
if "lista" not in st.session_state:
    st.session_state.lista = lista_ordenada(15)
if "objetivo" not in st.session_state:
    st.session_state.objetivo = 42
if "generador" not in st.session_state:
    st.session_state.generador = None
if "terminado" not in st.session_state:
    st.session_state.terminado = False
if "ejecutando" not in st.session_state:
    st.session_state.ejecutando = False
if "info_texto" not in st.session_state:
    st.session_state.info_texto = "📋 Listo para comenzar"
if "paso_actual" not in st.session_state:
    st.session_state.paso_actual = 0

# Estado del gráfico (como en ordenamiento)
if "idx_actual" not in st.session_state:
    st.session_state.idx_actual = -1
if "izquierda" not in st.session_state:
    st.session_state.izquierda = -1
if "derecha" not in st.session_state:
    st.session_state.derecha = -1
if "medio" not in st.session_state:
    st.session_state.medio = -1
if "operacion" not in st.session_state:
    st.session_state.operacion = "normal"
if "encontrado" not in st.session_state:
    st.session_state.encontrado = False

st.title("🔍 Simulador de Algoritmos de Búsqueda")
st.markdown("---")

# ========== SIDEBAR ==========
with st.sidebar:
    st.header("🎮 Controles")
    
    algoritmo = st.selectbox(
        "Algoritmo",
        ["Búsqueda Lineal", "Búsqueda Binaria", "Búsqueda por Interpolación", "Búsqueda Exponencial"],
        index=0
    )
    
    num_elementos = st.slider("Cantidad de elementos", 5, 25, 15, 5)
    st.session_state.objetivo = st.number_input("Valor a buscar", value=42, step=1)
    
    tipo_datos = st.selectbox(
        "Tipo de datos",
        ["Ordenada", "Aleatoria", "Inversa", "Casi ordenada"],
        index=0
    )
    
    if algoritmo == "Búsqueda Lineal":
        st.info("✅ La lista NO necesita estar ordenada")
    else:
        st.warning("⚠️ La lista DEBE estar ordenada para este algoritmo")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔄 Nueva lista", width="stretch"):
            if tipo_datos == "Aleatoria":
                nueva_lista = lista_aleatoria(num_elementos, min_val=10, max_val=200)
            elif tipo_datos == "Ordenada":
                nueva_lista = lista_ordenada(num_elementos, min_val=10, max_val=200)
            elif tipo_datos == "Inversa":
                nueva_lista = lista_inversa(num_elementos, min_val=10, max_val=200)
            else:
                nueva_lista = lista_casi_ordenada(num_elementos, min_val=10, max_val=200)
            
            st.session_state.lista = nueva_lista
            st.session_state.generador = None
            st.session_state.terminado = False
            st.session_state.ejecutando = False
            st.session_state.info_texto = "📋 Nueva lista generada"
            st.session_state.paso_actual = 0
            st.session_state.idx_actual = -1
            st.session_state.izquierda = -1
            st.session_state.derecha = -1
            st.session_state.medio = -1
            st.session_state.operacion = "normal"
            st.session_state.encontrado = False
            st.rerun()
    
    with col_btn2:
        if st.button("🔄 Reiniciar", width="stretch"):
            st.session_state.generador = None
            st.session_state.terminado = False
            st.session_state.ejecutando = False
            st.session_state.info_texto = "📋 Reiniciado"
            st.session_state.paso_actual = 0
            st.session_state.idx_actual = -1
            st.session_state.izquierda = -1
            st.session_state.derecha = -1
            st.session_state.medio = -1
            st.session_state.operacion = "normal"
            st.session_state.encontrado = False
            st.rerun()

# ========== FUNCIONES ==========
def obtener_generador(algo, lista, objetivo):
    if algo == "Búsqueda Lineal":
        return busqueda_lineal_generator(lista, objetivo)
    elif algo == "Búsqueda Binaria":
        return busqueda_binaria_generator(lista, objetivo)
    elif algo == "Búsqueda por Interpolación":
        return busqueda_interpolacion_generator(lista, objetivo)
    elif algo == "Búsqueda Exponencial":
        return busqueda_exponencial_generator(lista, objetivo)
    else:
        return busqueda_lineal_generator(lista, objetivo)

def actualizar_estado(estado):
    """Actualiza el estado de sesión con el estado del generador"""
    if len(estado) == 4:
        lista, idx_actual, idx_encontrado, operacion = estado
        st.session_state.lista = lista
        st.session_state.idx_actual = idx_actual
        st.session_state.izquierda = -1
        st.session_state.derecha = -1
        st.session_state.medio = -1
        st.session_state.operacion = operacion
        st.session_state.paso_actual += 1
        
        if operacion == "buscando":
            st.session_state.info_texto = f"🔍 Revisando posición {idx_actual}: valor = {lista[idx_actual]}"
            st.session_state.encontrado = False
        elif operacion == "encontrado":
            st.session_state.info_texto = f"✅ ¡ENCONTRADO! Posición {idx_actual}, valor = {lista[idx_actual]}"
            st.session_state.encontrado = True
            st.session_state.terminado = True
            st.session_state.ejecutando = False
        elif operacion == "no_encontrado":
            st.session_state.info_texto = "❌ Elemento no encontrado"
            st.session_state.encontrado = False
            st.session_state.terminado = True
            st.session_state.ejecutando = False
        else:
            st.session_state.info_texto = f"⚙️ {operacion}"
            st.session_state.encontrado = False
        return True
    
    elif len(estado) == 5:
        lista, izquierda, derecha, medio, operacion = estado
        st.session_state.lista = lista
        st.session_state.idx_actual = medio
        st.session_state.izquierda = izquierda
        st.session_state.derecha = derecha
        st.session_state.medio = medio
        st.session_state.operacion = operacion
        st.session_state.paso_actual += 1
        
        if operacion == "buscando":
            st.session_state.info_texto = f"🔍 Revisando posición {medio}: valor = {lista[medio]}"
            st.session_state.encontrado = False
        elif operacion == "encontrado":
            st.session_state.info_texto = f"✅ ¡ENCONTRADO! Posición {medio}, valor = {lista[medio]}"
            st.session_state.encontrado = True
            st.session_state.terminado = True
            st.session_state.ejecutando = False
        elif operacion == "no_encontrado":
            st.session_state.info_texto = "❌ Elemento no encontrado"
            st.session_state.encontrado = False
            st.session_state.terminado = True
            st.session_state.ejecutando = False
        else:
            st.session_state.info_texto = f"⚙️ {operacion}: rango [{izquierda}...{derecha}]"
            st.session_state.encontrado = False
        return True
    
    return False

# ========== INFORMACIÓN ==========
col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    st.markdown(f"**🔍 Algoritmo:** {algoritmo}")
with col_info2:
    st.markdown(f"**🎯 Buscando:** {st.session_state.objetivo}")
with col_info3:
    st.markdown(f"**📏 Elementos:** {len(st.session_state.lista)}")

st.markdown(f"**📋 Lista:** [{', '.join(map(str, st.session_state.lista))}]")
st.markdown("---")

# ========== CONTROLES ==========
st.markdown("### 🎮 Controles")
col_btn_play, col_btn_pausa, col_btn_paso = st.columns(3)

with col_btn_play:
    btn_play = st.button("▶️ Play", width="stretch")
with col_btn_pausa:
    btn_pausa = st.button("⏸️ Pausa", width="stretch")
with col_btn_paso:
    btn_paso = st.button("⏩ Paso", width="stretch")

# ========== CONTENEDOR PARA EL GRÁFICO ==========
grafico_placeholder = st.empty()

# ========== PROCESAR BOTONES ==========
if btn_play:
    if st.session_state.generador is None or st.session_state.terminado:
        st.session_state.generador = obtener_generador(algoritmo, st.session_state.lista, st.session_state.objetivo)
        st.session_state.terminado = False
        st.session_state.info_texto = "🔍 Buscando..."
        st.session_state.paso_actual = 0
        st.session_state.encontrado = False
        st.session_state.idx_actual = -1
        st.session_state.operacion = "normal"
    st.session_state.ejecutando = True
    st.rerun()

if btn_pausa:
    st.session_state.ejecutando = False
    st.rerun()

# ========== PASO A PASO (SOLO 2 CAMBIOS CLAVE) ==========
if btn_paso:
    st.session_state.ejecutando = False
    
    # ✅ CAMBIO 1: Crear generador si no existe o ya terminó
    if st.session_state.generador is None or st.session_state.terminado:
        st.session_state.generador = obtener_generador(algoritmo, st.session_state.lista, st.session_state.objetivo)
        st.session_state.terminado = False
        st.session_state.info_texto = "🔍 Buscando paso a paso..."
        st.session_state.paso_actual = 0
        st.session_state.encontrado = False
        st.session_state.idx_actual = -1
        st.session_state.operacion = "normal"
    
    try:
        estado = next(st.session_state.generador)
        actualizar_estado(estado)
        
        # ✅ CAMBIO 2: Dibujar gráfico INMEDIATAMENTE (sin st.rerun)
        if st.session_state.terminado:
            if st.session_state.encontrado:
                fig = dibujar_busqueda(st.session_state.lista, st.session_state.idx_actual, -1, -1, -1, "encontrado")
            else:
                fig = dibujar_busqueda(st.session_state.lista, -1, -1, -1, -1, "no_encontrado")
        else:
            fig = dibujar_busqueda(
                st.session_state.lista,
                st.session_state.idx_actual,
                st.session_state.izquierda,
                st.session_state.derecha,
                st.session_state.medio,
                st.session_state.operacion
            )
        grafico_placeholder.plotly_chart(fig, use_container_width=True, key=f"paso_{st.session_state.paso_actual}")
        # ✅ SIN st.rerun() - el gráfico ya se mostró
        
    except StopIteration:
        st.session_state.terminado = True
        st.session_state.ejecutando = False
        if not st.session_state.encontrado:
            st.session_state.info_texto = "❌ Elemento no encontrado"
        fig = dibujar_busqueda(st.session_state.lista, -1, -1, -1, -1, "no_encontrado")
        grafico_placeholder.plotly_chart(fig, use_container_width=True, key="paso_final")

# ========== ESTADO ==========
status_col1, status_col2 = st.columns(2)
with status_col1:
    estado_texto = "🟢 EJECUTANDO" if st.session_state.ejecutando else "⏸️ PAUSADO"
    st.markdown(f"**Estado:** {estado_texto}")
with status_col2:
    st.markdown(f"**Pasos:** {st.session_state.paso_actual}")

# ========== MOSTRAR RESULTADO ==========
if st.session_state.encontrado:
    st.success(st.session_state.info_texto)
elif st.session_state.terminado and not st.session_state.encontrado:
    st.error(st.session_state.info_texto)
else:
    st.info(st.session_state.info_texto)

# ========== DIBUJAR GRÁFICO SIEMPRE AL FINAL (como en ordenamiento) ==========
# Determinar qué mostrar
if st.session_state.terminado:
    if st.session_state.encontrado:
        op = "encontrado"
        idx = st.session_state.idx_actual
    else:
        op = "no_encontrado"
        idx = -1
    izq = -1
    der = -1
    med = -1
else:
    op = st.session_state.operacion
    idx = st.session_state.idx_actual
    izq = st.session_state.izquierda
    der = st.session_state.derecha
    med = st.session_state.medio

# Siempre dibujar el gráfico
fig = dibujar_busqueda(
    st.session_state.lista,
    idx,
    izq,
    der,
    med,
    op
)
st.plotly_chart(fig, use_container_width=True, key=f"grafico_{st.session_state.paso_actual}")

# ========== BUCLE DE ANIMACIÓN ==========
if st.session_state.ejecutando and not st.session_state.terminado:
    if st.session_state.generador:
        try:
            estado = next(st.session_state.generador)
            actualizar_estado(estado)
            time.sleep(0.3)
            st.rerun()
        except StopIteration:
            st.session_state.terminado = True
            st.session_state.ejecutando = False
            if not st.session_state.encontrado:
                st.session_state.info_texto = "❌ Elemento no encontrado"
            st.rerun()

# ========== INFORMACIÓN DEL ALGORITMO ==========
with st.expander("📖 Información del algoritmo"):
    info = {
        "Búsqueda Lineal": """
        **Búsqueda Lineal** - O(n)
        Recorre la lista elemento por elemento desde el principio.
        No requiere lista ordenada.
        """,
        "Búsqueda Binaria": """
        **Búsqueda Binaria** - O(log n)
        Divide la lista ordenada en mitades repetidamente.
        Requiere lista ORDENADA.
        """,
        "Búsqueda por Interpolación": """
        **Búsqueda por Interpolación** - O(log log n)
        Estima la posición del elemento basado en su valor.
        Requiere lista ORDENADA con distribución uniforme.
        """,
        "Búsqueda Exponencial": """
        **Búsqueda Exponencial** - O(log n)
        Encuentra un rango exponencialmente, luego aplica binaria.
        Requiere lista ORDENADA.
        """
    }
    st.markdown(info.get(algoritmo, ""))

# ========== LEYENDA ==========
with st.expander("🎨 Leyenda de colores"):
    st.markdown("""
    - 🔵 **Azul** = Elemento normal
    - 🟠 **Naranja** = Revisando actualmente
    - 🟢 **Verde** = Elemento encontrado
    - 🟣 **Púrpura** = Expandiendo rango (exponencial)
    - 🟡 **Verde oliva** = Rango encontrado
    - 🔴 **Línea roja** = Límites del rango (binaria)
    """)