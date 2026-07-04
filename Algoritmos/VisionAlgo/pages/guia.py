import streamlit as st
from utils.guia_usuario import mostrar_guia

st.set_page_config(
    page_title="AlgoVision - Guía de usuario",
    page_icon="📖",
    layout="wide"
)

st.title("📖 Guía de usuario de AlgoVision")
st.markdown("---")

mostrar_guia()

st.markdown("---")
st.caption("📖 Guía de usuario | SIS210 - Algoritmos y Estructuras de Datos")