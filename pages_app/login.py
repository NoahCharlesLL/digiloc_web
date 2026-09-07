import streamlit as st

def render():
    st.markdown("### Log In")

    if st.session_state.get("logged_in"):
        st.success(f"Logged in as **{st.session_state.get('username', 'User')}**")
        if st.button("Log out"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
        return

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log In", type="primary"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in!")
            st.rerun()
        else:
            st.warning("Enter a username and password (any values work for now — this is a placeholder).")