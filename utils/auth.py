import streamlit as st
from supabase import create_client, Client


def clear_session():
    st.session_state["authenticated"] = False
    st.session_state["user_email"] = None
    st.session_state["page"] = "login"
    st.session_state["access_token"] = None
    st.session_state["refresh_token"] = None


def get_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    client: Client = create_client(url, key)

    access_token = st.session_state.get("access_token")
    refresh_token = st.session_state.get("refresh_token")

    if access_token and refresh_token:
        try:
            client.auth.set_session(access_token, refresh_token)
        except Exception:
            clear_session()

    return client


def login_user(email, password):
    client = get_supabase()
    try:
        response = client.auth.sign_in_with_password({
            "email": email.strip(),
            "password": password
        })

        if response and response.user and response.session:
            st.session_state["authenticated"] = True
            st.session_state["user_email"] = response.user.email
            st.session_state["page"] = "dashboard"
            st.session_state["access_token"] = response.session.access_token
            st.session_state["refresh_token"] = response.session.refresh_token
            return True

        return False

    except Exception as e:
        st.error(f"Error de login: {e}")
        return False


def logout():
    clear_session()
    st.rerun()