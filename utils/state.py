import streamlit as st


def init_state():
    defaults = {
        "authenticated": False,
        "page": "dashboard",
        "user_email": None,
        "access_token": None,
        "refresh_token": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value