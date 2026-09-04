import streamlit as st
from utils.data import load_locations, load_drawings
from pages_app import splash, map_view, detail

st.set_page_config(page_title="Digital Locations", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1c1c1c; color: #E0E0E0; }
    h1, h2, h3 { color: #C9A84C; }
    </style>
""", unsafe_allow_html=True)

locations = load_locations()
area_drawings = load_drawings()

if "page" not in st.session_state:
    st.session_state.page = "splash"

if st.session_state.page == "splash":
    splash.render()
elif st.session_state.page == "map":
    map_view.render(locations)
elif st.session_state.page == "detail":
    loc = next(l for l in locations if l["id"] == st.session_state.selected_location)
    detail.render(loc, area_drawings)