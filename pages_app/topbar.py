import streamlit as st
from utils.theme import COLORS

def render(show_back=False):
    c1, c2, c3 = st.columns([3, 4, 2])
    with c1:
        st.markdown(f"<div class='digiloc-title' style='font-size:26px;'>DIGITAL LOCATIONS</div>", unsafe_allow_html=True)
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

    st.markdown("---")