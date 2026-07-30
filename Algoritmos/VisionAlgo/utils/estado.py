"""
Manejo del estado global de Streamlit para la animación.
"""

import streamlit as st

def inicializar_estado_ordenamiento():
    """Inicializa las variables de sesión para el módulo de ordenamiento."""
    if "ordenamiento_generador" not in st.session_state:
        st.session_state.ordenamiento_generador = None
    if "ordenamiento_pausado" not in st.session_state:
        st.session_state.ordenamiento_pausado = True
    if "ordenamiento_ejecutando" not in st.session_state:
        st.session_state.ordenamiento_ejecutando = False
    if "ordenamiento_velocidad" not in st.session_state:
        st.session_state.ordenamiento_velocidad = 0.5  # segundos entre pasos
    if "ordenamiento_lista_original" not in st.session_state:
        st.session_state.ordenamiento_lista_original = None
    if "ordenamiento_paso_actual" not in st.session_state:
        st.session_state.ordenamiento_paso_actual = 0
    if "ordenamiento_terminado" not in st.session_state:
        st.session_state.ordenamiento_terminado = False

def reiniciar_animacion():
    """Reinicia el estado de la animación."""
    st.session_state.ordenamiento_generador = None
    st.session_state.ordenamiento_pausado = False
    st.session_state.ordenamiento_paso_actual = 0
    st.session_state.ordenamiento_terminado = False