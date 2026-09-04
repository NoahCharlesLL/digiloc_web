import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
from utils.data import POI_ICONS, save_drawings

def render(loc, area_drawings):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"**Address**\n\n{loc['address']}")
        st.markdown(f"**Phone**\n\n{loc['phone']}")
        st.markdown(f"**Navigation**\n\n{loc['navigation']}")
        st.markdown("**Nearby**")
        for poi in loc.get("pois", []):
            st.write(f"- {poi['label']} ({poi['type']})")

        st.markdown("---")
        edit_mode = st.toggle("✏ Edit Areas", key="edit_mode")
        if edit_mode:
            st.text_input("New shape name", key="shape_name_input")
            st.color_picker("New shape color", "#C9A84C", key="shape_color_input")

    with col2:
        st.markdown("<div class='dl-vline'>", unsafe_allow_html=True)
        nav_map = folium.Map(location=[loc["lat"], loc["lng"]], zoom_start=16, tiles="OpenStreetMap")

        folium.CircleMarker(
            [loc["lat"], loc["lng"]], radius=10, color="#C9A84C",
            fill=True, fill_color="#C9A84C", fill_opacity=1, tooltip=loc["name"]
        ).add_to(nav_map)

        for poi in loc.get("pois", []):
            icon_name, color = POI_ICONS.get(poi["type"], ("map-marker", "#888"))
            folium.Marker(
                [poi["lat"], poi["lng"]], tooltip=poi["label"],
                icon=folium.Icon(color="white", icon_color=color, icon=icon_name, prefix="fa")
            ).add_to(nav_map)

        for area in loc.get("restricted_areas", []):
            folium.Polygon(
                locations=area["points"], color="red",
                fill=True, fill_opacity=0.3, tooltip=area["label"]
            ).add_to(nav_map)

        fg = folium.FeatureGroup(name="drawings")
        for shape in area_drawings.get(loc["id"], []):
            if "type" not in shape:
                continue
            props = shape.get("properties", {})
            name = props.get("name", "Unnamed")
            color = props.get("color", "#C9A84C")
            folium.GeoJson(
                shape,
                style_function=lambda x, c=color: {"color": c, "fillColor": c, "fillOpacity": 0.3},
                tooltip=name
            ).add_to(fg)
        fg.add_to(nav_map)

        if edit_mode:
            Draw(export=False, draw_options={"circlemarker": False}).add_to(nav_map)

        return_objs = ["all_drawings"] if edit_mode else []
        nav_map_data = st_folium(nav_map, width=900, height=550, key="nav_map", returned_objects=return_objs)

        if edit_mode and nav_map_data.get("all_drawings"):
            if st.button("💾 Save new shape"):
                new_shape = nav_map_data["all_drawings"][-1]
                new_shape["properties"] = {
                    "name": st.session_state.shape_name_input or "Unnamed",
                    "color": st.session_state.shape_color_input
                }
                existing = area_drawings.get(loc["id"], [])
                existing.append(new_shape)
                area_drawings[loc["id"]] = existing
                save_drawings(area_drawings)
                st.success(f"Saved '{new_shape['properties']['name']}'!")
                st.rerun()