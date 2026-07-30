import streamlit as st
import time
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
from visualizacion import dibujar_barras
from utils import (
    lista_aleatoria, lista_ordenada, lista_inversa, lista_casi_ordenada
)

st.set_page_config(page_title="AlgoVision - Ordenamiento", page_icon="📊", layout="wide")

# ========== JAVASCRIPT PARA MANTENER SCROLL ==========
st.markdown("""
<script>
// Guardar posición de scroll antes de recargar
window.addEventListener('beforeunload', function() {
    localStorage.setItem('scroll_pos', window.scrollY);
});

// Restaurar posición después de recargar
window.addEventListener('load', function() {
    const pos = localStorage.getItem('scroll_pos');
    if (pos !== null) {
        window.scrollTo(0, parseInt(pos));
        localStorage.removeItem('scroll_pos');
    }
});
</script>
""", unsafe_allow_html=True)

# ========== ANCLA PARA LA ANIMACIÓN ==========
st.markdown('<div id="animacion" style="scroll-margin-top: 80px;"></div>', unsafe_allow_html=True)

# ========== INICIALIZAR TODAS LAS VARIABLES ==========
if "lista" not in st.session_state:
    st.session_state.lista = None
if "generador" not in st.session_state:
    st.session_state.generador = None
if "terminado" not in st.session_state:
    st.session_state.terminado = False
if "ejecutando" not in st.session_state:
    st.session_state.ejecutando = False
if "info_texto" not in st.session_state:
    st.session_state.info_texto = "📋 Listo para comenzar"
if "ultima_operacion" not in st.session_state:
    st.session_state.ultima_operacion = "normal"
if "ultimo_idx1" not in st.session_state:
    st.session_state.ultimo_idx1 = -1
if "ultimo_idx2" not in st.session_state:
    st.session_state.ultimo_idx2 = -1
if "ultimo_idx3" not in st.session_state:
    st.session_state.ultimo_idx3 = -1
if "pasos_acumulados" not in st.session_state:
    st.session_state.pasos_acumulados = 0
if "pasos_por_frame" not in st.session_state:
    st.session_state.pasos_por_frame = 3  # Múltiples pasos por actualización

st.title("📊 Simulador de Algoritmos de Ordenamiento")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🎮 Controles")
    
    algoritmo = st.selectbox(
        "Algoritmo",
        ["Bubble Sort", "Selection Sort", "Insertion Sort", "Shell Sort", 
         "Quick Sort", "Merge Sort", "Counting Sort", "Radix Sort", "Bucket Sort"],
        index=0
    )
    
    tipo_datos = st.selectbox(
        "Tipo de datos",
        ["Aleatoria", "Ordenada", "Inversa", "Casi ordenada"],
        index=0
    )
    
    num_elementos = st.slider("Cantidad de elementos", 5, 20, 10, 5)
    
    velocidad = st.slider("Velocidad (segundos)", 0.05, 0.5, 0.15, 0.05)
    
    # Opción para ajustar pasos por frame (más fluidez)
    pasos_por_frame = st.slider("Pasos por actualización", 1, 5, 3, 1,
                                help="Más pasos = animación más rápida, menos parpadeo")
    st.session_state.pasos_por_frame = pasos_por_frame
    
    if st.button("🔄 Generar nueva lista", use_container_width=True):
        if tipo_datos == "Aleatoria":
            nueva_lista = lista_aleatoria(num_elementos)
        elif tipo_datos == "Ordenada":
            nueva_lista = lista_ordenada(num_elementos)
        elif tipo_datos == "Inversa":
            nueva_lista = lista_inversa(num_elementos)
        else:
            nueva_lista = lista_casi_ordenada(num_elementos)
        
        st.session_state.lista = nueva_lista
        st.session_state.generador = None
        st.session_state.terminado = False
        st.session_state.ejecutando = False
        st.session_state.info_texto = "📋 Nueva lista generada"
        st.session_state.ultima_operacion = "normal"
        st.session_state.ultimo_idx1 = -1
        st.session_state.ultimo_idx2 = -1
        st.session_state.ultimo_idx3 = -1
        st.rerun()

