import os
import math
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.generate_product_dataset import generate_synthetic_product_sales_dataset
from utils.product_ml_model import (
    train_product_mlp_model,
    forecast_product_next_days,
    forecast_all_products_next_days,
    load_product_dataset
)


def classify_demand(value: float) -> str:
    if value >= 10:
        return "Alta"
    elif value >= 6:
        return "Media"
    return "Baja"


def production_recommendation(tomorrow_units: float) -> int:
    """
    Redondea hacia arriba y añade un pequeño margen de seguridad.
    """
    if tomorrow_units <= 0:
        return 0
    return math.ceil(tomorrow_units * 1.10)


def enrich_predictions(all_pred_df: pd.DataFrame) -> pd.DataFrame:
    df = all_pred_df.copy()
    df["demand_level"] = df["tomorrow_prediction"].apply(classify_demand)
    df["recommended_units_tomorrow"] = df["tomorrow_prediction"].apply(production_recommendation)

    def build_action(row):
        if row["demand_level"] == "Alta":
            return "Priorizar producción y abastecimiento"
        elif row["demand_level"] == "Media":
            return "Producción regular con seguimiento"
        return "Producción moderada"

    df["recommended_action"] = df.apply(build_action, axis=1)

    return df


def show_predicciones():
    st.title("📈 Predicciones por Producto")
    st.caption("Estimación de unidades vendidas para sanduches y postres usando un modelo MLP.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1. Dataset",
        "2. Entrenamiento",
        "3. Evaluación",
        "4. Predicción individual",
        "5. Predicción general y recomendaciones"
    ])

    with tab1:
        st.markdown("### Dataset sintético por producto")
        st.write("Genera un historial artificial de 3 meses para 10 productos.")

        if st.button("Generar dataset sintético por producto", use_container_width=True):
            df = generate_synthetic_product_sales_dataset()
            st.success("Dataset generado correctamente.")
            st.dataframe(df.tail(20), use_container_width=True, hide_index=True)

        if os.path.exists("data/product_sales_history.csv"):
            df = load_product_dataset()

            st.markdown("#### Vista previa")
            st.dataframe(df.tail(20), use_container_width=True, hide_index=True)

            daily_sum = df.groupby("date", as_index=False)["units_sold"].sum()
            fig = px.line(
                daily_sum,
                x="date",
                y="units_sold",
                title="Unidades vendidas por día (total)"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aún no existe el dataset. Genera uno primero.")

    with tab2:
        st.markdown("### Entrenamiento del modelo MLP")
        st.write("Se entrena un modelo para estimar cuántas unidades venderá cada producto.")

        if st.button("Entrenar modelo por producto", use_container_width=True):
            result = train_product_mlp_model()
            st.session_state["product_ml_result"] = result
            st.success("Modelo entrenado correctamente.")

            st.write("**Características usadas:**")
            st.write(result["feature_cols"])

    with tab3:
        st.markdown("### Evaluación del modelo")
        result = st.session_state.get("product_ml_result")

        if result is None:
            st.info("Primero debes entrenar el modelo.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                st.metric("MAE", f"{result['mae']:.4f}")
            with c2:
                st.metric("RMSE", f"{result['rmse']:.4f}")

            eval_df = pd.DataFrame({
                "Real": result["y_test"].values,
                "Predicción": result["y_pred"]
            })

            st.markdown("#### Primeras muestras de evaluación")
            st.dataframe(eval_df.head(30), use_container_width=True, hide_index=True)

            eval_plot_df = eval_df.head(50).reset_index().rename(columns={"index": "Muestra"})
            fig_eval = px.line(
                eval_plot_df,
                x="Muestra",
                y=["Real", "Predicción"],
                title="Comparación entre valores reales y predichos"
            )
            st.plotly_chart(fig_eval, use_container_width=True)

    with tab4:
        st.markdown("### Predicción individual por producto")

        if not os.path.exists("data/product_sales_history.csv"):
            st.warning("Primero genera el dataset sintético.")
        else:
            df = load_product_dataset()
            product_names = sorted(df["product_name"].unique())

            product_name = st.selectbox("Selecciona un producto", product_names)
            days = st.slider("Número de días a predecir", min_value=1, max_value=14, value=7, key="individual_days")

            if st.button("Predecir producto seleccionado", use_container_width=True):
                try:
                    pred_df = forecast_product_next_days(product_name, days=days)
                    st.success("Predicción generada correctamente.")

                    tomorrow_units = float(pred_df.iloc[0]["predicted_units"])
                    total_units = float(pred_df["predicted_units"].sum())
                    recommendation = production_recommendation(tomorrow_units)
                    demand = classify_demand(tomorrow_units)

                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.metric("Predicción para mañana", f"{tomorrow_units:.2f} unidades")
                    with c2:
                        st.metric(f"Predicción próximos {days} días", f"{total_units:.2f} unidades")
                    with c3:
                        st.metric("Preparación sugerida para mañana", f"{recommendation} unidades")

                    if demand == "Alta":
                        st.success("Demanda esperada alta. Se recomienda priorizar este producto.")
                    elif demand == "Media":
                        st.info("Demanda esperada media. Mantener producción regular.")
                    else:
                        st.warning("Demanda esperada baja. Producir con moderación.")

                    st.dataframe(pred_df, use_container_width=True, hide_index=True)

                    fig_pred = px.bar(
                        pred_df,
                        x="date",
                        y="predicted_units",
                        title=f"Predicción de unidades para {product_name}"
                    )
                    st.plotly_chart(fig_pred, use_container_width=True)
                except Exception as e:
                    st.error(f"Error al predecir: {e}")

    with tab5:
        st.markdown("### Predicción general y recomendaciones automáticas")

        if not os.path.exists("data/product_sales_history.csv"):
            st.warning("Primero genera el dataset sintético.")
        else:
            days_general = st.slider(
                "Número de días para la proyección general",
                min_value=1,
                max_value=14,
                value=7,
                key="general_days"
            )

            if st.button("Generar predicción general", use_container_width=True):
                try:
                    all_pred_df = forecast_all_products_next_days(days=days_general)
                    enriched_df = enrich_predictions(all_pred_df)

                    st.success("Predicción general generada correctamente.")

                    st.markdown("#### Resumen operativo")
                    top_product = enriched_df.iloc[0]["product_name"]
                    top_total = enriched_df.iloc[0]["next_days_total"]

                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.metric("Producto con mayor demanda proyectada", top_product)
                    with c2:
                        st.metric(f"Demanda proyectada próximos {days_general} días", f"{top_total:.2f} unidades")
                    with c3:
                        avg_tomorrow = enriched_df["tomorrow_prediction"].mean()
                        st.metric("Promedio de demanda para mañana", f"{avg_tomorrow:.2f} unidades")

                    display_df = enriched_df.rename(columns={
                        "product_name": "Producto",
                        "tomorrow_prediction": "Predicción mañana",
                        "next_days_total": f"Predicción próximos {days_general} días",
                        "demand_level": "Nivel de demanda",
                        "recommended_units_tomorrow": "Preparar mañana",
                        "recommended_action": "Acción recomendada"
                    })

                    st.dataframe(display_df, use_container_width=True, hide_index=True)

                    fig_all = px.bar(
                        enriched_df,
                        x="product_name",
                        y="next_days_total",
                        title=f"Predicción total por producto para los próximos {days_general} días"
                    )
                    st.plotly_chart(fig_all, use_container_width=True)

                    fig_tomorrow = px.bar(
                        enriched_df,
                        x="product_name",
                        y="recommended_units_tomorrow",
                        title="Producción sugerida para mañana"
                    )
                    st.plotly_chart(fig_tomorrow, use_container_width=True)

                    st.markdown("#### Recomendaciones destacadas")
                    high_demand = enriched_df[enriched_df["demand_level"] == "Alta"]["product_name"].tolist()
                    medium_demand = enriched_df[enriched_df["demand_level"] == "Media"]["product_name"].tolist()

                    if high_demand:
                        st.success("Priorizar producción de: " + ", ".join(high_demand))
                    if medium_demand:
                        st.info("Mantener producción estable para: " + ", ".join(medium_demand))
                    if not high_demand and not medium_demand:
                        st.warning("La mayoría de productos tienen demanda baja proyectada.")
                except Exception as e:
                    st.error(f"Error al generar la predicción general: {e}")