import streamlit as st
import calendar
import datetime
import json
from utils.data import DATA_DIR

BOOKINGS_FILE = DATA_DIR / "bookings.json"

def _load_bookings():
    if BOOKINGS_FILE.exists():
        with open(BOOKINGS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}

def _save_bookings(bookings):
    with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(bookings, f, indent=2)


def render(loc):
    if "cal_year" not in st.session_state:
        today = datetime.date.today()
        st.session_state.cal_year = today.year
        st.session_state.cal_month = today.month
    if "selected_dates" not in st.session_state:
        st.session_state.selected_dates = set()

    col1, col2 = st.columns([2, 1])

    with col1:
        nav1, nav2, nav3 = st.columns([1, 3, 1])
        with nav1:
            if st.button("◀"):
                m, y = st.session_state.cal_month - 1, st.session_state.cal_year
                if m == 0:
                    m, y = 12, y - 1
                st.session_state.cal_month, st.session_state.cal_year = m, y
                st.rerun()
        with nav2:
            st.markdown(f"<div style='text-align:center; font-weight:600;'>{calendar.month_name[st.session_state.cal_month]} {st.session_state.cal_year}</div>", unsafe_allow_html=True)
        with nav3:
            if st.button("▶"):
                m, y = st.session_state.cal_month + 1, st.session_state.cal_year
                if m == 13:
                    m, y = 1, y + 1
                st.session_state.cal_month, st.session_state.cal_year = m, y
                st.rerun()

        with st.container(key="dl_calendar"):
            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            header_cols = st.columns(7, gap="small")
            for c, d in zip(header_cols, days):
                c.markdown(f"<div style='text-align:center; color:#8C8C8C; font-size:12px; padding:6px 0;'>{d}</div>", unsafe_allow_html=True)

            month_days = calendar.monthcalendar(st.session_state.cal_year, st.session_state.cal_month)
            for week in month_days:
                week_cols = st.columns(7, gap="small")
                for c, day in zip(week_cols, week):
                    if day == 0:
                        c.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)
                        continue
                    date_obj = datetime.date(st.session_state.cal_year, st.session_state.cal_month, day)
                    date_str = date_obj.isoformat()
                    selected = date_str in st.session_state.selected_dates
                    if c.button(str(day), key=f"day_{date_str}"):
                        if selected:
                            st.session_state.selected_dates.discard(date_str)
                        else:
                            st.session_state.selected_dates.add(date_str)
                        st.rerun()

        if st.session_state.selected_dates:
            st.caption(f"Selected: {', '.join(sorted(st.session_state.selected_dates))}")

    with col2:
        st.markdown("**Your details**")
        full_name = st.text_input("Full name", key="booking_name")
        email = st.text_input("E-mail", key="booking_email")
        message = st.text_area("Message", key="booking_message", height=150)

        if st.button("Confirm booking", type="primary"):
            if not st.session_state.selected_dates or not full_name or not email:
                st.warning("Pick at least one date and fill in name + email.")
            else:
                bookings = _load_bookings()
                entry = {
                    "name": full_name, "email": email, "message": message,
                    "dates": sorted(st.session_state.selected_dates),
                }
                bookings.setdefault(loc["id"], []).append(entry)
                _save_bookings(bookings)
                st.success(f"Booking request sent for {len(st.session_state.selected_dates)} date(s)!")
                st.session_state.selected_dates = set()