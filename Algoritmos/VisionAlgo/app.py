import streamlit as st

# ========== CONFIGURACIÓN DE PÁGINA ==========
st.set_page_config(
    page_title="AlgoVision - Simulador de Algoritmos",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== BARRA LATERAL ==========
with st.sidebar:
    st.markdown("# 🧠 AlgoVision")
    st.markdown("*Simulador de Algoritmos*")
    st.markdown("---")
    
    st.markdown("### 📁 Navegación")
    
    if st.button("🏠 Inicio", use_container_width=True, key="nav_inicio"):
        st.switch_page("app.py")
    
    if st.button("📊 Ordenamiento", use_container_width=True, key="nav_ordenamiento"):
        st.switch_page("pages/ordenamiento.py")
    
    if st.button("🏆 Comparar Ordenamiento", use_container_width=True, key="nav_comp_ordenamiento"):
        st.switch_page("pages/comparacion_ordenamiento.py")
        
    if st.button("🏆 Comparar Búsqueda", use_container_width=True, key="nav_comp_busqueda"):
        st.switch_page("pages/comparacion_busqueda.py")
    
    if st.button("🔍 Búsqueda", use_container_width=True, key="nav_busqueda"):
        st.switch_page("pages/busqueda.py")
        
    if st.button("🌳 Árboles", use_container_width=True, key="nav_arboles"):
        st.switch_page("pages/arboles.py")
    
    st.markdown("---")
    st.markdown("### 🚧 Próximamente")
    st.markdown("- 🔗 Grafos")
    
    st.markdown("---")
    st.caption("SIS210 - UNA Puno")

# ========== ESTILOS PERSONALIZADOS ==========
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        background: linear-gradient(135deg, #1f77b4, #2ca02c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-top: 0;
        margin-bottom: 30px;
    }
    .card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #e9ecef;
        transition: transform 0.2s;
        height: 100%;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .card-icon {
        font-size: 3em;
        margin-bottom: 10px;
    }
    .card-title {
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 10px;
        color: #1f77b4;
    }
    .card-description {
        color: #555;
        font-size: 0.9em;
        margin-bottom: 15px;
        text-align: left;
    }
    .stats-container {
        background: linear-gradient(135deg, #1f77b4, #17becf);
        border-radius: 15px;
        padding: 20px;
        color: white;
        margin-top: 20px;
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        padding: 20px;
        color: #888;
        font-size: 0.8em;
    }
</style>
""", unsafe_allow_html=True)

# ========== TÍTULO ==========
st.markdown('<p class="main-title">🧠 AlgoVision</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Simulador de Algoritmos y Estructuras de Datos<br>SIS210 - Universidad Nacional del Altiplano</p>', unsafe_allow_html=True)

st.markdown("---")

# ========== TARJETAS DE ACCESO ==========
st.markdown("### 🚀 Explora los módulos")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📊</div>
        <div class="card-title">Ordenamiento</div>
        <div class="card-description">
            • Bubble, Selection, Insertion<br>
            • Quick, Merge, Shell<br>
            • Counting, Radix, Bucket<br>
            • ¡9 algoritmos en total!
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📊 Explorar Ordenamiento", key="btn_ordenamiento", use_container_width=True):
        st.switch_page("pages/ordenamiento.py")

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🔍</div>
        <div class="card-title">Búsqueda</div>
        <div class="card-description">
            • Búsqueda Lineal<br>
            • Búsqueda Binaria<br>
            • Búsqueda por Interpolación<br>
            • Búsqueda Exponencial
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔍 Explorar Búsqueda", key="btn_busqueda", use_container_width=True):
        st.switch_page("pages/busqueda.py")

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🌳</div>
        <div class="card-title">Árboles</div>
        <div class="card-description">
            • Árbol Binario de Búsqueda<br>
            • Árbol AVL (balanceado)<br>
            • Árbol Rojo-Negro<br>
            • Árboles B y B+
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🌳 Explorar Árboles", key="btn_arboles", use_container_width=True):
        st.switch_page("pages/arboles.py")

with col4:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🏆</div>
        <div class="card-title">Comparaciones</div>
        <div class="card-description">
            • Comparar Ordenamiento<br>
            • Comparar Búsqueda<br>
            • Tablas de tiempos<br>
            • Gráficos comparativos
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ✅ BOTONES CON KEYS ÚNICAS
    if st.button("🏆 Comparar Ordenamiento", key="btn_comp_ordenamiento", use_container_width=True):
        st.switch_page("pages/comparacion_ordenamiento.py")
    
    if st.button("🏆 Comparar Búsqueda", key="btn_comp_busqueda", use_container_width=True):
        st.switch_page("pages/comparacion_busqueda.py")

st.markdown("---")

# ========== GRAFOS (fila adicional) ==========
st.markdown("### 🔗 Grafos")
col_grafos1, col_grafos2, col_grafos3, col_grafos4 = st.columns(4)
with col_grafos1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🔗</div>
        <div class="card-title">Grafos</div>
        <div class="card-description">
            • BFS (Amplitud)<br>
            • DFS (Profundidad)<br>
            • Dijkstra (Camino mínimo)<br>
            • PRIM (Árbol de expansión)
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.info("🚧 Próximamente")

st.markdown("---")

# ========== ALGORITMO DESTACADO Y ESTADÍSTICAS ==========
col_izq, col_der = st.columns([2, 1])

with col_izq:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ffd700, #ffb347); padding: 20px; border-radius: 15px;">
        <h3 style="margin: 0 0 10px 0; color: #333;">⭐ Algoritmo destacado</h3>
        <h2 style="margin: 0; color: #333;">Quick Sort</h2>
        <p style="margin: 5px 0 0 0; color: #444;">El algoritmo más rápido en la práctica.<br>
        Divide y vencerás con pivote. O(n log n) promedio.</p>
    </div>
    """, unsafe_allow_html=True)

with col_der:
    st.markdown("""
    <div class="stats-container">
        <h3 style="margin: 0 0 15px 0; text-align: center;">📊 Estadísticas</h3>
        <table style="width: 100%; color: white;">
            <tr><td>📋 Algoritmos:</td><td style="text-align: right;"><b>13</b></td></tr>
            <tr><td>📊 Visualizaciones:</td><td style="text-align: right;"><b>200+</b></td></tr>
            <tr><td>🏆 Competencias:</td><td style="text-align: right;"><b>15</b></td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ========== FOOTER ==========
st.markdown("""
<div class="footer">
    © 2026 - AlgoVision | Curso SIS210 - Algoritmos y Estructuras de Datos<br>
    Universidad Nacional del Altiplano | Docente: Mg. Aldo Hernán Zanabria Gálvez
</div>
""", unsafe_allow_html=True)