"""
Guía de usuario para el simulador AlgoVision.
"""

import streamlit as st

def mostrar_guia():
    """Muestra la guía de usuario completa."""
    
    st.markdown("""
    # 🧠 Guía de Usuario - AlgoVision
    
    Bienvenido a **AlgoVision**, el simulador interactivo de algoritmos y estructuras de datos.
    Esta guía te ayudará a entender cómo usar cada módulo del simulador.
    
    ---
    
    ## 📋 Índice
    1. [Navegación general](#navegacion)
    2. [Módulo de Ordenamiento](#ordenamiento)
    3. [Módulo de Búsqueda](#busqueda)
    4. [Módulo de Árboles](#arboles)
    5. [Módulo de Grafos](#grafos)
    6. [Comparación de algoritmos](#comparacion)
    7. [Consejos para principiantes](#consejos)
    
    ---
    
    ## 🏠 Navegación general {#navegacion}
    
    ### Barra lateral
    En la barra lateral izquierda encontrarás:
    - **🧠 AlgoVision**: Título del simulador
    - **📁 Navegación**: Botones para acceder a cada módulo
    - **🚧 Próximamente**: Módulos en desarrollo
    
    ### Página de inicio
    Desde la página principal puedes:
    - Ver tarjetas con todos los módulos disponibles
    - Acceder a las comparaciones de algoritmos
    - Ver estadísticas generales del simulador
    
    ---
    
    ## 📊 Módulo de Ordenamiento {#ordenamiento}
    
    ### ¿Qué hace?
    Muestra cómo los algoritmos de ordenamiento organizan una lista de números.
    
    ### Algoritmos disponibles (9):
    - **Bubble Sort**: El más lento pero fácil de entender
    - **Selection Sort**: Selecciona el mínimo cada vez
    - **Insertion Sort**: Inserta elementos en su posición correcta
    - **Shell Sort**: Versión mejorada de Insertion Sort
    - **Quick Sort**: El más rápido en la práctica
    - **Merge Sort**: Divide y vencerás confiable
    - **Counting Sort**: Ordena por conteo (solo enteros)
    - **Radix Sort**: Ordena dígito por dígito
    - **Bucket Sort**: Distribuye en cubetas
    
    ### Cómo usarlo:
    1. **Selecciona un algoritmo** en el menú desplegable
    2. **Elige el tipo de datos**: Aleatoria, Ordenada, Inversa o Casi ordenada
    3. **Ajusta el tamaño** de la lista (5-30 elementos)
    4. **Controla la velocidad** de la animación
    5. **Usa los botones**:
       - ▶️ **Play**: Inicia la animación automática
       - ⏸️ **Pausa**: Detiene la animación
       - ⏩ **Paso**: Avanza un paso a la vez
       - 🔄 **Nueva lista**: Genera nuevos datos
       - 🔄 **Reiniciar**: Vuelve al inicio
    
    ### Leyenda de colores:
    - 🔵 Azul: Elemento normal
    - 🟠 Naranja: Elementos comparándose
    - 🔴 Rojo: Elementos intercambiándose
    - 🟢 Verde: Elementos ya ordenados
    - 🟣 Púrpura: Pivote (Quick Sort)
    
    ---
    
    ## 🔍 Módulo de Búsqueda {#busqueda}
    
    ### ¿Qué hace?
    Muestra cómo los algoritmos de búsqueda encuentran un elemento en una lista.
    
    ### Algoritmos disponibles (4):
    - **Búsqueda Lineal**: Recorre elemento por elemento
    - **Búsqueda Binaria**: Divide y vencerás (necesita lista ordenada)
    - **Búsqueda por Interpolación**: Estima la posición (necesita datos uniformes)
    - **Búsqueda Exponencial**: Encuentra rango y luego binaria
    
    ### Cómo usarlo:
    1. **Selecciona un algoritmo**
    2. **Elige el tipo de datos**: Ordenada (para binaria) o Aleatoria (para lineal)
    3. **Define el valor a buscar**
    4. **Genera una lista** con el botón "Generar lista de prueba"
    5. **Usa los controles**:
       - ▶️ **Play**: Animación automática
       - ⏸️ **Pausa**: Detiene
       - ⏩ **Paso**: Avanza uno a uno
    
    ### Leyenda de colores:
    - 🔵 Azul: Elemento normal
    - 🟠 Naranja: Elemento revisado actualmente
    - 🟢 Verde: Elemento encontrado
    - 🔴 Rojo: Límites del rango (búsqueda binaria)
    
    ---
    
    ## 🌳 Módulo de Árboles {#arboles}
    
    ### ¿Qué hace?
    Muestra la estructura y operaciones de diferentes tipos de árboles.
    
    ### Árboles disponibles (5):
    - **ABB**: Árbol Binario de Búsqueda
    - **AVL**: Auto-balanceado (rotaciones)
    - **Rojo-Negro**: Balanceado con colores
    - **Árbol B**: Múltiples claves por nodo
    - **Árbol B+**: Similar a B con hojas enlazadas
    
    ### Cómo usarlo:
    1. **Selecciona el tipo de árbol**
    2. **Operaciones disponibles**:
       - ➕ **Insertar**: Agrega un valor al árbol
       - 🔍 **Buscar**: Encuentra un valor
       - 🗑️ **Eliminar**: Elimina un valor
    3. **Recorridos** (para árboles binarios):
       - In-Order: Izquierda → Raíz → Derecha
       - Pre-Order: Raíz → Izquierda → Derecha
       - Post-Order: Izquierda → Derecha → Raíz
       - BFS: Nivel por nivel
    4. **Navegación**:
       - ⬅️ **Anterior**: Paso previo
       - ➡️ **Siguiente**: Siguiente paso
       - ▶️ **Auto**: Reproduce todos los pasos
    
    ### Leyenda de colores:
    - 🔵 Azul: Nodo normal
    - 🟠 Naranja: Nodo visitado
    - 🟢 Verde: Nodo encontrado
    - 🟣 Púrpura: Nodo insertado
    - 🔴 Rojo: Nodo eliminado
    - ⚫ Negro / 🔴 Rojo: Colores de Rojo-Negro
    
    ---
    
    ## 🔗 Módulo de Grafos {#grafos}
    
    ### ¿Qué hace?
    Muestra cómo los algoritmos recorren y exploran grafos.
    
    ### Algoritmos disponibles (4):
    - **BFS**: Búsqueda en amplitud (cola)
    - **DFS**: Búsqueda en profundidad (pila)
    - **Dijkstra**: Encuentra el camino más corto
    - **PRIM**: Construye el árbol de expansión mínima
    
    ### Cómo usarlo:
    1. **Paso 1**: Elige un grafo de ejemplo
    2. **Paso 2**: Selecciona el algoritmo
    3. **Paso 3**: Elige el nodo de inicio (y destino para Dijkstra)
    4. **Paso 4**: Presiona "Ejecutar algoritmo"
    5. **Paso 5**: Usa los botones de navegación para ver el recorrido
    
    ### Leyenda de colores:
    - 🔵 Azul: Nodo no visitado
    - 🟠 Naranja: Nodo actual
    - 🟢 Verde: Nodo visitado
    - ⚪ Gris: Arista normal
    - 🔴 Rojo: Arista del árbol / Camino encontrado
    
    ---
    
    ## 🏆 Comparación de algoritmos {#comparacion}
    
    ### ¿Qué hace?
    Compara el rendimiento de todos los algoritmos en un mismo módulo.
    
    ### Módulos de comparación:
    - **Ordenamiento**: 9 algoritmos (tiempo, comparaciones, intercambios)
    - **Búsqueda**: 4 algoritmos (tiempo, comparaciones, elementos revisados)
    - **Árboles**: 5 estructuras (altura, tamaño, balance)
    
    ### Cómo usarlo:
    1. **Selecciona los algoritmos** a comparar
    2. **Configura los datos** de prueba
    3. **Presiona "Iniciar comparación"**
    4. **Analiza los resultados**:
       - Tabla de estadísticas
       - Gráfico de barras
       - Gráfico de radar
       - Podio de ganadores
    
    ---
    
    ## 💡 Consejos para principiantes {#consejos}
    
    ### 1. Empieza con ordenamiento
    El módulo de ordenamiento es el más visual y fácil de entender. Prueba **Bubble Sort** primero.
    
    ### 2. Usa el paso a paso
    No uses Play inmediatamente. El modo **"Paso"** te permite ver cada operación con calma.
    
    ### 3. Experimenta con diferentes datos
    - **Ordenamiento**: Prueba listas aleatorias, ordenadas e inversas
    - **Búsqueda**: Busca valores existentes y no existentes
    - **Árboles**: Inserta en diferentes órdenes
    - **Grafos**: Prueba diferentes nodos de inicio
    
    ### 4. Observa los colores
    Los colores te indican lo que está pasando en cada momento. Presta atención a las leyendas.
    
    ### 5. Usa las comparaciones
    Los módulos de comparación te muestran qué algoritmo es mejor para cada situación.
    
    ### 6. No tengas miedo de equivocarte
    Prueba, observa, cambia parámetros y prueba de nuevo. Así se aprende.
    
    ---
    
    ## 📚 Recursos adicionales
    
    - **Sílabo del curso**: Consulta las semanas 4-16 para la teoría
    - **Bibliografía**: Cormen, Knuth, Sedgewick (ver referencias)
    - **Videos**: Busca visualizaciones en YouTube para complementar
    
    ---
    
    **🎓 ¡Feliz aprendizaje!**
    """)

