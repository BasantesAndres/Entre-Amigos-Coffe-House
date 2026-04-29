import streamlit as st
import pandas as pd
from datetime import date
from utils.db import get_all_products, get_daily_menu, add_product_to_daily_menu, remove_product_from_daily_menu


def show_menu_diario():
    st.title("📅 Menú Diario")
    selected_date = st.date_input("Fecha del menú", value=date.today())

    tab1, tab2 = st.tabs(["Menú actual", "Agregar productos"])

    with tab1:
        menu_items = get_daily_menu(selected_date.isoformat())
        if not menu_items:
            st.info("No hay productos en el menú de esta fecha.")
        else:
            rows = []
            for item in menu_items:
                prod = item.get("products", {})
                rows.append({
                    "Menu ID": item["id"],
                    "Fecha": item["menu_date"],
                    "Producto": prod.get("name", ""),
                    "Categoría": prod.get("category", ""),
                    "Precio": prod.get("price", 0),
                    "Stock": prod.get("stock", 0),
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

            ids = {f"{r['Menu ID']} - {r['Producto']}": r["Menu ID"] for r in rows}
            selected_remove = st.selectbox("Selecciona un producto del menú para eliminar", list(ids.keys()))
            if st.button("Eliminar del menú", use_container_width=True):
                remove_product_from_daily_menu(ids[selected_remove])
                st.success("Producto eliminado del menú.")
                st.rerun()

    with tab2:
        products = get_all_products(active_only=True)
        menu_items = get_daily_menu(selected_date.isoformat())
        menu_product_ids = {item["product_id"] for item in menu_items}

        available_products = [p for p in products if p["id"] not in menu_product_ids]

        if not available_products:
            st.info("No hay productos disponibles para agregar.")
        else:
            options = {
                f"{p['id']} - {p['name']} (${float(p['price']):.2f})": p["id"]
                for p in available_products
            }
            selected = st.selectbox("Selecciona un producto", list(options.keys()))
            if st.button("Agregar al menú", use_container_width=True):
                result = add_product_to_daily_menu(options[selected], selected_date.isoformat(), True)
                if result:
                    st.success("Producto agregado al menú.")
                    st.rerun()