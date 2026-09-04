import streamlit as st
import folium
from streamlit_folium import st_folium

FILTER_OPTIONS = [
    ("Indoor", "indoor"), ("Outdoor", "outdoor"),
    ("Has Toilets", "toilet"), ("Has WiFi", "wifi"), ("Has Power", "power"),
]

def _apply_filters(locations, search_text, active_filters):
    result = []
    for loc in locations:
        if search_text:
            if search_text not in loc["name"].lower() and search_text not in loc.get("city", "").lower():
                continue
        if active_filters:
            setting = loc.get("setting", "")
            amenities = loc.get("amenities", [])
            match = True
            for f in active_filters:
                if f in ("indoor", "outdoor"):
                    if setting != f:
                        match = False
                        break
                elif f not in amenities:
                    match = False
                    break
            if not match:
                continue
        result.append(loc)
    return result


def render(locations):
    st.header("DIGITAL LOCATIONS")

    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "map"
    if "active_filters" not in st.session_state:
        st.session_state.active_filters = set()

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🗺 Map View", type="primary" if st.session_state.view_mode == "map" else "secondary"):
            st.session_state.view_mode = "map"
            st.rerun()
    with col2:
        if st.button("☰ List View", type="primary" if st.session_state.view_mode == "list" else "secondary"):
            st.session_state.view_mode = "list"
            st.rerun()

    search_text = st.text_input("🔍 Search", "").strip().lower()

    with st.expander("⚡ Filter Locations"):
        cols = st.columns(len(FILTER_OPTIONS))
        for (label, key), c in zip(FILTER_OPTIONS, cols):
            active = key in st.session_state.active_filters
            if c.button(label, type="primary" if active else "secondary", key=f"filter_{key}"):
                if active:
                    st.session_state.active_filters.discard(key)
                else:
                    st.session_state.active_filters.add(key)
                st.rerun()

    filtered = _apply_filters(locations, search_text, st.session_state.active_filters)
    st.caption(f"{len(filtered)} / {len(locations)} locations")

    if st.session_state.view_mode == "map":
        _render_map(filtered)
    else:
        _render_list(filtered)


def _render_map(locations):
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
        clicked = next((l for l in locations if l["name"] == map_data["last_object_clicked_tooltip"]), None)
        if clicked:
            st.session_state.selected_location = clicked["id"]
            st.session_state.page = "detail"
            st.rerun()


def _render_list(locations):
    for loc in locations:
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([1, 4, 1, 1])
            with c1:
                st.markdown("🖼")
            with c2:
                st.markdown(f"**{loc['name'].upper()}**")
                st.caption(loc["address"])
            with c3:
                if st.button("Show on Map", key=f"map_{loc['id']}"):
                    st.session_state.view_mode = "map"
                    st.rerun()
            with c4:
                if st.button("More Info", key=f"info_{loc['id']}"):
                    st.session_state.selected_location = loc["id"]
                    st.session_state.page = "detail"
                    st.rerun()