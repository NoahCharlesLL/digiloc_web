import streamlit as st
from utils.theme import title

def render(show_back=False):
    c1, c2, c3 = st.columns([3, 4, 2])
    with c1:
        title("DIGITAL LOCATIONS")
    with c3:
        b1, b2 = st.columns(2)
        if b1.button("About"):
            st.session_state.page = "about"
            st.rerun()
        if b2.button("👤 Log In"):
            st.session_state.page = "login"
            st.rerun()

    if show_back:
        if st.button("← Back"):
            st.session_state.page = st.session_state.get("back_target", "map")
            st.rerun()

    st.markdown("<div class='dl-divider'></div>", unsafe_allow_html=True)