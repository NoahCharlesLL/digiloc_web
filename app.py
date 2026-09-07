import streamlit as st
from utils.data import load_locations, load_drawings
from utils.theme import inject_css, close_frame
from pages_app import splash, map_view, detail, about, topbar, login

st.set_page_config(page_title="Digital Locations", layout="wide")
inject_css()

locations = load_locations()
area_drawings = load_drawings()

if "page" not in st.session_state:
    st.session_state.page = "splash"

if st.session_state.page == "splash":
    splash.render()
else:
    is_detail = st.session_state.page == "detail"
    tab_options = ["Info", "Navigation", "Stage", "Booking"] if is_detail else None
    topbar.render(show_back=(st.session_state.page != "map"), tab_options=tab_options)

    if st.session_state.page == "map":
        map_view.render(locations)
    elif st.session_state.page == "detail":
        loc = next(l for l in locations if l["id"] == st.session_state.selected_location)
        st.session_state.back_target = "map"
        detail.render(loc, area_drawings)
    elif st.session_state.page == "about":
        about.render()
    elif st.session_state.page == "login":
        login.render()

close_frame()