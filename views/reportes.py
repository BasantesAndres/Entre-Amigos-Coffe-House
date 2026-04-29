import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import get_sales_by_day, get_top_selling_products, get_all_orders


def show_reportes():
    st.title("📊 Reportes de Ventas")
    st.caption("Analiza el comportamiento de ventas del negocio mediante métricas y gráficas.")

    orders = get_all_orders()
    sales_by_day = get_sales_by_day()
    top_products = get_top_selling_products()

    if not orders:
        st.info("No hay ventas registradas todavía.")
        return

    total_income = sum(float(o.get("total", 0)) for o in orders)
    avg_ticket = total_income / len(orders) if orders else 0

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Pedidos totales", len(orders))
    with c2:
        st.metric("Ingresos acumulados", f"${total_income:.2f}")
    with c3:
        st.metric("Ticket promedio", f"${avg_ticket:.2f}")

    st.markdown("### Ventas por día")
    if sales_by_day:
        df_sales = pd.DataFrame(sales_by_day)
        df_sales["sales"] = df_sales["sales"].astype(float)

        fig = px.bar(
            df_sales,
            x="date",
            y="sales",
            title="Ventas por día",
            labels={"date": "Fecha", "sales": "Ventas"}
        )
        st.plotly_chart(fig, use_container_width=True)

        display_sales = df_sales.copy()
        display_sales["sales"] = display_sales["sales"].map(lambda x: f"${x:.2f}")
        display_sales = display_sales.rename(columns={"date": "Fecha", "sales": "Ventas"})
        st.dataframe(display_sales, use_container_width=True, hide_index=True)

    st.markdown("### Productos más vendidos")
    if top_products:
        df_top = pd.DataFrame(top_products[:10])

        fig2 = px.bar(
            df_top,
            x="product",
            y="quantity",
            title="Top productos vendidos",
            labels={"product": "Producto", "quantity": "Cantidad vendida"}
        )
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.pie(
            df_top,
            names="product",
            values="quantity",
            title="Participación por producto"
        )
        st.plotly_chart(fig3, use_container_width=True)

        display_top = df_top.rename(columns={
            "product": "Producto",
            "quantity": "Cantidad vendida"
        })
        st.dataframe(display_top, use_container_width=True, hide_index=True)

        best_product = df_top.iloc[0]["product"]
        best_quantity = int(df_top.iloc[0]["quantity"])
        st.success(f"Producto más vendido: {best_product} con {best_quantity} unidades.")
    else:
        st.info("Todavía no hay productos vendidos.")

    st.markdown("### Historial general de ventas")
    df_orders = pd.DataFrame(orders)
    df_orders["total"] = df_orders["total"].astype(float).map(lambda x: f"${x:.2f}")

    display_orders = df_orders.rename(columns={
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

    st.dataframe(display_orders, use_container_width=True, hide_index=True)