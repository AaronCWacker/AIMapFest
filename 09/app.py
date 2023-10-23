import streamlit as st
import folium
import json
from streamlit_folium import folium_static
import calendar

# Internal dataset saved as jsonl
birds_jsonl = '''
{"species": "Canada Goose", "lat": 44.9778, "lon": -93.2650, "start_month": "September", "end_month": "April"}
{"species": "Mallard Duck", "lat": 44.8835, "lon": -93.2273, "start_month": "August", "end_month": "May"}
{"species": "Wood Duck", "lat": 44.9778, "lon": -93.2650, "start_month": "March", "end_month": "November"}
{"species": "Trumpeter Swan", "lat": 45.0941, "lon": -94.2392, "start_month": "October", "end_month": "April"}
{"species": "Tundra Swan", "lat": 44.9358, "lon": -93.1553, "start_month": "November", "end_month": "April"}
{"species": "Canvasback", "lat": 44.8835, "lon": -93.2273, "start_month": "September", "end_month": "May"}
{"species": "Redhead", "lat": 44.9778, "lon": -93.2650, "start_month": "September", "end_month": "May"}
{"species": "Greater Scaup", "lat": 44.8835, "lon": -93.2273, "start_month": "September", "end_month": "May"}
{"species": "Lesser Scaup", "lat": 44.9778, "lon": -93.2650, "start_month": "September", "end_month": "May"}
{"species": "Hooded Merganser", "lat": 44.8835, "lon": -93.2273, "start_month": "October", "end_month": "April"}
'''
birds = [json.loads(line) for line in birds_jsonl.strip().split('\n')]

def create_marker(bird):
    species = bird['species']
    lat = bird['lat']
    lon = bird['lon']
    start_month = bird['start_month']
    end_month = bird['end_month']
    popup_msg = f"{species}: {start_month} - {end_month}"
    icon = folium.Icon(icon="cloud")
    return folium.Marker(location=[lat, lon], popup=popup_msg, icon=icon)

def create_map(center, zoom, markers):
    m = folium.Map(location=center, zoom_start=zoom)
    for marker in markers:
        marker.add_to(m)
    return m

st.title("Bird Migration Map 🦢")
st.markdown("### 📅 Use the slider to filter birds based on the months they are visible")

month = st.slider("Select a month", 1, 12, 1)
selected_markers = [create_marker(bird) for bird in birds if month >= list(calendar.month_abbr).index(bird['start_month'][:3]) and month <= list(calendar.month_abbr).index(bird['end_month'][:3])]

center = [44.9778, -93.2650]  # Latitude, Longitude
zoom = 8  # Initial zoom level

m = create_map(center, zoom, selected_markers)

# Show the map in Streamlit
folium_static(m)

# Using Streamlit to inject HTML and JavaScript for animation effects
st.markdown("<h2 style='text-align: center; color: red;'>This is a HTML header</h2>", unsafe_allow_html=True)

js_code = """
    // Your JavaScript code here
"""
st.markdown(f"<script>{js_code}</script>", unsafe_allow_html=True)
