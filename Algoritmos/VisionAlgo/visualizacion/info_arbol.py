"""
Información y estadísticas de árboles binarios y B-Trees.
"""

import streamlit as st

def es_nodo_b(nodo):
    """Verifica si un nodo es de tipo B (tiene claves y hijos)."""
    return hasattr(nodo, 'claves') and hasattr(nodo, 'hijos')

def obtener_info_arbol(raiz):
    """
    Obtiene información estadística del árbol (binario o B).
    """
    if raiz is None:
        return {
            "altura": 0,
            "tamaño": 0,
            "nodos_hoja": 0,
            "nodos_internos": 0,
            "nivel_maximo": 0,
            "es_completo": True,
            "es_balanceado": True,
            "factor_balance": 0,
            "tipo": "vacío"
        }
    
    # ========== DETECTAR TIPO DE ÁRBOL ==========
    if es_nodo_b(raiz):
        return _obtener_info_arbol_b(raiz)
    else:
        return _obtener_info_arbol_binario(raiz)

def _obtener_info_arbol_b(raiz):
    """Información para árboles B (multinodo)."""
    
    def calcular_altura_b(nodo):
        if nodo is None or len(nodo.claves) == 0:
            return 0
        if nodo.hoja:
            return 1
        return 1 + max(calcular_altura_b(hijo) for hijo in nodo.hijos if hijo is not None)
    
    def calcular_tamaño_b(nodo):
        if nodo is None or len(nodo.claves) == 0:
            return 0
        return 1 + sum(calcular_tamaño_b(hijo) for hijo in nodo.hijos if hijo is not None)
    
    def contar_hojas_b(nodo):
        if nodo is None or len(nodo.claves) == 0:
            return 0
        if nodo.hoja:
            return 1
        return sum(contar_hojas_b(hijo) for hijo in nodo.hijos if hijo is not None)
    
    def contar_internos_b(nodo):
        if nodo is None or len(nodo.claves) == 0:
            return 0
        if not nodo.hoja:
            return 1 + sum(contar_internos_b(hijo) for hijo in nodo.hijos if hijo is not None)
        return 0
    
    def nivel_maximo_b(nodo, nivel=0):
        if nodo is None or len(nodo.claves) == 0:
            return nivel - 1
        if nodo.hoja:
            return nivel
        return max(nivel_maximo_b(hijo, nivel + 1) for hijo in nodo.hijos if hijo is not None)
    
    altura = calcular_altura_b(raiz)
    tamaño = calcular_tamaño_b(raiz)
    hojas = contar_hojas_b(raiz)
    internos = contar_internos_b(raiz)
    nivel_max = nivel_maximo_b(raiz)
    
    return {
        "altura": altura,
        "tamaño": tamaño,
        "nodos_hoja": hojas,
        "nodos_internos": internos,
        "nivel_maximo": nivel_max,
        "es_completo": True,  # Los árboles B siempre son completos
        "es_balanceado": True,  # Los árboles B siempre son balanceados
        "factor_balance": 0,
        "tipo": "B-Tree",
        "grado": len(raiz.claves) if raiz.claves else 0
    }

