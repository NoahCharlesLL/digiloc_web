import streamlit as st
import json
from utils.data import DATA_DIR

USERS_FILE = DATA_DIR / "users.json"

def _load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}

def _save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

def render():
    st.markdown("### Register")

    first_name = st.text_input("First name", key="reg_first")
    last_name = st.text_input("Last name", key="reg_last")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_pw1")
    password2 = st.text_input("Repeat password", type="password", key="reg_pw2")

    if st.button("Create account", type="primary"):
        if not all([first_name, last_name, email, password, password2]):
            st.warning("Fill in all fields.")
        elif password != password2:
            st.error("Passwords do not match.")
        else:
            users = _load_users()
            if email in users:
                st.error("Email already registered.")
            else:
                users[email] = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "password": password,
                }
                _save_users(users)
                st.success("Account created! You can log in now.")
                st.session_state.page = "login"
                st.rerun()

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()