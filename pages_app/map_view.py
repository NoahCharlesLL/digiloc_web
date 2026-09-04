import streamlit as st
import folium
from streamlit_folium import st_folium

def render(locations):
    st.header("DIGITAL LOCATIONS")
    m = folium.Map(location=[51.43, 7.26], zoom_start=8, tiles="OpenStreetMap")

    for loc in locations:
        folium.CircleMarker(
            [loc["lat"], loc["lng"]], radius=10, tooltip=loc["name"],
            color="#C9A84C", fill=True, fill_color="#C9A84C", fill_opacity=1
        ).add_to(m)

    map_data = st_folium(
        m, width=1200, height=600, key="overview_map",
        returned_objects=["last_object_clicked_tooltip"]
    )

    if map_data.get("last_object_clicked_tooltip"):
        clicked = next(l for l in locations if l["name"] == map_data["last_object_clicked_tooltip"])
        st.session_state.selected_location = clicked["id"]
        st.session_state.page = "detail"
        st.rerun()