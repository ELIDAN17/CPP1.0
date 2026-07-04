import streamlit as st
from utils.guia_usuario import mostrar_guia_resumida

# ========== CONFIGURACIÓN DE PÁGINA ==========
st.set_page_config(
    page_title="AlgoVision - Simulador de Algoritmos",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== BARRA LATERAL PERSONALIZADA ==========
with st.sidebar:
    st.markdown("# 🧠 AlgoVision")
    st.markdown("*Simulador de Algoritmos*")
    st.markdown("---")
    
    st.markdown("### 📁 Navegación")
    
    if st.button("🏠 Inicio", use_container_width=True, key="nav_inicio"):
        st.switch_page("app.py")
    
    if st.button("📖 Guía de usuario", use_container_width=True, key="nav_guia"):
        st.switch_page("pages/guia.py")
    
    st.markdown("---")
    
    st.markdown("### 🔬 Módulos")
    
    if st.button("📊 Ordenamiento", use_container_width=True, key="nav_ordenamiento"):
        st.switch_page("pages/ordenamiento.py")
    
    if st.button("🔍 Búsqueda", use_container_width=True, key="nav_busqueda"):
        st.switch_page("pages/busqueda.py")
    
    if st.button("🌳 Árboles", use_container_width=True, key="nav_arboles"):
        st.switch_page("pages/arboles.py")
    
    if st.button("🔗 Grafos", use_container_width=True, key="nav_grafos"):
        st.switch_page("pages/grafos.py")
    
    st.markdown("---")
    
    st.markdown("### 🏆 Comparaciones")
    
    if st.button("📊 Ordenamiento", use_container_width=True, key="nav_comp_ordenamiento"):
        st.switch_page("pages/comparacion_ordenamiento.py")
    
    if st.button("🔍 Búsqueda", use_container_width=True, key="nav_comp_busqueda"):
        st.switch_page("pages/comparacion_busqueda.py")
    
    if st.button("🌳 Árboles", use_container_width=True, key="nav_comp_arboles"):
        st.switch_page("pages/comparacion_arboles.py")
    
    if st.button("🔗 Grafos", use_container_width=True, key="nav_comp_grafos"):
        st.switch_page("pages/comparacion_grafos.py")
    
    st.markdown("---")
    st.caption("J_Ely © 2026 - AlgoVision")

# ========== ESTILOS PERSONALIZADOS ==========
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 3.5em;
        font-weight: bold;
        background: linear-gradient(135deg, #1f77b4, #2ca02c, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        animation: fadeIn 1s ease-in;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-top: 0;
        margin-bottom: 30px;
        font-size: 1.2em;
    }
    .card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #e9ecef;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
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
        border-top: 1px solid #eee;
    }
    .welcome-box {
        background: linear-gradient(135deg, #e8f5e9, #b2dfdb);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 5px solid #2ca02c;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .btn-group {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ========== TÍTULO ==========
st.markdown('<p class="main-title">🧠 AlgoVision</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Simulador interactivo de Algoritmos y Estructuras de Datos<br>📚 SIS210 - Universidad Nacional del Altiplano</p>', unsafe_allow_html=True)

st.markdown("---")

# ========== BIENVENIDA ==========
st.markdown("""
<div class="welcome-box">
    <h3 style="margin: 0; color: #1a6b1a;">🎓 ¡Bienvenido a AlgoVision!</h3>
    <p style="margin: 5px 0 0 0; color: #333;">
        Aprende algoritmos y estructuras de datos de forma visual e interactiva. 
        Explora los módulos, ejecuta animaciones y compara el rendimiento de cada algoritmo.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ========== GUÍA DE USUARIO ==========
mostrar_guia_resumida()

st.markdown("---")

# ========== TARJETAS DE ACCESO - MÓDULOS PRINCIPALES ==========
st.markdown("### 🔬 Módulos principales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📊</div>
        <div class="card-title">Ordenamiento</div>
        <div class="card-description">
            • 9 algoritmos<br>
            • Animaciones paso a paso<br>
            • Comparación de rendimiento
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
            • 4 algoritmos<br>
            • Búsqueda Lineal y Binaria<br>
            • Interpolación y Exponencial
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
            • ABB, AVL, Rojo-Negro<br>
            • Árboles B y B+<br>
            • Recorridos y balanceo
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🌳 Explorar Árboles", key="btn_arboles", use_container_width=True):
        st.switch_page("pages/arboles.py")

with col4:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🔗</div>
        <div class="card-title">Grafos</div>
        <div class="card-description">
            • BFS y DFS<br>
            • Dijkstra (camino mínimo)<br>
            • PRIM (árbol de expansión)
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔗 Explorar Grafos", key="btn_grafos", use_container_width=True):
        st.switch_page("pages/grafos.py")

st.markdown("---")

# ========== TARJETAS DE COMPARACIONES ==========
st.markdown("### 🏆 Comparaciones")

col_comp1, col_comp2, col_comp3, col_comp4 = st.columns(4)

with col_comp1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📊</div>
        <div class="card-title">Ordenamiento</div>
        <div class="card-description">
            • 9 algoritmos<br>
            • Tiempo, comparaciones<br>
            • Gráficos y radar
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🏆 Comparar Ordenamiento", key="btn_comp_ordenamiento", use_container_width=True):
        st.switch_page("pages/comparacion_ordenamiento.py")

with col_comp2:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🔍</div>
        <div class="card-title">Búsqueda</div>
        <div class="card-description">
            • 4 algoritmos<br>
            • Tiempo, comparaciones<br>
            • Elementos revisados
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🏆 Comparar Búsqueda", key="btn_comp_busqueda", use_container_width=True):
        st.switch_page("pages/comparacion_busqueda.py")

with col_comp3:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🌳</div>
        <div class="card-title">Árboles</div>
        <div class="card-description">
            • 5 estructuras<br>
            • Altura, tamaño<br>
            • Balance y eficiencia
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🏆 Comparar Árboles", key="btn_comp_arboles", use_container_width=True):
        st.switch_page("pages/comparacion_arboles.py")

with col_comp4:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🔗</div>
        <div class="card-title">Grafos</div>
        <div class="card-description">
            • 4 algoritmos<br>
            • Tiempo, pasos<br>
            • Nodos visitados
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🏆 Comparar Grafos", key="btn_comp_grafos", use_container_width=True):
        st.switch_page("pages/comparacion_grafos.py")

st.markdown("---")

# ========== ESTADÍSTICAS ==========
st.markdown("### 📊 Estadísticas del simulador")

col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)

with col_stats1:
    st.metric("📋 Algoritmos", "17", help="Total de algoritmos implementados")

with col_stats2:
    st.metric("🌳 Estructuras", "5", help="Tipos de estructuras de datos")

with col_stats3:
    st.metric("🏆 Comparaciones", "4", help="Módulos de comparación")

with col_stats4:
    st.metric("📊 Animaciones", "200+", help="Visualizaciones generadas")

st.markdown("---")

# ========== FOOTER ==========
st.markdown("""
<div class="footer">
    J_Ely© 2026 - AlgoVision | Algoritmos y Estructuras de Datos<br>
</div>
""", unsafe_allow_html=True)