import streamlit as st

COLORS = {
    "bg": "#1A1A1A",
    "bg_panel": "#212121",
    "border": "#5A5A5A",
    "accent": "#D9A441",
    "accent_soft": "#F2E9D8",
    "text": "#F2F2F2",
    "text_muted": "#8C8C8C",
}

FONT_BODY = "'Segoe UI', sans-serif"
FONT_TITLE = "'Consolas', monospace"


def inject_css():
    c = COLORS
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {c['bg']};
            color: {c['text']};
            font-family: {FONT_BODY};
        }}
        header[data-testid="stHeader"] {{ background: transparent; }}
        #MainMenu, footer {{ visibility: hidden; }}
        .block-container {{ padding-top: 1.5rem; max-width: 1300px; }}

        .dl-label {{
            font-size: 11px; letter-spacing: 2px; text-transform: uppercase;
            color: {c['text_muted']}; font-family: {FONT_TITLE};
        }}
        .dl-title {{
            font-family: {FONT_TITLE}; color: {c['accent']};
            letter-spacing: 3px; font-weight: 700;
        }}

        h1, h2, h3 {{ color: {c['text']}; font-weight: 600; }}

        hr, .dl-divider {{ border: none; border-top: 2px solid {c['border']}; margin: 1rem 0; }}

        /* buttons: strong box, visible border */
        .stButton > button {{
            background-color: {c['bg_panel']};
            color: {c['text']};
            border: 2px solid {c['border']};
            border-radius: 0px;
            font-family: {FONT_BODY};
            font-size: 13px;
            padding: 0.5rem 1.1rem;
            transition: border-color 0.15s, color 0.15s;
        }}
        .stButton > button:hover {{
            border-color: {c['accent']};
            color: {c['accent']};
        }}
        .stButton > button[kind="primary"] {{
            background-color: {c['accent']};
            color: {c['bg']};
            border-color: {c['accent']};
            font-weight: 700;
        }}

        .stTextInput input, .stTextArea textarea, .stMultiSelect > div {{
            background-color: {c['bg_panel']} !important;
            color: {c['text']} !important;
            border: 2px solid {c['border']} !important;
            border-radius: 0px !important;
        }}

        /* every panel/container = visible box */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border: 2px solid {c['border']} !important;
            border-radius: 0px !important;
            background-color: {c['bg_panel']};
        }}

        .stTabs [data-baseweb="tab-list"] {{ gap: 0; border-bottom: 2px solid {c['border']}; }}
        .stTabs [data-baseweb="tab"] {{
            background: {c['bg_panel']}; color: {c['text_muted']};
            font-family: {FONT_TITLE}; font-size: 12px; letter-spacing: 1px;
            border: 2px solid {c['border']}; border-bottom: none;
        }}
        .stTabs [aria-selected="true"] {{
            color: {c['accent']} !important;
            border-color: {c['accent']} !important;
        }}
        </style>
    """, unsafe_allow_html=True)


def title(text, size=26):
    st.markdown(f"<div class='dl-title' style='font-size:{size}px;'>{text}</div>", unsafe_allow_html=True)

def label(text):
    st.markdown(f"<div class='dl-label'>{text}</div>", unsafe_allow_html=True)

def divider():
    st.markdown("<div class='dl-divider'></div>", unsafe_allow_html=True)