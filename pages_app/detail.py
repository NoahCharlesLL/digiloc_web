import streamlit as st
from pages_app.location_tabs import info_tab, navigation_tab, stage_tab, booking_tab

def render(loc, area_drawings):
    st.subheader(loc["name"].upper() , text_alignment = "center")

    active = st.session_state.get("detail_tab", "Info")

    if active == "Info":
        info_tab.render(loc)
    elif active == "Navigation":
        navigation_tab.render(loc, area_drawings)
    elif active == "Stage":
        stage_tab.render(loc)
    elif active == "Booking":
        booking_tab.render(loc)