import streamlit as st

def render(loc):
    st.write("Unreal Engine launcher — coming soon.")
    st.write(f"Project file: {loc.get('unreal_project', 'N/A')}")