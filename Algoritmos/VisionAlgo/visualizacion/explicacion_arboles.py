"""
Explicaciones de métodos de árboles para mostrar al usuario.
"""

import streamlit as st

def mostrar_explicacion_metodo(metodo, tipo_arbol="ABB"):
    """
    Muestra la explicación del método según el tipo de árbol.
    """
    
    if metodo == "insertar":
        if tipo_arbol == "ABB":
            st.markdown("""
            ### 🔍 ¿Cómo funciona la inserción en ABB?
            
            **1. Búsqueda de posición:** Comienza desde la raíz y compara el valor con cada nodo.
            
            **2. Decisión:** Si el valor es menor, va al subárbol izquierdo; si es mayor, al derecho.
            
            **3. Inserción:** Cuando encuentra un espacio vacío, crea un nuevo nodo.
            
            **Complejidad:** O(log n) en promedio, O(n) en el peor caso.
            """)
        elif tipo_arbol == "AVL":
            st.markdown("""
            ### 🔍 ¿Cómo funciona la inserción en AVL?
            
            **1. Inserción normal:** Igual que en ABB.
            
            **2. Actualización de alturas:** Se actualiza la altura de cada nodo.
            
            **3. Verificación de balance:** Se calcula el factor de balance (altura izquierda - altura derecha).
            
            **4. Rotaciones:** Si el factor es > 1 o < -1, se aplican rotaciones:
            - **Rotación derecha:** Cuando el subárbol izquierdo está más pesado
            - **Rotación izquierda:** Cuando el subárbol derecho está más pesado
            - **Rotación doble:** Casos más complejos
            
            **Complejidad:** O(log n) siempre (gracias al balanceo).
            """)
        elif tipo_arbol == "Rojo-Negro":
            st.markdown("""
            ### 🔍 ¿Cómo funciona la inserción en Rojo-Negro?
            
            **1. Inserción normal:** Igual que en ABB, pero el nuevo nodo es rojo.
            
            **2. Propiedades a mantener:**
            - Raíz negra
            - Nodos rojos no pueden tener hijos rojos
            - Todos los caminos tienen el mismo número de nodos negros
            
            **3. Rebalanceo:** Se aplican casos según la posición del tío:
            - **Caso 1:** Tío rojo → Recolorear
            - **Caso 2:** Tío negro y nodo en esquina → Rotación y recolorear
            - **Caso 3:** Tío negro y nodo en línea → Rotación simple
            
            **Complejidad:** O(log n) siempre.
            """)
        elif tipo_arbol == "Árbol B":
            st.markdown("""
            ### 🔍 ¿Cómo funciona la inserción en Árbol B?
            
            **1. Búsqueda de hoja:** Se busca la hoja donde debe ir el valor.
            
            **2. Inserción en hoja:** Se inserta en orden dentro de la hoja.
            
            **3. División:** Si la hoja está llena (2t-1 claves), se divide:
            - La clave media sube al padre
            - Se crean dos nuevas hojas
            
            **4. Propagación:** La división puede propagarse hacia arriba.
            
            **Complejidad:** O(log n) siempre.
            """)
        elif tipo_arbol == "Árbol B+":
            st.markdown("""
            ### 🔍 ¿Cómo funciona la inserción en B+?
            
            **1. Búsqueda de hoja:** Igual que en Árbol B.
            
            **2. Inserción en hoja:** Todas las claves van en las hojas.
            
            **3. División:** Similar a B, pero:
            - Las hojas mantienen todas las claves
            - Las claves de los nodos internos son copias
            
            **4. Enlaces:** Las hojas están enlazadas para recorridos secuenciales.
            
            **Complejidad:** O(log n) siempre.
            """)
    
    elif metodo == "buscar":
        st.markdown("""
        ### 🔍 ¿Cómo funciona la búsqueda?
        
        **1. Recorrido:** Comienza desde la raíz.
        
        **2. Comparación:** Compara el valor buscado con el nodo actual.
        
        **3. Decisión:** Si es igual → encontrado. Si es menor → va a la izquierda. Si es mayor → va a la derecha.
        
        **4. Resultado:** Si llega a None → no encontrado.
        
        **Complejidad:** O(log n) en promedio, O(n) en el peor caso (ABB no balanceado).
        """)
    
    elif metodo == "eliminar":
        if tipo_arbol == "ABB":
            st.markdown("""
            ### 🗑️ ¿Cómo funciona la eliminación en ABB?
            
            **1. Búsqueda del nodo:** Se busca el nodo a eliminar.
            
            **2. Caso 1 - Sin hijos:** Se elimina directamente.
            
            **3. Caso 2 - Un hijo:** Se reemplaza el nodo por su hijo.
            
            **4. Caso 3 - Dos hijos:** Se busca el sucesor (mínimo del subárbol derecho) y se reemplaza.
            
            **Complejidad:** O(log n) en promedio, O(n) en el peor caso.
            """)
        elif tipo_arbol == "AVL":
            st.markdown("""
            ### 🗑️ ¿Cómo funciona la eliminación en AVL?
            
            **1. Eliminación normal:** Igual que en ABB.
            
            **2. Actualización de alturas:** Se actualiza la altura de los nodos afectados.
            
            **3. Verificación de balance:** Se calcula el factor de balance.
            
            **4. Rotaciones:** Si está desbalanceado, se aplican rotaciones (igual que en inserción).
            
            **Complejidad:** O(log n) siempre.
            """)
        else:
            st.markdown(f"""
            ### 🗑️ ¿Cómo funciona la eliminación en {tipo_arbol}?
            
            El proceso de eliminación es similar al de ABB, pero con ajustes según el tipo de árbol:
            
            - **AVL:** Requiere rebalanceo después de la eliminación.
            - **Rojo-Negro:** Requiere rebalanceo para mantener las propiedades.
            - **Árbol B / B+:** Puede requerir redistribución o fusión de nodos.
            """)