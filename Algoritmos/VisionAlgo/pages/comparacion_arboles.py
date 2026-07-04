"""
Pestaña de Comparación de Árboles
Ejecuta todos los árboles con los mismos datos y compara estadísticas.
"""

import streamlit as st
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
from algoritmos.arboles import ArbolABB, ArbolAVL, ArbolRojoNegro, ArbolB, ArbolBMas

st.set_page_config(page_title="AlgoVision - Comparación Árboles", page_icon="🏆", layout="wide")

st.title("🏆 Comparación de Árboles")
st.markdown("### ¿Cuál árbol es mejor según el caso de uso?")
st.markdown("---")

# ========== SIDEBAR ==========
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Selección de valores a insertar
    st.markdown("### 📋 Datos de prueba")
    
    tipo_datos = st.selectbox(
        "Tipo de datos",
        ["Aleatorio", "Ordenado", "Inverso", "Personalizado"],
        index=0,
        help="El tipo de datos afecta el balanceo de los árboles"
    )
    
    num_elementos = st.slider(
        "Cantidad de elementos",
        min_value=5,
        max_value=50,
        value=15,
        step=5,
        help="Para más de 30 elementos, los árboles se vuelven más interesantes"
    )
    
    # Valores personalizados (solo si se selecciona Personalizado)
    valores_personalizados = ""
    if tipo_datos == "Personalizado":
        st.markdown("**Ingresa los valores (separados por comas):**")
        valores_personalizados = st.text_area(
            "Valores",
            value="50, 30, 70, 20, 40, 60, 80, 10, 90, 25, 35, 55, 65, 75, 85",
            height=80,
            help="Ejemplo: 50, 30, 70, 20, 40, 60, 80"
        )
    
    st.markdown("---")
    st.markdown("### 🌳 Árboles a comparar")
    
    arboles_seleccionados = st.multiselect(
        "Selecciona los árboles",
        ["ABB", "AVL", "Rojo-Negro", "Árbol B", "Árbol B+"],
        default=["ABB", "AVL", "Rojo-Negro", "Árbol B", "Árbol B+"]
    )
    
    st.markdown("---")
    ejecutar = st.button("🏁 ¡INICIAR COMPARACIÓN!", use_container_width=True, type="primary")

# ========== FUNCIONES ==========
def generar_datos(tipo, n, valores_personalizados=None):
    """
    Genera lista de valores según el tipo seleccionado.
    
    Args:
        tipo: "Aleatorio", "Ordenado", "Inverso", "Personalizado"
        n: Número de elementos (para tipos automáticos)
        valores_personalizados: String con valores separados por comas
    """
    if tipo == "Personalizado":
        if valores_personalizados:
            try:
                # Limpiar y convertir a enteros
                valores = [int(v.strip()) for v in valores_personalizados.split(",") if v.strip()]
                if not valores:
                    # Si no hay valores, usar valores por defecto
                    valores = [50, 30, 70, 20, 40, 60, 80, 10, 90, 25, 35, 55, 65, 75, 85]
                    st.warning("⚠️ No se ingresaron valores. Usando valores por defecto.")
                return valores
            except ValueError:
                st.error("⚠️ Error en los valores personalizados. Usando valores por defecto.")
                return [50, 30, 70, 20, 40, 60, 80, 10, 90, 25, 35, 55, 65, 75, 85]
        else:
            # Si no hay valores personalizados, usar valores por defecto
            return [50, 30, 70, 20, 40, 60, 80, 10, 90, 25, 35, 55, 65, 75, 85]
    
    elif tipo == "Aleatorio":
        # Generar valores únicos aleatorios
        return random.sample(range(10, 200), min(n, 190))
    elif tipo == "Ordenado":
        return list(range(10, 10 + n))
    elif tipo == "Inverso":
        return list(range(10 + n - 1, 9, -1))
    else:
        return random.sample(range(10, 200), min(n, 190))

