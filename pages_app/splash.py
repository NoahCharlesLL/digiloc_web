import streamlit as st

def render():
    st.title("DIGITAL LOCATIONS")
    if st.button("Find a location!"):
        st.session_state.page = "map"
        st.rerun()