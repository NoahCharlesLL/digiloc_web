import streamlit as st
import json
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval
from utils.data import save_drawings
from pathlib import Path

PRESET_COLORS = [
    "#980000", "#FF0000", "#FF9900", "#FFFF00", "#00FF00", "#FFFFFF",
    "#FF00FF", "#9900FF", "#0000FF", "#4A86E8", "#00FFFF", "#000000",
    "#d9a441", "#8d9f44", "#4b905b", "#0e7a6d", "#14616d", "#2f4858"
]

MARKER_TYPES = [
    ("toilet", "🚻"), ("wifi", "📶"), ("power", "🔌"),
    ("parking", "🅿️"), ("food", "🍴"), ("custom", "📍"),
]

HTML_PATH = Path(__file__).parent / "navigation.html"


def render(loc, area_drawings):
    st.markdown("**Draw areas/markers on the map. Configure name/color, click Confirm, then click Save.**")

    saved = area_drawings.get(loc["id"], [])
    loc_id = str(loc["id"])

    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("__LAT__", str(loc["lat"]))
    html = html.replace("__LNG__", str(loc["lng"]))
    html = html.replace("__PRESETS__", json.dumps(PRESET_COLORS))
    html = html.replace("__MARKER_TYPES__", json.dumps(MARKER_TYPES))
    html = html.replace("__SAVED_SHAPES__", json.dumps(saved))
    html = html.replace("__LOC_ID__", loc_id)

    components.html(html, height=650, scrolling=False)

    stored = streamlit_js_eval(
        js_expressions=f"localStorage.getItem('nav_shapes_{loc_id}')",
        key=f"read_shapes_{loc_id}"
    )
    if stored:
        try:
            shapes = json.loads(stored)
            if shapes != saved:
                area_drawings[loc["id"]] = shapes
                save_drawings(area_drawings)
                streamlit_js_eval(
                    js_expressions=f"localStorage.removeItem('nav_shapes_{loc_id}')",
                    key=f"clear_shapes_{loc_id}"
                )
                st.success(f"Saved {len(shapes)} shape(s)!")
                st.rerun()
        except Exception as e:
            st.error(f"Couldn't parse JSON: {e}")