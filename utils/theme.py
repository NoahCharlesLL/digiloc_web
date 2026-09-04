COLORS = {
    "bg": "#2E2E2E",
    "bg_soft": "#E7E7E7",
    "accent": "#D9A441",
    "accent_soft": "#F2E9D8",
    "text": "#FFFFFF",
    "text_dark": "#1A1A1A",
}

FONT_BODY = "'Segoe UI', sans-serif"
FONT_TITLE = "'Consolas', monospace"

def inject_css():
    import streamlit as st
    c = COLORS
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {c['bg']}; color: {c['text']}; font-family: {FONT_BODY}; }}
        h1, h2, h3 {{ color: {c['accent']}; }}
        .digiloc-title {{ font-family: {FONT_TITLE}; color: {c['accent']}; letter-spacing: 4px; }}
        </style>
    """, unsafe_allow_html=True)