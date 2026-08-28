import streamlit as st
import json
from pathlib import Path
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium

st.set_page_config(page_title="Digital Locations", layout="wide")

DATA_DIR = Path(__file__).parent / "data"
POI_COLORS = {"toilet": "#4FA8E0", "wifi": "#5BC27A", "power": "#E05B5B"}

with open(DATA_DIR / "locations.json", encoding="utf-8") as f:
    locations = json.load(f)

DRAWINGS_FILE = DATA_DIR / "area_drawings.json"
if DRAWINGS_FILE.exists():
    with open(DRAWINGS_FILE, encoding="utf-8") as f:
        area_drawings = json.load(f)
else:
    area_drawings = {}

st.markdown("""
    <style>
    .stApp { background-color: #1c1c1c; color: #E0E0E0; }
    h1, h2, h3 { color: #C9A84C; }
    </style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "splash"
if "selected_location" not in st.session_state:
    st.session_state.selected_location = None

def go_to(page):
    st.session_state.page = page

# ---------------- SPLASH ----------------
if st.session_state.page == "splash":
    st.title("DIGITAL LOCATIONS")
    if st.button("Find a location!"):
        go_to("map")
        st.rerun()

# ---------------- MAP ----------------
elif st.session_state.page == "map":
    st.header("DIGITAL LOCATIONS")

    m = folium.Map(location=[51.43, 7.26], zoom_start=8, tiles="OpenStreetMap")

    for loc in locations:
        folium.CircleMarker(
            [loc["lat"], loc["lng"]],
            radius=10,
            tooltip=loc["name"],
            color="#C9A84C",
            fill=True,
            fill_color="#C9A84C",
            fill_opacity=1
        ).add_to(m)

    map_data = st_folium(m, width=1200, height=600, key="overview_map")

    if map_data.get("last_object_clicked_tooltip"):
        clicked = next(l for l in locations if l["name"] == map_data["last_object_clicked_tooltip"])
        st.session_state.selected_location = clicked["id"]
        go_to("detail")
        st.rerun()

# ---------------- DETAIL ----------------
elif st.session_state.page == "detail":
    loc = next(l for l in locations if l["id"] == st.session_state.selected_location)

    top_col1, top_col2 = st.columns([1, 5])
    with top_col1:
        if st.button("← Back"):
            go_to("map")
            st.rerun()
    with top_col2:
        st.subheader(loc["name"].upper())

    tab_info, tab_nav, tab_stage, tab_booking = st.tabs(["Info", "Navigation", "Stage", "Booking"])

    # ---- INFO TAB ----
    with tab_info:
        col1, col2 = st.columns([2, 3])
        with col1:
            img_dir = DATA_DIR / "images" / loc["id"]
            if img_dir.exists():
                imgs = [p for p in img_dir.iterdir() if p.suffix.lower() in [".jpg", ".jpeg", ".png"]]
                for img in imgs:
                    st.image(str(img), use_container_width=True)
            else:
                st.write("No images found.")
        with col2:
            st.markdown(f"**Address**\n\n{loc['address']}")
            st.markdown(f"**Phone**\n\n{loc['phone']}")
            st.markdown(f"**About**\n\n{loc['about']}")
            st.markdown(f"**General**\n\n{loc['general']}")

    # ---- NAVIGATION TAB ----
    with tab_nav:
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
                shape_name = st.text_input("New shape name", key="shape_name_input")
                shape_color = st.color_picker("New shape color", "#C9A84C", key="shape_color_input")

        with col2:
            nav_map = folium.Map(location=[loc["lat"], loc["lng"]], zoom_start=16, tiles="OpenStreetMap")

            folium.CircleMarker(
                [loc["lat"], loc["lng"]],
                radius=10, color="#C9A84C", fill=True, fill_color="#C9A84C", fill_opacity=1,
                tooltip=loc["name"]
            ).add_to(nav_map)

            for poi in loc.get("pois", []):
                folium.CircleMarker(
                    [poi["lat"], poi["lng"]],
                    radius=6, color=POI_COLORS.get(poi["type"], "#888"),
                    fill=True, fill_opacity=1, tooltip=poi["label"]
                ).add_to(nav_map)

            for area in loc.get("restricted_areas", []):
                folium.Polygon(
                    locations=area["points"],
                    color="red", fill=True, fill_opacity=0.3,
                    tooltip=area["label"]
                ).add_to(nav_map)

            # Draw previously saved shapes with their own name/color
            for shape in area_drawings.get(loc["id"], []):
                if "type" not in shape:
                    continue
                props = shape.get("properties", {})
                folium.GeoJson(
                    shape,
                    tooltip=props.get("name", ""),
                    style_function=lambda x, c=props.get("color", "#C9A84C"): {"color": c, "fillColor": c, "fillOpacity": 0.3}
                ).add_to(nav_map)

            if edit_mode:
                Draw(export=False).add_to(nav_map)

            nav_map_data = st_folium(nav_map, width=900, height=550, key="nav_map")

            if edit_mode and nav_map_data.get("all_drawings"):
                if st.button("💾 Save new shape"):
                    new_shape = nav_map_data["all_drawings"][-1]  # latest drawn
                    new_shape["properties"] = {
                        "name": st.session_state.shape_name_input or "Unnamed",
                        "color": st.session_state.shape_color_input
                    }
                    existing = area_drawings.get(loc["id"], [])
                    existing.append(new_shape)
                    area_drawings[loc["id"]] = existing
                    with open(DRAWINGS_FILE, "w", encoding="utf-8") as f:
                        json.dump(area_drawings, f, indent=2)
                    st.success(f"Saved '{new_shape['properties']['name']}'!")
                    st.rerun()

    # ---- STAGE TAB ----
    with tab_stage:
        st.write("Unreal Engine launcher — coming soon.")
        st.write(f"Project file: {loc.get('unreal_project', 'N/A')}")

    # ---- BOOKING TAB ----
    with tab_booking:
        st.write("Booking calendar & contact form — coming soon.")
        st.markdown(f"**Contact:** {loc['contact']}")