def _obtener_info_arbol_binario(raiz):
    """Información para árboles binarios (ABB, AVL, Rojo-Negro)."""
    
    def calcular_altura(nodo):
        if nodo is None:
            return 0
        return 1 + max(calcular_altura(nodo.izquierdo), calcular_altura(nodo.derecho))
    
    def calcular_tamaño(nodo):
        if nodo is None:
            return 0
        return 1 + calcular_tamaño(nodo.izquierdo) + calcular_tamaño(nodo.derecho)
    
    def contar_hojas(nodo):
        if nodo is None:
            return 0
        if nodo.izquierdo is None and nodo.derecho is None:
            return 1
        return contar_hojas(nodo.izquierdo) + contar_hojas(nodo.derecho)
    
    def contar_internos(nodo):
        if nodo is None:
            return 0
        if nodo.izquierdo is not None or nodo.derecho is not None:
            return 1 + contar_internos(nodo.izquierdo) + contar_internos(nodo.derecho)
        return contar_internos(nodo.izquierdo) + contar_internos(nodo.derecho)
    
    def calcular_nivel_maximo(nodo, nivel=0):
        if nodo is None:
            return nivel - 1
        return max(calcular_nivel_maximo(nodo.izquierdo, nivel + 1),
                   calcular_nivel_maximo(nodo.derecho, nivel + 1))
    
    def es_completo(nodo, indice=0, tamaño=0):
        if nodo is None:
            return True
        if indice >= tamaño:
            return False
        return (es_completo(nodo.izquierdo, 2 * indice + 1, tamaño) and
                es_completo(nodo.derecho, 2 * indice + 2, tamaño))
    
    def es_balanceado(nodo):
        if nodo is None:
            return True
        altura_izq = calcular_altura(nodo.izquierdo)
        altura_der = calcular_altura(nodo.derecho)
        if abs(altura_izq - altura_der) > 1:
            return False
        return es_balanceado(nodo.izquierdo) and es_balanceado(nodo.derecho)
    
    def factor_balance(nodo):
        if nodo is None:
            return 0
        return calcular_altura(nodo.izquierdo) - calcular_altura(nodo.derecho)
    
    altura = calcular_altura(raiz)
    tamaño = calcular_tamaño(raiz)
    hojas = contar_hojas(raiz)
    internos = contar_internos(raiz)
    nivel_max = calcular_nivel_maximo(raiz)
    completo = es_completo(raiz, 0, tamaño)
    balanceado = es_balanceado(raiz)
    factor_bal = factor_balance(raiz)
    
    return {
        "altura": altura,
        "tamaño": tamaño,
        "nodos_hoja": hojas,
        "nodos_internos": internos,
        "nivel_maximo": nivel_max,
        "es_completo": completo,
        "es_balanceado": balanceado,
        "factor_balance": factor_bal,
        "tipo": "Binario"
    }

def obtener_info_nodo(nodo, raiz):
    """
    Obtiene información de un nodo específico (binario o B).
    """
    if nodo is None:
        return None
    
    # ========== NODO B ==========
    if es_nodo_b(nodo):
        info = {
            "valor": nodo.claves,
            "claves": nodo.claves.copy(),
            "es_hoja": nodo.hoja,
            "hijos": len(nodo.hijos),
            "tipo": "B",
            "padre": None,
            "nivel": None
        }
        
        # Buscar padre y nivel
        if raiz:
            def buscar_en_b(actual, objetivo, nivel=0):
                if actual is None or len(actual.claves) == 0:
                    return None, None
                if actual == objetivo:
                    return None, nivel
                if actual.hoja:
                    return None, None
                for hijo in actual.hijos:
                    if hijo == objetivo:
                        return actual, nivel + 1
                    padre, niv = buscar_en_b(hijo, objetivo, nivel + 1)
                    if padre is not None:
                        return padre, niv
                return None, None
            
            padre, nivel = buscar_en_b(raiz, nodo)
            info["padre"] = padre.claves if padre else None
            info["nivel"] = nivel
        
        return info
    
    # ========== NODO BINARIO ==========
    info = {
        "valor": nodo.valor,
        "izquierdo": nodo.izquierdo.valor if nodo.izquierdo else None,
        "derecho": nodo.derecho.valor if nodo.derecho else None,
        "altura": getattr(nodo, "altura", None),
        "color": getattr(nodo, "color", None),
        "padre": None,
        "nivel": None,
        "es_hoja": nodo.izquierdo is None and nodo.derecho is None,
        "es_raiz": nodo == raiz,
        "tiene_hijos": nodo.izquierdo is not None or nodo.derecho is not None,
        "factor_balance": None,
        "tipo": "Binario"
    }
    
    # Calcular factor de balance (si tiene atributo altura)
    if hasattr(nodo, "altura"):
        altura_izq = nodo.izquierdo.altura if nodo.izquierdo and hasattr(nodo.izquierdo, "altura") else 0
        altura_der = nodo.derecho.altura if nodo.derecho and hasattr(nodo.derecho, "altura") else 0
        info["factor_balance"] = altura_izq - altura_der
    
    # Buscar padre y nivel
    if raiz:
        def buscar_padre_nivel(actual, valor, padre=None, nivel=0):
            if actual is None:
                return None, None
            if actual == nodo:
                return padre, nivel
            if valor < actual.valor:
                return buscar_padre_nivel(actual.izquierdo, valor, actual, nivel + 1)
            else:
                return buscar_padre_nivel(actual.derecho, valor, actual, nivel + 1)
        
        padre, nivel = buscar_padre_nivel(raiz, nodo.valor)
        info["padre"] = padre.valor if padre else None
        info["nivel"] = nivel
    
    return info