# Inicializar lista por defecto
if st.session_state.lista is None:
    st.session_state.lista = lista_aleatoria(num_elementos)

# Controles de animación
st.markdown("### 🎮 Controles")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("▶️ Play", use_container_width=True):
        st.session_state.ejecutando = True
        st.rerun()
with col2:
    if st.button("⏸️ Pausa", use_container_width=True):
        st.session_state.ejecutando = False
        st.rerun()
with col3:
    if st.button("⏩ Paso", use_container_width=True):
        st.session_state.ejecutando = False
        if st.session_state.generador is not None and not st.session_state.terminado:
            try:
                estado = next(st.session_state.generador)
                if len(estado) == 4:
                    lista, idx1, idx2, op = estado
                    st.session_state.lista = lista
                    st.session_state.ultima_operacion = op
                    st.session_state.ultimo_idx1 = idx1
                    st.session_state.ultimo_idx2 = idx2
                    st.session_state.info_texto = f"🔍 {op.upper()}: índices {idx1} y {idx2}"
                elif len(estado) == 5:
                    lista, idx1, idx2, idx3, op = estado
                    st.session_state.lista = lista
                    st.session_state.ultima_operacion = op
                    st.session_state.ultimo_idx1 = idx1
                    st.session_state.ultimo_idx2 = idx2
                    st.session_state.ultimo_idx3 = idx3
                    st.session_state.info_texto = f"🔍 {op.upper()}: índices {idx1}, {idx2}"
                else:
                    lista, idx1, idx2, op, extra = estado
                    st.session_state.lista = lista
                    st.session_state.ultima_operacion = op
                    st.session_state.ultimo_idx1 = idx1
                    st.session_state.info_texto = f"🔍 {op.upper()}: índice {idx1}"
            except StopIteration:
                st.session_state.terminado = True
                st.session_state.ejecutando = False
                st.session_state.ultima_operacion = "finished"
                st.session_state.info_texto = "🎉 ¡Ordenamiento completado!"
        st.rerun()
with col4:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.generador = None
        st.session_state.terminado = False
        st.session_state.ejecutando = False
        st.session_state.ultima_operacion = "normal"
        st.session_state.ultimo_idx1 = -1
        st.session_state.ultimo_idx2 = -1
        st.session_state.ultimo_idx3 = -1
        st.session_state.info_texto = "📋 Reiniciado"
        st.rerun()

# Mostrar estado
status_col1, status_col2 = st.columns(2)
with status_col1:
    estado_texto = "🟢 EJECUTANDO" if st.session_state.ejecutando else "⏸️ PAUSADO"
    st.markdown(f"**Estado:** {estado_texto}")
with status_col2:
    st.markdown(f"**Algoritmo:** {algoritmo}")


# Crear generador
if st.session_state.generador is None and not st.session_state.terminado:
    if algoritmo == "Bubble Sort":
        st.session_state.generador = bubble_sort_generator(st.session_state.lista)
    elif algoritmo == "Selection Sort":
        st.session_state.generador = selection_sort_generator(st.session_state.lista)
    elif algoritmo == "Insertion Sort":
        st.session_state.generador = insertion_sort_generator(st.session_state.lista)
    elif algoritmo == "Shell Sort":
        st.session_state.generador = shell_sort_generator(st.session_state.lista)
    elif algoritmo == "Quick Sort":
        st.session_state.generador = quick_sort_generator(st.session_state.lista)
    elif algoritmo == "Merge Sort":
        st.session_state.generador = merge_sort_generator(st.session_state.lista)
    elif algoritmo == "Counting Sort":
        st.session_state.generador = counting_sort_generator(st.session_state.lista)
    elif algoritmo == "Radix Sort":
        st.session_state.generador = radix_sort_generator(st.session_state.lista)
    elif algoritmo == "Bucket Sort":
        st.session_state.generador = bucket_sort_generator(st.session_state.lista, num_buckets=5)

