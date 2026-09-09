import streamlit as st
from utils.data import load_locations, load_drawings
from utils.theme import inject_css, close_frame
from pages_app import splash, map_view, detail, about, topbar, login, register

st.set_page_config(page_title="Digital Locations", layout="wide")
inject_css()

locations = load_locations()
area_drawings = load_drawings()

if "page" not in st.session_state:
    st.session_state.page = st.query_params.get("page", "splash")
if "selected_location" not in st.session_state and "loc" in st.query_params:
    st.session_state.selected_location = st.query_params["loc"]
if "detail_tab" not in st.session_state and "tab" in st.query_params:
    st.session_state.detail_tab = st.query_params["tab"]

st.query_params["page"] = st.session_state.page
if st.session_state.get("selected_location"):
    st.query_params["loc"] = str(st.session_state.selected_location)
if st.session_state.get("detail_tab"):
    st.query_params["tab"] = st.session_state.detail_tab

if st.session_state.page == "splash":
    splash.render()
else:
    is_detail = st.session_state.page == "detail"
    tab_options = ["Info", "Navigation", "Stage", "Booking"] if is_detail else None
    topbar.render(show_back=(st.session_state.page != "map"), tab_options=tab_options)

    if st.session_state.page == "map":
        map_view.render(locations)
    elif st.session_state.page == "detail":
        loc = next(l for l in locations if str(l["id"]) == str(st.session_state.selected_location))
        st.session_state.back_target = "map"
        detail.render(loc, area_drawings)
    elif st.session_state.page == "about":
        about.render()
    elif st.session_state.page == "login":
        login.render()
    elif st.session_state.page == "register":
        register.render()

close_frame()