import streamlit as st
import json
from utils.data import DATA_DIR

USERS_FILE = DATA_DIR / "users.json"

def _load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}

def render():
    st.markdown("### Log In")

    if st.session_state.get("logged_in"):
        st.success(f"Logged in as **{st.session_state.get('username', 'User')}**")
        if st.button("Log out"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
        return

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log In", type="primary"):
        users = _load_users()
        user = users.get(email)
        if user and user["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = f"{user['first_name']} {user['last_name']}"
            st.success("Logged in!")
            st.rerun()
        else:
            st.error("Invalid email or password.")

    if st.button("Register"):
        st.session_state.page = "register"
        st.rerun()