# Mostrar gráfico con Plotly
fig = dibujar_barras(
    st.session_state.lista,
    st.session_state.ultimo_idx1,
    st.session_state.ultimo_idx2,
    st.session_state.ultimo_idx3,
    st.session_state.ultima_operacion if not st.session_state.terminado else "finished",
    ancho=900,
    alto=500
)
st.plotly_chart(fig, use_container_width=True, key="chart_principal")

# ========== BUCLE DE ANIMACIÓN OPTIMIZADO ==========
# Múltiples pasos por actualización para reducir parpadeo
if st.session_state.ejecutando and not st.session_state.terminado:
    if st.session_state.generador is not None:
        try:
            # Ejecutar varios pasos antes de actualizar la UI
            for _ in range(st.session_state.pasos_por_frame):
                estado = next(st.session_state.generador)
                if len(estado) == 4:
                    lista, idx1, idx2, op = estado
                    st.session_state.lista = lista
                    st.session_state.ultima_operacion = op
                    st.session_state.ultimo_idx1 = idx1
                    st.session_state.ultimo_idx2 = idx2
                    if op == "swapping":
                        st.session_state.info_texto = f"🔄 INTERCAMBIO: {lista[idx1]} ↔ {lista[idx2]}"
                    elif op == "comparing":
                        st.session_state.info_texto = f"🔍 COMPARACIÓN: {lista[idx1]} vs {lista[idx2]}"
                    else:
                        st.session_state.info_texto = f"⚙️ {op.upper()}"
                elif len(estado) == 5:
                    lista, idx1, idx2, idx3, op = estado
                    st.session_state.lista = lista
                    st.session_state.ultima_operacion = op
                    st.session_state.ultimo_idx1 = idx1
                    st.session_state.ultimo_idx2 = idx2
                    st.session_state.ultimo_idx3 = idx3
                    st.session_state.info_texto = f"⚙️ {op.upper()}"
                else:
                    lista, idx1, idx2, op, extra = estado
                    st.session_state.lista = lista
                    st.session_state.ultima_operacion = op
                    st.session_state.ultimo_idx1 = idx1
                    st.session_state.info_texto = f"⚙️ {op.upper()}"
            
            # Pausa proporcional a la velocidad
            time.sleep(velocidad * st.session_state.pasos_por_frame / 2)
            st.rerun()
        except StopIteration:
            st.session_state.terminado = True
            st.session_state.ejecutando = False
            st.session_state.ultima_operacion = "finished"
            st.session_state.info_texto = "🎉 ¡ORDENAMIENTO COMPLETADO!"
            st.rerun()

# Información del algoritmo
with st.expander("📖 Información del algoritmo"):
    info = {
        "Bubble Sort": "Compara elementos adyacentes y los intercambia si están desordenados. O(n²).",
        "Selection Sort": "Encuentra el mínimo y lo coloca al inicio. O(n²).",
        "Insertion Sort": "Inserta cada elemento en su posición correcta. O(n²).",
        "Shell Sort": "Usa gaps para mover elementos rápido. O(n log² n).",
        "Quick Sort": "Divide y vencerás con pivote. O(n log n) promedio.",
        "Merge Sort": "Divide, ordena y mezcla. O(n log n).",
        "Counting Sort": "Cuenta frecuencias. O(n + k).",
        "Radix Sort": "Ordena dígito por dígito. O(d × n).",
        "Bucket Sort": "Distribuye en cubetas. O(n + k)."
    }
    st.markdown(f"**{algoritmo}:** {info.get(algoritmo, 'Algoritmo de ordenamiento')}")
    st.markdown("---")
    st.markdown("💡 **Leyenda de colores:**")
    st.markdown("🔵 Azul = Normal | 🟠 Naranja = Comparando | 🔴 Rojo = Intercambiando | 🟢 Verde = Ordenado")