import streamlit as st
import calendar
import datetime
import json
from utils.data import DATA_DIR

BOOKINGS_FILE = DATA_DIR / "bookings.json"

def _load_bookings():
    if BOOKINGS_FILE.exists() and BOOKINGS_FILE.stat().st_size > 0:
        with open(BOOKINGS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}

def _save_bookings(bookings):
    with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(bookings, f, indent=2)

def _date_range(start, end):
    days = (end - start).days
    return [(start + datetime.timedelta(days=i)).isoformat() for i in range(days + 1)]

def render(loc):
    today = datetime.date.today()

    if "cal_year" not in st.session_state:
        st.session_state.cal_year = today.year
        st.session_state.cal_month = today.month
    st.session_state.setdefault("range_start", None)
    st.session_state.setdefault("range_end", None)

    bookings = _load_bookings()
    blocked_dates = set()
    for entry in bookings.get(loc["id"], []):
        blocked_dates.update(entry.get("dates", []))

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
            st.markdown(
                f"<div style='text-align:center; font-weight:600;'>"
                f"{calendar.month_name[st.session_state.cal_month]} {st.session_state.cal_year}</div>",
                unsafe_allow_html=True,
            )
        with nav3:
            if st.button("▶"):
                m, y = st.session_state.cal_month + 1, st.session_state.cal_year
                if m == 13:
                    m, y = 1, y + 1
                st.session_state.cal_month, st.session_state.cal_year = m, y
                st.rerun()

        css_rules = []

        with st.container(key="dl_calendar"):
            days_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            header_cols = st.columns(7, gap="small")
            for i, (c, d) in enumerate(zip(header_cols, days_labels)):
                weekend = i >= 5
                color = "var(--accent, #D9A441)" if weekend else "#8C8C8C"
                c.markdown(
                    f"<div style='text-align:center; color:{color}; font-size:12px; padding:6px 0;'>{d}</div>",
                    unsafe_allow_html=True,
                )

            month_days = calendar.monthcalendar(st.session_state.cal_year, st.session_state.cal_month)
            for week in month_days:
                week_cols = st.columns(7, gap="small")
                for c, day in zip(week_cols, week):
                    if day == 0:
                        c.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)
                        continue

                    date_obj = datetime.date(st.session_state.cal_year, st.session_state.cal_month, day)
                    date_str = date_obj.isoformat()
                    btn_key = f"day_{date_str}"

                    is_blocked = date_str in blocked_dates
                    is_past = date_obj < today
                    is_today = date_obj == today
                    is_weekend = date_obj.weekday() >= 5
                    start, end = st.session_state.range_start, st.session_state.range_end
                    is_edge = date_obj in (start, end)
                    in_range = start and end and start < date_obj < end
                    disabled = is_blocked or is_past

                    with c:
                        if st.button(str(day), key=btn_key, disabled=disabled):
                            if start is None or (start and end):
                                st.session_state.range_start = date_obj
                                st.session_state.range_end = None
                            elif date_obj < start:
                                st.session_state.range_end = start
                                st.session_state.range_start = date_obj
                            else:
                                st.session_state.range_end = date_obj
                            st.rerun()

                    sel = f".st-key-{btn_key} button"
                    if is_blocked:
                        css_rules.append(f"{sel} {{ opacity:0.3; text-decoration:line-through; }}")
                    elif is_past:
                        css_rules.append(f"{sel} {{ opacity:0.3; }}")
                    elif is_edge:
                        css_rules.append(
                            f"{sel} {{ background:#D9A441 !important; }} "
                            f"{sel} div[data-testid='stMarkdownContainer'] p {{ color:#1A1A1A !important; font-weight:700; }}"
                        )
                    elif in_range:
                        css_rules.append(
                            f"{sel} {{ background:rgba(217,164,65,0.18) !important; }} "
                            f"{sel} div[data-testid='stMarkdownContainer'] p {{ color:{'#F2F2F2'} !important; }}"
                        )
                    else:
                        extra = ""
                        if is_weekend:
                            extra += "color:#D9A441;"
                        if is_today:
                            extra += "border:1px solid #D9A441 !important;"
                        if extra:
                            css_rules.append(f"{sel} {{ {extra} }}")

        st.markdown(f"<style>{''.join(css_rules)}</style>", unsafe_allow_html=True)

        if st.session_state.range_start:
            label = st.session_state.range_start.isoformat()
            if st.session_state.range_end:
                label += f" → {st.session_state.range_end.isoformat()}"
            st.caption(f"Selected: {label}")

    with col2:
        st.markdown("**Your details**")
        with st.form("booking_form", clear_on_submit=True):
            full_name = st.text_input("Full name")
            email = st.text_input("E-mail")
            message = st.text_area("Message", height=150)
            submitted = st.form_submit_button("Confirm booking", type="primary")

        if submitted:
            start, end = st.session_state.range_start, st.session_state.range_end
            if not start or not full_name or not email:
                st.warning("Pick a date range and fill in name + email.")
            else:
                end = end or start
                dates = _date_range(start, end)
                if any(d in blocked_dates for d in dates):
                    st.error("Selected range overlaps an already booked date.")
                else:
                    entry = {"name": full_name, "email": email, "message": message, "dates": dates}
                    bookings.setdefault(loc["id"], []).append(entry)
                    _save_bookings(bookings)
                    st.success(f"Booking request sent for {len(dates)} date(s)!")
                    st.session_state.range_start = None
                    st.session_state.range_end = None
                    st.rerun()