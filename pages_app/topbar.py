import streamlit as st
from utils.theme import title

def render(show_back=False, tab_options=None):
    c1, c2, c3 = st.columns([5, 1, 2], vertical_alignment="bottom")
    with c1:
        # Logo first, title second, and spacer column (_) absorbing empty space to the right
        logo_col, title_col, _ = st.columns([0.3, 3.8, 1.6], vertical_alignment="bottom")
        with logo_col:
            st.image("C:/Users/noah_hainer/Desktop/SVG/Asset 2.svg", width=52)
        with title_col:
            title("DIGITAL LOCATIONS", 52)
    with c3:
        a1, a2 = st.columns(2)
        with a1:
            if a1.button("About", key="topbar_about", use_container_width=True):
                st.session_state.page = "about"
                st.rerun()
        with a2:
            if a2.button("👤 Log In", key="topbar_login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()

    if show_back:
        if tab_options:
            if "detail_tab" not in st.session_state or st.session_state.detail_tab not in tab_options:
                st.session_state.detail_tab = tab_options[0]

            back_col, tab_col = st.columns([1, 6])
            with back_col:
                if st.button("←", key="topbar_back"):
                    st.session_state.page = st.session_state.get("back_target", "map")
                    st.rerun()

            with tab_col:
                with st.container(key="dl_tabbar"):
                    tab_cols = st.columns(len(tab_options), gap=0)
                    for name, col in zip(tab_options, tab_cols):
                        active = st.session_state.detail_tab == name
                        if col.button(name, key=f"tab_{name}", type="primary" if active else "secondary",
                                      use_container_width=True):
                            st.session_state.detail_tab = name
                            st.rerun()
        else:
            if st.button("←", key="topbar_back"):
                st.session_state.page = st.session_state.get("back_target", "map")
                st.rerun()

    st.markdown("<div class='dl-divider'></div>", unsafe_allow_html=True)