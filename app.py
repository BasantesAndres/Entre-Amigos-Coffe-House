import streamlit as st

from utils.state import init_state
from utils.styles import load_global_styles
from utils.auth import login_user
from components.sidebar import render_sidebar

from views.dashboard import show_dashboard
from views.productos import show_productos
from views.menu_diario import show_menu_diario
from views.pedidos import show_pedidos
from views.entregas import show_entregas
from views.reportes import show_reportes
from views.predicciones import show_predicciones
from views.inventario import show_inventario
from views.autorespuestas import show_autorespuestas


st.set_page_config(
    page_title="Dulce Gestión",
    page_icon="🍰",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_state()
load_global_styles()


def show_login():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="brand-title">Dulce Gestión</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">Inicia sesión para acceder al sistema</div>', unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Iniciar Sesión", use_container_width=True)

        if submitted:
            if not email or not password:
                st.warning("Completa todos los campos.")
            else:
                ok = login_user(email, password)
                if ok:
                    st.success("Inicio de sesión exitoso.")
                    st.rerun()
                else:
                    st.error("Correo o contraseña incorrectos.")

    st.markdown('</div>', unsafe_allow_html=True)


def show_current_page():
    page = st.session_state.get("page", "dashboard")

    if page == "dashboard":
        show_dashboard()
    elif page == "productos":
        show_productos()
    elif page == "menu_diario":
        show_menu_diario()
    elif page == "pedidos":
        show_pedidos()
    elif page == "entregas":
        show_entregas()
    elif page == "reportes":
        show_reportes()
    elif page == "predicciones":
        show_predicciones()
    elif page == "inventario":
        show_inventario()
    elif page == "autorespuestas":
        show_autorespuestas()
    else:
        show_dashboard()


if not st.session_state["authenticated"]:
    show_login()
else:
    render_sidebar()
    show_current_page()