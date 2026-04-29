import streamlit as st


def render_header():
    st.markdown('<div class="main-title">Panel Principal</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Bienvenida al sistema de gestión de tu negocio. Administra productos, ventas, inventario y reportes desde un solo lugar.</div>',
        unsafe_allow_html=True
    )