def mostrar_info_arbol(raiz, titulo="📊 Información del árbol"):
    """
    Muestra la información del árbol en un formato amigable.
    """
    if raiz is None:
        st.warning("🌱 El árbol está vacío")
        return None
    
    info = obtener_info_arbol(raiz)
    
    st.markdown(f"### {titulo}")
    
    # ========== MOSTRAR SEGÚN TIPO ==========
    if info.get("tipo") == "B-Tree":
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🌳 Altura", info["altura"])
            st.metric("📏 Tamaño", info["tamaño"])
            st.metric("🍃 Nodos hoja", info["nodos_hoja"])
        with col2:
            st.metric("📐 Nodos internos", info["nodos_internos"])
            st.metric("📊 Nivel máximo", info["nivel_maximo"])
            st.metric("📌 Grado (claves/nodo)", info.get("grado", 0))
        with col3:
            st.metric("✅ Balanceado", "Sí" if info["es_balanceado"] else "No")
            st.metric("📋 Tipo", info.get("tipo", "B-Tree"))
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🌳 Altura", info["altura"])
            st.metric("📏 Tamaño", info["tamaño"])
            st.metric("🍃 Nodos hoja", info["nodos_hoja"])
        with col2:
            st.metric("📐 Nodos internos", info["nodos_internos"])
            st.metric("📊 Nivel máximo", info["nivel_maximo"])
            st.metric("⚖️ Factor de balance", info["factor_balance"])
        with col3:
            st.metric("✅ ¿Completo?", "Sí" if info["es_completo"] else "No")
            st.metric("⚖️ ¿Balanceado?", "Sí" if info["es_balanceado"] else "No")
    
    return info

def mostrar_info_nodo(nodo, raiz):
    """
    Muestra la información de un nodo específico.
    """
    if nodo is None:
        st.warning("⚠️ No hay nodo seleccionado")
        return
    
    info = obtener_info_nodo(nodo, raiz)
    
    # ========== NODO B ==========
    if info.get("tipo") == "B":
        st.markdown(f"### 🔍 Información del nodo B")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📌 Claves", str(info["claves"]))
            st.metric("🍃 ¿Es hoja?", "✅ Sí" if info["es_hoja"] else "❌ No")
        with col2:
            st.metric("👨‍👦 Hijos", info["hijos"])
            st.metric("👨‍👧‍👦 Padre", str(info["padre"]) if info["padre"] else "None (Raíz)")
        with col3:
            st.metric("📊 Nivel", info["nivel"] if info["nivel"] is not None else "-")
        return
    
    # ========== NODO BINARIO ==========
    st.markdown(f"### 🔍 Información del nodo {info['valor']}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📌 Valor", info["valor"])
        st.metric("👨‍👦 Hijo izquierdo", info["izquierdo"] if info["izquierdo"] is not None else "None")
        st.metric("👨‍👦 Hijo derecho", info["derecho"] if info["derecho"] is not None else "None")
    with col2:
        st.metric("👨‍👧‍👦 Padre", info["padre"] if info["padre"] is not None else "None (Raíz)")
        st.metric("📊 Nivel", info["nivel"] if info["nivel"] is not None else "-")
        st.metric("📏 Altura", info["altura"] if info["altura"] is not None else "-")
    with col3:
        st.metric("🍃 ¿Es hoja?", "✅ Sí" if info["es_hoja"] else "❌ No")
        st.metric("👑 ¿Es raíz?", "✅ Sí" if info["es_raiz"] else "❌ No")
        st.metric("⚖️ Factor balance", info["factor_balance"] if info["factor_balance"] is not None else "-")