def mostrar_guia_resumida():
    """Muestra una versión resumida de la guía (para la página de inicio)."""
    
    with st.expander("📖 Guía rápida de usuario", expanded=False):
        st.markdown("""
        ### 🚀 ¿Cómo usar AlgoVision?
        
        **Paso a paso:**
        1. **Explora los módulos**: Ordenamiento, Búsqueda, Árboles, Grafos
        2. **Elige un algoritmo** de la lista
        3. **Configura los datos** (tamaño, tipo, valores)
        4. **Usa los controles**: Play, Pausa, Paso, Auto
        5. **Observa** los colores y la animación
        6. **Compara** algoritmos en las pestañas de comparación
        
        ---
        
        ### 🎨 Significado de colores
        
        | Color | Significado |
        |-------|-------------|
        | 🔵 **Azul** | Elemento normal / no visitado |
        | 🟠 **Naranja** | Elemento en proceso / visitando |
        | 🟢 **Verde** | Elemento encontrado / ordenado |
        | 🔴 **Rojo** | Elemento intercambiado / eliminado |
        | 🟣 **Púrpura** | Nodo insertado / pivote |
        
        ---
        
        ### 💡 Consejos
        
        - Empieza con **Bubble Sort** en ordenamiento
        - Usa **Paso a paso** para entender cada operación
        - Prueba **diferentes tipos de datos**
        - Revisa las **leyendas de colores** en cada módulo
        
        📖 Para más detalles, despliega esta guía o consulta la guía completa.
        """)