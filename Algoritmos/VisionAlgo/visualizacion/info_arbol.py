"""
Información y estadísticas de árboles binarios.
"""

import streamlit as st

def obtener_info_arbol(raiz):
    """
    Obtiene información estadística del árbol.
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
            "factor_balance": 0
        }
    
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
        "factor_balance": factor_bal
    }

def obtener_info_nodo(nodo, raiz):
    """
    Obtiene información de un nodo específico.
    """
    if nodo is None:
        return None
    
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
        "factor_balance": None
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
    
    st.markdown(f"### 🔍 Información del nodo {nodo.valor}")
    
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