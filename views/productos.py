import streamlit as st
import pandas as pd
from utils.db import (
    get_all_products,
    create_product,
    update_product,
    delete_product,
    get_product_by_id
)


def show_productos():
    st.title("📦 Gestión de Productos")
    st.caption("Administra productos, stock, stock mínimo y estado de activación.")

    tab1, tab2, tab3 = st.tabs(["Lista", "Nuevo", "Editar / Eliminar"])

    with tab1:
        products = get_all_products()

        if not products:
            st.warning("No hay productos registrados todavía.")
        else:
            df = pd.DataFrame(products)

            search = st.text_input("Buscar por nombre o categoría")
            if search:
                df = df[
                    df["name"].astype(str).str.contains(search, case=False, na=False) |
                    df["category"].astype(str).str.contains(search, case=False, na=False)
                ]

            if "price" in df.columns:
                df["price"] = df["price"].astype(float).map(lambda x: f"${x:.2f}")

            if "created_at" in df.columns:
                df["created_at"] = df["created_at"].astype(str).str[:19]

            df = df.rename(columns={
                "id": "ID",
                "name": "Nombre",
                "category": "Categoría",
                "price": "Precio",
                "stock": "Stock",
                "min_stock": "Stock mínimo",
                "description": "Descripción",
                "is_active": "Activo",
                "created_at": "Creado"
            })

            desired_order = [
                "ID", "Nombre", "Categoría", "Precio", "Stock",
                "Stock mínimo", "Activo", "Descripción", "Creado"
            ]
            existing_order = [c for c in desired_order if c in df.columns]
            df = df[existing_order]

            st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("### Registrar nuevo producto")
        with st.form("new_product_form", clear_on_submit=True):
            c1, c2 = st.columns(2)

            with c1:
                name = st.text_input("Nombre")
                category = st.selectbox(
                    "Categoría",
                    ["Tortas", "Cupcakes", "Galletas", "Postres", "Bebidas", "Snacks", "Otro"]
                )
                price = st.number_input("Precio", min_value=0.0, step=0.5, format="%.2f")

            with c2:
                stock = st.number_input("Stock inicial", min_value=0, step=1)
                min_stock = st.number_input("Stock mínimo", min_value=0, step=1, value=3)
                is_active = st.checkbox("Activo", value=True)

            description = st.text_area("Descripción")
            submitted = st.form_submit_button("Guardar producto", use_container_width=True)

            if submitted:
                clean_name = name.strip()
                existing_names = [p.get("name", "").strip().lower() for p in get_all_products()]

                if not clean_name:
                    st.warning("El nombre del producto es obligatorio.")
                elif clean_name.lower() in existing_names:
                    st.warning("Ya existe un producto con ese nombre.")
                else:
                    result = create_product(
                        clean_name,
                        category,
                        price,
                        stock,
                        min_stock,
                        description,
                        is_active
                    )

                    if result:
                        st.success("Producto guardado correctamente.")
                        st.rerun()
                    else:
                        st.error("No se pudo guardar el producto.")

    with tab3:
        products = get_all_products()
        if not products:
            st.info("No hay productos disponibles.")
            return

        options = {
            f"{p['id']} - {p['name']} ({p['category']})": p["id"]
            for p in products
        }

        selected = st.selectbox("Selecciona un producto", list(options.keys()))
        product_id = options[selected]
        product = get_product_by_id(product_id)

        if product:
            with st.form("edit_product_form"):
                c1, c2 = st.columns(2)
                categories = ["Tortas", "Cupcakes", "Galletas", "Postres", "Bebidas", "Snacks", "Otro"]
                idx = categories.index(product["category"]) if product["category"] in categories else len(categories) - 1

                with c1:
                    name = st.text_input("Nombre", value=product.get("name", ""))
                    category = st.selectbox("Categoría", categories, index=idx)
                    price = st.number_input(
                        "Precio",
                        min_value=0.0,
                        value=float(product.get("price", 0)),
                        step=0.5,
                        format="%.2f"
                    )

                with c2:
                    stock = st.number_input(
                        "Stock",
                        min_value=0,
                        value=int(product.get("stock", 0)),
                        step=1
                    )
                    min_stock = st.number_input(
                        "Stock mínimo",
                        min_value=0,
                        value=int(product.get("min_stock", 3)),
                        step=1
                    )
                    is_active = st.checkbox("Activo", value=product.get("is_active", True))

                description = st.text_area("Descripción", value=product.get("description", ""))

                col_save, col_delete = st.columns(2)
                with col_save:
                    save_btn = st.form_submit_button("Actualizar producto", use_container_width=True)
                with col_delete:
                    delete_btn = st.form_submit_button("Eliminar producto", use_container_width=True)

                if save_btn:
                    clean_name = name.strip()
                    if not clean_name:
                        st.warning("El nombre del producto es obligatorio.")
                    else:
                        result = update_product(
                            product_id,
                            clean_name,
                            category,
                            price,
                            stock,
                            min_stock,
                            description,
                            is_active
                        )
                        if result is not None:
                            st.success("Producto actualizado correctamente.")
                            st.rerun()

                if delete_btn:
                    result = delete_product(product_id)
                    if result is not None:
                        st.success("Producto eliminado correctamente.")
                        st.rerun()