def obtener_estadisticas(arbol, nombre):
    """Obtiene estadísticas de un árbol."""
    stats = {
        "nombre": nombre,
        "altura": arbol.altura() if hasattr(arbol, 'altura') else 0,
        "tamaño": arbol.tamaño() if hasattr(arbol, 'tamaño') else 0,
    }
    
    # Estadísticas adicionales según tipo de árbol
    if hasattr(arbol, 'es_balanceado'):
        stats["balanceado"] = arbol.es_balanceado()
    else:
        stats["balanceado"] = True
    
    if hasattr(arbol, 'raiz') and arbol.raiz:
        if hasattr(arbol.raiz, 'claves'):
            stats["claves_por_nodo"] = len(arbol.raiz.claves)
            stats["tipo"] = "B-Tree"
        else:
            stats["claves_por_nodo"] = 1
            stats["tipo"] = "Binario"
    else:
        stats["claves_por_nodo"] = 0
        stats["tipo"] = "Vacío"
    
    return stats

def ejecutar_arbol(nombre, arbol_class, valores, t=3):
    """Ejecuta la inserción de valores en un árbol y mide tiempo."""
    inicio = time.time()
    
    if nombre in ["Árbol B", "Árbol B+"]:
        arbol = arbol_class(t=t)
    else:
        arbol = arbol_class()
    
    for v in valores:
        try:
            # Consumir el generador para ejecutar la inserción
            for _ in arbol.insertar(v):
                pass
        except Exception as e:
            st.warning(f"⚠️ Error insertando {v} en {nombre}: {e}")
            continue
    
    fin = time.time()
    tiempo_ms = (fin - inicio) * 1000
    
    stats = obtener_estadisticas(arbol, nombre)
    stats["tiempo_ms"] = tiempo_ms
    
    return stats, arbol

# ========== DICCIONARIO DE ÁRBOLES ==========
ARBOLES = {
    "ABB": ArbolABB,
    "AVL": ArbolAVL,
    "Rojo-Negro": ArbolRojoNegro,
    "Árbol B": ArbolB,
    "Árbol B+": ArbolBMas,
}

# ========== INICIALIZAR RESULTADOS ==========
if "resultados_arboles" not in st.session_state:
    st.session_state.resultados_arboles = None
if "arboles_creados" not in st.session_state:
    st.session_state.arboles_creados = None
if "valores_utilizados" not in st.session_state:
    st.session_state.valores_utilizados = None

# ========== EJECUTAR COMPARACIÓN ==========
if ejecutar:
    if not arboles_seleccionados:
        st.error("⚠️ Selecciona al menos un árbol para comparar")
    else:
        with st.spinner("🔄 Construyendo árboles... Esto puede tomar unos segundos"):
            # Generar datos
            valores = generar_datos(tipo_datos, num_elementos, valores_personalizados)
            st.session_state.valores_utilizados = valores
            
            resultados = []
            arboles_creados = {}
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, nombre in enumerate(arboles_seleccionados):
                status_text.text(f"Construyendo {nombre}...")
                
                if nombre in ["Árbol B", "Árbol B+"]:
                    stats, arbol = ejecutar_arbol(nombre, ARBOLES[nombre], valores, t=3)
                else:
                    stats, arbol = ejecutar_arbol(nombre, ARBOLES[nombre], valores)
                
                resultados.append(stats)
                arboles_creados[nombre] = arbol
                
                progress_bar.progress((i + 1) / len(arboles_seleccionados))
            
            progress_bar.empty()
            status_text.empty()
            
            # Ordenar por altura (menor altura = mejor)
            resultados.sort(key=lambda x: x["altura"])
            
            st.session_state.resultados_arboles = resultados
            st.session_state.arboles_creados = arboles_creados

