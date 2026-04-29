import streamlit as st
import pandas as pd
from utils.db import get_all_orders, update_order_status, get_order_items


def show_entregas():
    st.title("🚚 Gestión de Entregas")
    st.caption("Administra el estado de los pedidos en preparación, en camino y entregados.")

    orders = get_all_orders()

    if not orders:
        st.info("No hay pedidos registrados todavía.")
        return

    df = pd.DataFrame(orders)

    st.markdown("### Pedidos registrados")
    show_df = df.rename(columns={
        "id": "ID",
        "customer_name": "Cliente",
        "customer_phone": "Teléfono",
        "customer_address": "Dirección",
        "order_date": "Fecha",
        "status": "Estado",
        "payment_method": "Pago",
        "notes": "Notas",
        "total": "Total"
    })
    st.dataframe(show_df, use_container_width=True, hide_index=True)

    st.markdown("### Gestionar entrega")
    order_map = {
        f"{o['id']} - {o['customer_name']} - {o['status']} - ${float(o['total']):.2f}": o["id"]
        for o in orders
    }

    selected_order_label = st.selectbox("Selecciona un pedido", list(order_map.keys()))
    selected_order_id = order_map[selected_order_label]

    st.markdown("#### Detalle del pedido")
    items = get_order_items(selected_order_id)
    if items:
        detail_rows = []
        for item in items:
            prod = item.get("products", {})
            detail_rows.append({
                "Producto": prod.get("name", ""),
                "Categoría": prod.get("category", ""),
                "Cantidad": item.get("quantity", 0),
                "Precio unitario": item.get("unit_price", 0),
                "Subtotal": item.get("subtotal", 0),
            })
        st.dataframe(pd.DataFrame(detail_rows), use_container_width=True, hide_index=True)

    new_status = st.selectbox(
        "Nuevo estado",
        ["pendiente", "en preparación", "en camino", "entregado", "cancelado"]
    )

    if st.button("Actualizar entrega", use_container_width=True):
        update_order_status(selected_order_id, new_status)
        st.success("Estado de entrega actualizado correctamente.")
        st.rerun()