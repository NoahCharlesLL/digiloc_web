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

#TODO
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
        #COMMENT IN IF YOU WANT TO REMOVE THE STREAMLIT HEADER
        # [data-testid="stToolbar"] {{ display: none !important; }}
        # [data-testid="stAppDeployButton"] {{ display: none !important; }}
        #MainMenu, footer {{ visibility: hidden; }}

        .block-container {{
            border-left: 3px solid {c['border']};
            border-right: 3px solid {c['border']};
            padding-left: 1.5rem;
            padding-right: 1.5rem;
            # For having it normal do this for the next line: padding-top: 0;
            padding-top: 3.5rem !important;
            padding-bottom: 2rem;
            max-width: 1800px;
        }}

        .dl-label {{
            font-size: 11px; letter-spacing: 2px; text-transform: uppercase;
            color: {c['text_muted']}; font-family: {FONT_TITLE};
        }}
        .dl-title {{
            font-family: {FONT_TITLE}; color: {c['accent']};
            letter-spacing: 3px; font-weight: 700;
        }}

        h1, h2, h3 {{ color: {c['text']}; font-weight: 600; }}

        .dl-divider {{
            border: none; border-top: 3px solid {c['border']};
            margin: 0.8rem -1.5rem;
        }}

        .dl-vline {{
            border-left: 3px solid {c['border']};
            padding-left: 1.5rem;
            margin-left: -1.5rem;
        }}

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
        }}

        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border: 2px solid {c['border']} !important;
            background-color: {c['bg_panel']};
        }}

        /* tabs: one full-width underline, active tab just colored */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 1.5rem;
            width: calc(100% + 3rem) !important;
            margin-left: -1.5rem;
            padding-left: 1.5rem;
            border-bottom: 3px solid {c['border']} !important;
        }}
        .stTabs [data-baseweb="tab"] {{
            background: transparent !important;
            color: {c['text_muted']};
            font-family: {FONT_TITLE}; font-size: 13px; letter-spacing: 1px;
            border: none !important;
            padding-bottom: 10px;
        }}
        .stTabs [aria-selected="true"] {{
            color: {c['accent']} !important;
        }}
        .stTabs [data-baseweb="tab-highlight"],
        .stTabs [data-baseweb="tab-border"] {{
            display: none !important;
            height: 0 !important;
            background: transparent !important;
        }}
        
        /* segmented control: connected tab buttons */
        .st-key-dl_tabbar .stButton > button {{
            border-radius: 0px !important;
            white-space: nowrap;
            font-size: 13px;
            padding: 0.5rem 0.5rem;
        }}
        .st-key-dl_tabbar [data-testid="stColumn"]:not(:first-child) .stButton > button {{
            border-left: none !important;
        }}

        /* force ALL corners square, no exceptions */
        .stTextInput input, .stTextArea textarea,
        .stMultiSelect > div, .stSelectbox > div,
        .stButton > button, div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 0px !important;
        }}

        [data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="base-input"] {{
            border-radius: 0px !important;
        }}
        [data-baseweb="input"] > div, [data-baseweb="textarea"] > div {{
            border-radius: 0px !important;
        }}
        div[data-testid="stTextInput"] div,
        div[data-testid="stTextArea"] div {{
            border-radius: 0px !important;
        }}
        div[data-testid="stTextInput"] input {{
            border-radius: 0px !important;
        }}

        /* vanilla calendar: st.container(key=) actually nests, so this works */
        .st-key-dl_calendar {{
            border: 2px solid {c['border']};
        }}
        .st-key-dl_calendar .stButton > button {{
            border: none !important;
            outline: none !important;
            background: transparent !important;
            box-shadow: none !important;
            border-radius: 0px !important;
            width: 100%;
            height: 40px;
            font-size: 13px;
            padding: 0;
            border-right: 1px solid rgba(255,255,255,0.08) !important;
            border-bottom: 1px solid rgba(255,255,255,0.08) !important;
        }}
        .st-key-dl_calendar .stButton > button:focus,
        .st-key-dl_calendar .stButton > button:active {{
            box-shadow: none !important;
            outline: none !important;
        }}
        .st-key-dl_calendar .stButton > button,
        .st-key-dl_calendar .stButton > button:focus,
        .st-key-dl_calendar .stButton > button:active,
        .st-key-dl_calendar .stButton > button div[data-testid="stMarkdownContainer"] p {{
            color: {c['text']} !important;
        }}
        .st-key-dl_calendar div[data-testid="stElementContainer"] {{
            width: 100% !important;
        }}
        .st-key-dl_calendar .stButton {{
            width: 100% !important;
        }}
        .stButton > button:has(div[data-testid="stMarkdownContainer"]) {{
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }}
        .stButton > button div[data-testid="stMarkdownContainer"] {{
            width: 100%;
            text-align: center !important;
        }}
        .stButton > button div[data-testid="stMarkdownContainer"] p {{
            text-align: center !important;
            margin: 0 !important;
            width: 100%;
        }}
        
        /* full-bleed hr */
        hr {{
            border: none !important;
            border-top: 3px solid {c['border']} !important;
            margin: 0.8rem -1.5rem !important;
            width: calc(100% + 3rem) !important;
        }}
        /* auth buttons: connected segmented pair */
        .st-key-dl_authbar div[data-testid="stHorizontalBlock"] {{ gap: 0 !important; }}
        .st-key-dl_authbar [data-testid="stColumn"]:not(:first-child) .stButton > button {{
            border-left: none !important;
        }}
        </style>
    """, unsafe_allow_html=True)


def title(text, size):
    st.markdown(f"<div class='dl-title' style='font-size:{size}px;'>{text}</div>", unsafe_allow_html=True)

def label(text):
    st.markdown(f"<div class='dl-label'>{text}</div>", unsafe_allow_html=True)

def divider():
    st.markdown("<div class='dl-divider'></div>", unsafe_allow_html=True)

def close_frame():
    st.markdown("<div class='dl-divider' style='margin-top:2rem;'></div>", unsafe_allow_html=True)