# ========== MOSTRAR RESULTADOS ==========
if st.session_state.resultados_arboles:
    resultados = st.session_state.resultados_arboles
    valores = st.session_state.valores_utilizados
    
    # ========== MOSTRAR DATOS UTILIZADOS ==========
    st.subheader("📋 Datos de prueba")
    
    # Mostrar los valores utilizados
    if len(valores) <= 30:
        st.markdown(f"**Valores insertados:** `{valores}`")
    else:
        # Mostrar solo los primeros 30 valores
        preview = valores[:30]
        st.markdown(f"**Valores insertados:** `{preview}...` (total: {len(valores)})")
    
    st.markdown(f"**Tipo:** {tipo_datos} | **Cantidad:** {len(valores)} elementos")
    st.markdown("---")
    
    # ========== TARJETA DEL GANADOR ==========
    ganador = resultados[0]  # Ordenado por altura (menor altura = mejor)
    
    col_ganador1, col_ganador2, col_ganador3 = st.columns([1, 2, 1])
    with col_ganador2:
        st.markdown(f"""
        <div style='text-align: center; background: linear-gradient(135deg, #ffd700, #ffb347); 
                    padding: 20px; border-radius: 20px; margin: 10px 0;'>
            <h1 style='margin: 0; font-size: 3em;'>🏆</h1>
            <h2 style='margin: 0; color: #fff;'>MEJOR ÁRBOL</h2>
            <h1 style='margin: 10px 0 0 0; color: #fff; font-size: 2.5em;'>{ganador['nombre']}</h1>
            <p style='margin: 5px 0 0 0; color: #fff; font-size: 1.2em;'>⚡ Altura: {ganador['altura']}</p>
            <p style='margin: 0; color: #fff;'>Tamaño: {ganador['tamaño']} nodos</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== TABLA DE RESULTADOS ==========
    st.subheader("📊 Tabla comparativa de resultados")
    
    df = pd.DataFrame(resultados)
    df = df.rename(columns={
        "nombre": "Árbol",
        "altura": "Altura",
        "tamaño": "Tamaño (nodos)",
        "tiempo_ms": "Tiempo (ms)",
        "balanceado": "¿Balanceado?",
        "claves_por_nodo": "Claves/nodo",
        "tipo": "Tipo"
    })
    
    df["Tiempo (ms)"] = df["Tiempo (ms)"].map(lambda x: f"{x:.2f}")
    df["¿Balanceado?"] = df["¿Balanceado?"].map(lambda x: "✅ Sí" if x else "❌ No")
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # ========== GRÁFICO DE BARRAS (Altura) ==========
    st.subheader("📈 Comparación de altura")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    nombres = [r["nombre"] for r in resultados]
    alturas = [r["altura"] for r in resultados]
    
    colores_barras = []
    for i, altura in enumerate(alturas):
        if i == 0:
            colores_barras.append("#ffd700")  # Dorado
        elif i == 1:
            colores_barras.append("#c0c0c0")  # Plata
        elif i == 2:
            colores_barras.append("#cd7f32")  # Bronce
        else:
            colores_barras.append("#1f77b4")  # Azul normal
    
    bars = ax.barh(nombres, alturas, color=colores_barras, edgecolor="black")
    ax.set_xlabel("Altura", fontsize=12)
    ax.set_title("Comparación de alturas (menor = mejor balanceado)", fontsize=14, fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    
    for bar, altura in zip(bars, alturas):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                f"{altura}", va="center", fontsize=10)
    
    st.pyplot(fig)
    plt.close(fig)
    
    # ========== GRÁFICO DE TAMAÑO ==========
    st.subheader("📊 Comparación de tamaño")
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    
    tamanos = [r["tamaño"] for r in resultados]
    
    bars2 = ax2.barh(nombres, tamanos, color="#17becf", edgecolor="black")
    ax2.set_xlabel("Número de nodos", fontsize=12)
    ax2.set_title("Comparación de tamaño (menos nodos = más eficiente)", fontsize=14, fontweight="bold")
    ax2.grid(axis="x", linestyle="--", alpha=0.3)
    
    for bar, tam in zip(bars2, tamanos):
        ax2.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                f"{tam}", va="center", fontsize=10)
    
    st.pyplot(fig2)
    plt.close(fig2)
    
    # ========== GRÁFICO DE RADAR ==========
    st.subheader("📊 Perfil de eficiencia")
    
    # Normalizar valores para el radar
    max_altura = max(r["altura"] for r in resultados) if resultados else 1
    max_tamano = max(r["tamaño"] for r in resultados) if resultados else 1
    max_tiempo = max(r["tiempo_ms"] for r in resultados) if resultados else 1
    
    fig3, ax3 = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    
    categorias = ['Altura\n(menor mejor)', 'Tamaño\n(menor mejor)', 'Tiempo\n(menor mejor)']
    num_vars = len(categorias)
    
    angulos = [n / float(num_vars) * 2 * 3.14159 for n in range(num_vars)]
    angulos += angulos[:1]
    
    for resultado in resultados:
        valores_radar = [
            1 - (resultado["altura"] / max_altura) if max_altura > 0 else 0,
            1 - (resultado["tamaño"] / max_tamano) if max_tamano > 0 else 0,
            1 - (resultado["tiempo_ms"] / max_tiempo) if max_tiempo > 0 else 0
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
        st.markdown("**🏆 Mejor altura**")
        st.markdown(f"🥇 **{resultados[0]['nombre']}** - Altura: {resultados[0]['altura']}")
        if len(resultados) > 1:
            st.markdown(f"🥈 **{resultados[1]['nombre']}** - Altura: {resultados[1]['altura']}")
        if len(resultados) > 2:
            st.markdown(f"🥉 **{resultados[2]['nombre']}** - Altura: {resultados[2]['altura']}")
    
    with col_analisis2:
        st.markdown("**📊 Estadísticas de la prueba**")
        st.markdown(f"📋 **Datos:** {len(valores)} elementos")
        st.markdown(f"📌 **Tipo:** {tipo_datos}")
        st.markdown(f"🌳 **Árboles evaluados:** {len(arboles_seleccionados)}")
    
    # ========== EXPLICACIÓN ==========
    with st.expander("📖 Interpretación de resultados"):
        st.markdown("""
        ### ¿Cómo interpretar los resultados?
        
        | Métrica | Significado |
        |---------|-------------|
        | **Altura** | Número de niveles. Menor altura = mejor balanceo |
        | **Tamaño** | Número de nodos. Menos nodos = más eficiente |
        | **Tiempo** | Tiempo de inserción. Menor tiempo = más rápido |
        | **Balanceado** | Si el árbol mantiene equilibrio automáticamente |
        | **Claves/nodo** | Promedio de claves por nodo (B-Trees tienen más) |
        
        ### ¿Cuándo usar cada árbol?
        
        - **ABB**: Para estructuras pequeñas o cuando los datos llegan aleatoriamente
        - **AVL**: Cuando las búsquedas son más frecuentes que las inserciones
        - **Rojo-Negro**: Cuando las inserciones son más frecuentes que las búsquedas
        - **Árbol B**: Para bases de datos y discos (menos accesos)
        - **Árbol B+**: Para índices de bases de datos (recorridos secuenciales)
        """)
    
    # ========== BOTÓN LIMPIAR ==========
    if st.button("🗑️ Limpiar resultados", use_container_width=True):
        st.session_state.resultados_arboles = None
        st.session_state.arboles_creados = None
        st.session_state.valores_utilizados = None
        st.rerun()

# ========== MENSAJE INICIAL ==========
else:
    st.info("👈 **Configura la competencia y presiona 'INICIAR COMPARACIÓN'**")
    
    col_ejemplo1, col_ejemplo2, col_ejemplo3 = st.columns(3)
    with col_ejemplo1:
        st.markdown("""
        ### 💡 ¿Qué hace esta herramienta?
        Construye **todos los árboles seleccionados** con los **mismos datos** y mide:
        - 📏 Altura
        - 📊 Tamaño
        - ⏱️ Tiempo de inserción
        - ⚖️ Balance
        """)
    with col_ejemplo2:
        st.markdown("""
        ### 🏆 ¿Cómo se determina el ganador?
        El ganador es el árbol con **menor altura** (mejor balanceado).
        
        En caso de empate, se considera el que tiene **menos nodos**.
        """)
    with col_ejemplo3:
        st.markdown("""
        ### 📊 ¿Qué tipo de datos probar?
        - **Aleatorio:** Comportamiento promedio
        - **Ordenado:** Mejor caso para algunos, peor para ABB
        - **Inverso:** Muestra degeneración en ABB
        - **Personalizado:** Pruebas específicas
        """)

# ========== FOOTER ==========
st.markdown("---")
st.caption("🏆 Comparación de árboles | SIS210 - Algoritmos y Estructuras de Datos")