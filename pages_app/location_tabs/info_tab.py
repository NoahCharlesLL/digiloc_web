import streamlit as st
from utils.data import DATA_DIR

def render(loc):
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
        st.markdown("<div class='dl-vline'>", unsafe_allow_html=True)
        st.markdown(f"**Address**\n\n{loc['address']}")
        st.markdown(f"**Phone**\n\n{loc['phone']}")
        st.markdown(f"**About**\n\n{loc['about']}")
        st.markdown(f"**General**\n\n{loc['general']}")