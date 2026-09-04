import streamlit as st
import folium
import datetime
from utils.data import DATA_DIR
import json
from folium.plugins import Draw
from streamlit_folium import st_folium
from utils.data import DATA_DIR, POI_ICONS, save_drawings

BOOKINGS_FILE = DATA_DIR / "bookings.json"

def _load_bookings():
    if BOOKINGS_FILE.exists():
        with open(BOOKINGS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}

def _save_bookings(bookings):
    with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(bookings, f, indent=2)


def _render_booking(loc):
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("**Select dates**")
        today = datetime.date.today()
        date_options = [today + datetime.timedelta(days=i) for i in range(60)]
        date_labels = [d.strftime("%a, %d %b %Y") for d in date_options]

        selected_labels = st.multiselect("Available dates (next 60 days)", date_labels, key="booking_dates")

    with col2:
        st.markdown("**Your details**")
        full_name = st.text_input("Full name", key="booking_name")
        email = st.text_input("E-mail", key="booking_email")
        message = st.text_area("Message", key="booking_message", height=150)

        if st.button("Confirm booking", type="primary"):
            if not selected_labels or not full_name or not email:
                st.warning("Pick at least one date and fill in name + email.")
            else:
                bookings = _load_bookings()
                entry = {
                    "name": full_name, "email": email, "message": message,
                    "dates": selected_labels,
                }
                bookings.setdefault(loc["id"], []).append(entry)
                _save_bookings(bookings)
                st.success(f"Booking request sent for {len(selected_labels)} date(s)!")


def render(loc, area_drawings):
    st.subheader(loc["name"].upper())

    tab_info, tab_nav, tab_stage, tab_booking = st.tabs(["Info", "Navigation", "Stage", "Booking"])

    with tab_info:
        _render_info(loc)
    with tab_nav:
        _render_nav(loc, area_drawings)
    with tab_stage:
        st.write("Unreal Engine launcher — coming soon.")
        st.write(f"Project file: {loc.get('unreal_project', 'N/A')}")
    with tab_booking:
        _render_booking(loc)


def _render_info(loc):
    col1, col2 = st.columns([2, 3])
    with col1:
        img_dir = DATA_DIR / "images" / loc["id"]
        if img_dir.exists():
            for img in img_dir.iterdir():
                if img.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                    st.image(str(img), use_container_width=True)
        else:
            st.write("No images found.")
    with col2:
        st.markdown(f"**Address**\n\n{loc['address']}")
        st.markdown(f"**Phone**\n\n{loc['phone']}")
        st.markdown(f"**About**\n\n{loc['about']}")
        st.markdown(f"**General**\n\n{loc['general']}")


def _render_nav(loc, area_drawings):
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
        nav_map_data = st_folium(
            nav_map, width=900, height=550, key="nav_map",
            returned_objects=return_objs
        )

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