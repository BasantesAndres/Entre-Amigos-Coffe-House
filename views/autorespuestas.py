import streamlit as st
import pandas as pd


def generate_message(message_type, customer_name, order_id=None, extra_text=""):
    customer_name = customer_name.strip() if customer_name else "cliente"

    templates = {
        "confirmacion": f"Hola {customer_name}, tu pedido ha sido recibido correctamente. En breve iniciaremos su preparación. {extra_text}".strip(),
        "preparacion": f"Hola {customer_name}, tu pedido ya está en preparación. Te avisaremos cuando esté listo para salir. {extra_text}".strip(),
        "camino": f"Hola {customer_name}, tu pedido está en camino. Gracias por tu compra. {extra_text}".strip(),
        "entregado": f"Hola {customer_name}, tu pedido ha sido entregado con éxito. Esperamos que disfrutes tu compra. {extra_text}".strip(),
        "promocion": f"Hola {customer_name}, tenemos novedades y promociones especiales disponibles hoy. {extra_text}".strip(),
    }

    base = templates.get(message_type, "")
    if order_id:
        base = f"Pedido #{order_id}. {base}"
    return base


def show_autorespuestas():
    st.title("💬 Auto Respuestas")
    st.caption("Generador de mensajes automáticos para clientes.")

    tab1, tab2 = st.tabs(["Generar mensaje", "Plantillas disponibles"])

    with tab1:
        with st.form("message_form"):
            customer_name = st.text_input("Nombre del cliente")
            order_id = st.text_input("ID del pedido (opcional)")
            message_type = st.selectbox(
                "Tipo de mensaje",
                ["confirmacion", "preparacion", "camino", "entregado", "promocion"]
            )
            extra_text = st.text_area("Texto adicional opcional")
            submitted = st.form_submit_button("Generar mensaje", use_container_width=True)

            if submitted:
                msg = generate_message(message_type, customer_name, order_id, extra_text)
                st.success("Mensaje generado correctamente.")
                st.text_area("Mensaje listo para copiar", value=msg, height=180)

    with tab2:
        templates = [
            {"Tipo": "confirmacion", "Uso": "Cuando el pedido ha sido recibido"},
            {"Tipo": "preparacion", "Uso": "Cuando el pedido está siendo elaborado"},
            {"Tipo": "camino", "Uso": "Cuando el pedido salió a entrega"},
            {"Tipo": "entregado", "Uso": "Cuando el cliente ya recibió el pedido"},
            {"Tipo": "promocion", "Uso": "Para enviar mensajes promocionales"},
        ]
        st.dataframe(pd.DataFrame(templates), use_container_width=True, hide_index=True)