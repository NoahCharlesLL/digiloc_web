import streamlit as st

def render():
    st.markdown("### About Digital Locations")
    st.write(
        "Digital Locations is a scouting and booking platform built for film "
        "and photo productions across North Rhine-Westphalia. Browse real-world "
        "filming locations, explore detailed navigation and amenity info, mark "
        "up areas directly on the map, and request bookings — all in one place."
    )
    st.markdown("---")
    st.markdown("**How it works**")
    st.write("1. Browse locations on the map or list view.")
    st.write("2. Open a location to see photos, navigation details, and stage tools.")
    st.write("3. Draw custom areas on the location's map for planning access, restrictions, or equipment zones.")
    st.write("4. Request a booking directly through the calendar.")
    st.markdown("---")
    st.markdown("**Contact**")
    st.write("hello@digiloc.io")
    st.write("+49 30 000 000")