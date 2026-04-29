import streamlit as st
import pandas as pd
from utils.db import get_all_products, create_order, get_all_orders, get_order_items, update_order_status


def show_pedidos():
    st.title("🛒 Gestión de Pedidos")
    st.caption("Registra pedidos, visualiza historial y actualiza estados.")

    tab1, tab2 = st.tabs(["Nuevo pedido", "Historial de pedidos"])

    with tab1:
        products = [p for p in get_all_products(active_only=True) if int(p["stock"]) > 0]

        if not products:
            st.warning("No hay productos activos con stock disponible.")
        else:
            with st.form("new_order_form", clear_on_submit=True):
                st.subheader("Datos del cliente")
                customer_name = st.text_input("Nombre del cliente")
                customer_phone = st.text_input("Teléfono")
                customer_address = st.text_input("Dirección")
                payment_method = st.selectbox("Método de pago", ["efectivo", "transferencia", "tarjeta"])
                notes = st.text_area("Notas")

                st.subheader("Productos del pedido")
                num_items = st.number_input(
                    "Número de productos diferentes",
                    min_value=1,
                    max_value=min(10, len(products)),
                    value=1,
                    step=1
                )

                option_map = {
                    f"{p['id']} - {p['name']} (${float(p['price']):.2f}) - stock {p['stock']}": p
                    for p in products
                }

                selected_labels = []
                quantities = []

                for i in range(num_items):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        selected = st.selectbox(
                            f"Producto #{i+1}",
                            list(option_map.keys()),
                            key=f"product_{i}"
                        )
                    with c2:
                        qty = st.number_input(
                            f"Cantidad #{i+1}",
                            min_value=1,
                            step=1,
                            key=f"qty_{i}"
                        )

                    selected_labels.append(selected)
                    quantities.append(qty)

                submitted = st.form_submit_button("Registrar pedido", use_container_width=True)

                if submitted:
                    clean_name = customer_name.strip()

                    if not clean_name:
                        st.warning("El nombre del cliente es obligatorio.")
                    elif len(set(selected_labels)) != len(selected_labels):
                        st.warning("No puedes repetir el mismo producto varias veces en un mismo pedido.")
                    else:
                        items = []
                        preview_rows = []
                        valid = True

                        for selected, qty in zip(selected_labels, quantities):
                            product = option_map[selected]
                            stock = int(product["stock"])
                            price = float(product["price"])

                            if qty > stock:
                                st.warning(f"La cantidad solicitada supera el stock disponible de {product['name']}.")
                                valid = False
                                break

                            subtotal = qty * price
                            items.append({
                                "product_id": product["id"],
                                "quantity": qty
                            })
                            preview_rows.append({
                                "Producto": product["name"],
                                "Cantidad": qty,
                                "Precio unitario": f"${price:.2f}",
                                "Subtotal": f"${subtotal:.2f}"
                            })

                        if valid:
                            st.markdown("### Resumen del pedido")
                            st.dataframe(pd.DataFrame(preview_rows), use_container_width=True, hide_index=True)

                            total = sum(
                                float(option_map[label]["price"]) * qty
                                for label, qty in zip(selected_labels, quantities)
                            )
                            st.info(f"Total del pedido: ${total:.2f}")

                            order_id = create_order(
                                customer_name=clean_name,
                                customer_phone=customer_phone,
                                customer_address=customer_address,
                                payment_method=payment_method,
                                notes=notes,
                                items=items
                            )

                            if order_id:
                                st.success(f"Pedido #{order_id} registrado correctamente.")
                                st.rerun()

    with tab2:
        orders = get_all_orders()

        if not orders:
            st.info("No hay pedidos registrados.")
        else:
            df = pd.DataFrame(orders)
            df["total"] = df["total"].astype(float).map(lambda x: f"${x:.2f}")

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

            order_map = {
                f"{o['id']} - {o['customer_name']} - ${float(o['total']):.2f}": o["id"]
                for o in orders
            }

            selected_order = st.selectbox("Selecciona un pedido", list(order_map.keys()))
            order_id = order_map[selected_order]

            st.markdown("### Detalle del pedido")
            items = get_order_items(order_id)
            if items:
                rows = []
                for item in items:
                    prod = item.get("products", {})
                    rows.append({
                        "Producto": prod.get("name", ""),
                        "Categoría": prod.get("category", ""),
                        "Cantidad": item.get("quantity", 0),
                        "Precio unitario": f"${float(item.get('unit_price', 0)):.2f}",
                        "Subtotal": f"${float(item.get('subtotal', 0)):.2f}",
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

            status = st.selectbox(
                "Actualizar estado",
                ["pendiente", "en preparación", "en camino", "entregado", "cancelado"]
            )

            if st.button("Actualizar estado del pedido", use_container_width=True):
                update_order_status(order_id, status)
                st.success("Estado actualizado correctamente.")
                st.rerun()