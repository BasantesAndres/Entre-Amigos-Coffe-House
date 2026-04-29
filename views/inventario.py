import streamlit as st
import pandas as pd
from utils.db import get_all_products, register_inventory_movement, get_inventory_movements


def show_inventario():
    st.title("🧾 Control de Inventario")

    tab1, tab2 = st.tabs(["Movimientos", "Historial"])

    with tab1:
        products = get_all_products()
        if not products:
            st.info("No hay productos registrados.")
        else:
            with st.form("inventory_form", clear_on_submit=True):
                option_map = {f"{p['id']} - {p['name']} (stock: {p['stock']})": p["id"] for p in products}
                selected = st.selectbox("Producto", list(option_map.keys()))
                movement_type = st.selectbox("Tipo de movimiento", ["entrada", "salida", "ajuste"])
                quantity = st.number_input("Cantidad", min_value=0, step=1)
                reason = st.text_input("Motivo")
                submitted = st.form_submit_button("Registrar movimiento", use_container_width=True)

                if submitted:
                    if quantity < 0:
                        st.warning("La cantidad no puede ser negativa.")
                    else:
                        ok = register_inventory_movement(option_map[selected], movement_type, quantity, reason)
                        if ok:
                            st.success("Movimiento registrado correctamente.")
                            st.rerun()

    with tab2:
        rows = get_inventory_movements()
        if not rows:
            st.info("No hay movimientos registrados.")
        else:
            parsed = []
            for row in rows:
                prod = row.get("products", {})
                parsed.append({
                    "ID": row["id"],
                    "Producto": prod.get("name", ""),
                    "Categoría": prod.get("category", ""),
                    "Tipo": row["movement_type"],
                    "Cantidad": row["quantity"],
                    "Motivo": row["reason"],
                    "Fecha": row["created_at"],
                })
            st.dataframe(pd.DataFrame(parsed), use_container_width=True, hide_index=True)