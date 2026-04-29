import streamlit as st
from datetime import datetime
from components.cards import stat_card
from components.header import render_header
from utils.db import get_dashboard_stats


def show_dashboard():
    render_header()
    stats = get_dashboard_stats()

    c1, c2, c3 = st.columns(3)
    with c1:
        stat_card("Productos Totales", str(stats["total_products"]))
    with c2:
        stat_card("En Menú Hoy", str(stats["menu_today"]))
    with c3:
        stat_card("Pedidos Hoy", str(stats["orders_today"]))

    c4, c5 = st.columns(2)
    with c4:
        stat_card("Stock Bajo", str(stats["low_stock"]))
    with c5:
        stat_card("Ganancia Hoy", f"${stats['sales_today']:.2f}")

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown('<div class="panel-box">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Acceso Rápido</div>', unsafe_allow_html=True)

        if st.button("📝 Nuevo Pedido", use_container_width=True):
            st.session_state["page"] = "pedidos"
            st.rerun()

        if st.button("📅 Configurar Menú del Día", use_container_width=True):
            st.session_state["page"] = "menu_diario"
            st.rerun()

        if st.button("📦 Gestionar Productos", use_container_width=True):
            st.session_state["page"] = "productos"
            st.rerun()

        if st.button("📊 Ver Reportes", use_container_width=True):
            st.session_state["page"] = "reportes"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        now = datetime.now()
        st.markdown('<div class="panel-box">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Información del Sistema</div>', unsafe_allow_html=True)
        st.write("🟢 Sistema operativo")
        st.write("Horario configurado: 3:00 PM - 9:00 PM")
        st.write(f"Fecha actual: {now.strftime('%d/%m/%Y')}")
        st.write(f"Usuario autenticado: {st.session_state.get('user_email', 'No autenticado')}")
        st.markdown('</div>', unsafe_allow_html=True)