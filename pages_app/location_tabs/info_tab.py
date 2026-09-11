import streamlit as st
import base64
from io import BytesIO
from PIL import Image, ImageOps
from utils.data import DATA_DIR

@st.cache_data(show_spinner=False)
def _load_preview_b64(path_str, mtime, max_dim=1400):
    pil_img = Image.open(path_str)
    pil_img = ImageOps.exif_transpose(pil_img)
    pil_img.thumbnail((max_dim, max_dim))
    buf = BytesIO()
    pil_img.save(buf, format="JPEG", quality=80)
    return base64.b64encode(buf.getvalue()).decode()

@st.cache_data(show_spinner=False)
def _load_full_b64(path_str, mtime, max_dim=2400):
    pil_img = Image.open(path_str)
    pil_img = ImageOps.exif_transpose(pil_img)
    pil_img.thumbnail((max_dim, max_dim))
    buf = BytesIO()
    pil_img.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode()

@st.dialog("Full size", width="large")
def _show_fullscreen(path_str, mtime):
    b64 = _load_full_b64(path_str, mtime)
    st.markdown(
        f"<img src='data:image/jpeg;base64,{b64}' style='width:100%; height:auto;' />",
        unsafe_allow_html=True,
    )

def render(loc):
    img_dir = DATA_DIR / "images" / loc["id"]
    images = []
    if img_dir.exists():
        images = sorted(
            p for p in img_dir.iterdir()
            if p.suffix.lower() in [".jpg", ".jpeg", ".png"]
        )

    idx_key = f"carousel_idx_{loc['id']}"
    st.session_state.setdefault(idx_key, 0)

    if images:
        st.session_state[idx_key] %= len(images)
        current = images[st.session_state[idx_key]]
        mtime = current.stat().st_mtime

        b64 = _load_preview_b64(str(current), mtime)
        wrap_key = f"imgwrap_{loc['id']}"

        st.markdown(
            f"""
            <style>
            .st-key-{wrap_key} {{ position: relative; text-align: center; }}
            .st-key-{wrap_key} img {{
                max-height: 55vh; width: auto; max-width: 100%;
                object-fit: contain; display: inline-block;
            }}
            .st-key-{wrap_key} div[data-testid="stElementContainer"]:has(.stButton) {{
                position: absolute !important; inset: 0 !important; width: 100% !important; height: 100% !important;
            }}
            .st-key-{wrap_key} .stButton {{ width: 100% !important; height: 100% !important; }}
            .st-key-{wrap_key} .stButton > button {{
                width: 100% !important; height: 100% !important;
                opacity: 0; cursor: pointer; border: none; background: transparent; padding: 0;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

        nav1, nav2, nav3 = st.columns([1, 6, 1])
        with nav1:
            if st.button("◀", key=f"prev_{loc['id']}"):
                st.session_state[idx_key] = (st.session_state[idx_key] - 1) % len(images)
                st.rerun()
        with nav2:
            with st.container(key=wrap_key):
                st.markdown(
                    f"""
                    <div style="display:flex; justify-content:center; width:100%;">
                        <img src="data:image/jpeg;base64,{b64}"
                             style="max-height:55vh; width:auto; max-width:100%; object-fit:contain; display:block;" />
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("", key=f"fullsize_{loc['id']}"):
                    _show_fullscreen(str(current), mtime)
            st.caption(f"{st.session_state[idx_key] + 1} / {len(images)}")
        with nav3:
            if st.button("▶", key=f"next_{loc['id']}"):
                st.session_state[idx_key] = (st.session_state[idx_key] + 1) % len(images)
                st.rerun()
    else:
        st.write("No images found.")

    st.markdown("<div class='dl-divider'></div>", unsafe_allow_html=True)

    st.markdown(f"**Address**\n\n{loc['address']}")
    st.markdown(f"**Phone**\n\n{loc['phone']}")
    st.markdown(f"**About**\n\n{loc['about']}")
    st.markdown(f"**General**\n\n{loc['general']}")