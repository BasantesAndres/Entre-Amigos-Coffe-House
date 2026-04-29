import streamlit as st
from utils.auth import logout


def render_sidebar():
    with st.sidebar:
        st.markdown("## 🍰 Dulce Gestión")
        st.caption("Sistema de gestión del negocio")
        st.write("")

        menu_items = [
            ("dashboard", "🏠 Inicio"),
            ("productos", "📦 Productos"),
            ("menu_diario", "📅 Menú Diario"),
            ("pedidos", "🛒 Pedidos"),
            ("entregas", "🚚 Entregas"),
            ("reportes", "📊 Reportes"),
            ("predicciones", "📈 Predicciones"),
            ("inventario", "🧾 Inventario"),
            ("autorespuestas", "💬 Auto Respuestas"),
        ]

        current_page = st.session_state.get("page", "dashboard")

        for key, label in menu_items:
            button_type = "primary" if current_page == key else "secondary"
            if st.button(label, use_container_width=True, type=button_type):
                st.session_state["page"] = key
                st.rerun()

        st.write("---")
        st.markdown(f"**Usuario:** {st.session_state.get('user_email', 'Sin sesión')}")
        st.markdown("**Estado:** Activo")

        if st.button("Cerrar sesión", use_container_width=True):
            logout()