import streamlit as st
from pages_app.location_tabs import info_tab, navigation_tab, stage_tab, booking_tab

def render(loc, area_drawings):
    st.subheader(loc["name"].upper())

    tab_info, tab_nav, tab_stage, tab_booking = st.tabs(["Info", "Navigation", "Stage", "Booking"])

    with tab_info:
        info_tab.render(loc)
    with tab_nav:
        navigation_tab.render(loc, area_drawings)
    with tab_stage:
        stage_tab.render(loc)
    with tab_booking:
        booking_tab.render(loc)