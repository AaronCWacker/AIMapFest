# Streamlit Folium, Google Maps, Cesium, and Python Map Dashboards
https://www.youtube.com/playlist?list=PLHgX2IExbFovf9Y1AmsG2p0ehwR30_FDW

# List of Map Projects.
1. https://huggingface.co/spaces/awacke1/Northern.Lights.Map.Streamlit.Folium:  
2. https://huggingface.co/spaces/awacke1/HTML5-Aframe-3dMap-Flight
3. https://huggingface.co/spaces/awacke1/HTML5-Aframe-3D-Maps
4. https://huggingface.co/spaces/awacke1/Google-Maps-Web-Service-Py
5. https://huggingface.co/spaces/awacke1/UnitedStatesMapAIandNLP
6. https://huggingface.co/spaces/awacke1/MN.Map.Hospitals.Top.Five
7. https://huggingface.co/spaces/awacke1/3.HTML5-Aframe-3dMap-Flight
8. https://huggingface.co/spaces/awacke1/Maps.Markers.Honor.Iceland
9. https://huggingface.co/spaces/awacke1/Bird-Species-Migration-Month-Map
10. https://huggingface.co/spaces/awacke1/VizLib-TopLargeHospitalsNewJersey
11. https://huggingface.co/spaces/awacke1/Gradio-Maps-Latitude-Longitude
12. https://huggingface.co/spaces/awacke1/Top-Ten-Board-Games-Map-Making-Strategy

# Google Maps and Folium Together

```
Modify the program below to change the start location to Venice Beach, the destination to Santa Monica, and the list of medical centers to be the top ten medical centers with latitude and longitude for state of California.  import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import googlemaps
from datetime import datetime
import os

# Initialize Google Maps
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_KEY'))

# Function to fetch directions
def get_directions_and_coords(source, destination):
    now = datetime.now()
    directions_info = gmaps.directions(source, destination, mode='driving', departure_time=now)
    if directions_info:
        steps = directions_info[0]['legs'][0]['steps']
        coords = [(step['start_location']['lat'], step['start_location']['lng']) for step in steps]
        return steps, coords
    else:
        return None, None

# Function to render map with directions
def render_folium_map(coords):
    m = folium.Map(location=[coords[0][0], coords[0][1]], zoom_start=13)
    folium.PolyLine(coords, color="blue", weight=2.5, opacity=1).add_to(m)
    return m

# Function to add medical center paths and annotate distance
def add_medical_center_paths(m, source, med_centers):
    for name, lat, lon, specialty, city in med_centers:
        _, coords = get_directions_and_coords(source, (lat, lon))
        if coords:
            folium.PolyLine(coords, color="red", weight=2.5, opacity=1).add_to(m)
            folium.Marker([lat, lon], popup=name).add_to(m)
            distance_info = gmaps.distance_matrix(source, (lat, lon), mode='driving')
            distance = distance_info['rows'][0]['elements'][0]['distance']['text']
            folium.PolyLine(coords, color='red').add_to(m)
            folium.map.Marker(
                [coords[-1][0], coords[-1][1]],
                icon=folium.DivIcon(
                    icon_size=(150, 36),
                    icon_anchor=(0, 0),
                    html=f'<div style="font-size: 10pt; color : red;">{distance}</div>',
                    )
                ).add_to(m)

# Streamlit UI
st.title('Google Maps and Minnesota Medical Centers')
st.sidebar.header('Directions')

source_location = st.sidebar.text_input("Source Location", "Mound, MN")
destination_location = st.sidebar.text_input("Destination Location", "Minneapolis, MN")

if st.sidebar.button('Get Directions'):
    steps, coords = get_directions_and_coords(source_location, destination_location)
    if steps and coords:
        st.subheader('Driving Directions:')
        for i, step in enumerate(steps):
            st.write(f"{i+1}. {step['html_instructions']}")
        st.subheader('Route on Map:')
        m1 = render_folium_map(coords)
        folium_static(m1)
    else:
        st.write("No available routes.")

# The existing code for Minnesota medical centers
st.markdown("## 🏥 Minnesota Medical Centers 🌳")
m2 = folium.Map(location=[45.6945, -93.9002], zoom_start=6)
marker_cluster = MarkerCluster().add_to(m2)

# Define Minnesota medical centers data
minnesota_med_centers = [
    ('Mayo Clinic', 44.0224, -92.4658, 'General medical and surgical', 'Rochester'),
    ('University of Minnesota Medical Center', 44.9721, -93.2595, 'Teaching hospital', 'Minneapolis'),
    ('Abbott Northwestern Hospital', 44.9526, -93.2622, 'Heart specialty', 'Minneapolis'),
    ('Regions Hospital', 44.9558, -93.0942, 'Trauma center', 'St. Paul'),
    ('St. Cloud Hospital', 45.5671, -94.1989, 'Multiple specialties', 'St. Cloud'),
    ('Park Nicollet Methodist Hospital', 44.9304, -93.3640, 'General medical and surgical', 'St. Louis Park'),
    ('Fairview Ridges Hospital', 44.7391, -93.2777, 'Community hospital', 'Burnsville'),
    ('Mercy Hospital', 45.1761, -93.3099, 'Acute care', 'Coon Rapids'),
    ('North Memorial Health Hospital', 45.0131, -93.3246, 'General medical and surgical', 'Robbinsdale'),
    ('Essentia Health-Duluth', 46.7860, -92.1011, 'Community hospital', 'Duluth'),
    ('M Health Fairview Southdale Hospital', 44.8806, -93.3241, 'Community hospital', 'Edina'),
    ('Woodwinds Health Campus', 44.9272, -92.9689, 'Community hospital', 'Woodbury'),
    ('United Hospital', 44.9460, -93.1052, 'Acute care', 'St. Paul'),
    ('Buffalo Hospital', 45.1831, -93.8772, 'Community hospital', 'Buffalo'),
    ('Maple Grove Hospital', 45.1206, -93.4790, 'Community hospital', 'Maple Grove'),
    ('Olmsted Medical Center', 44.0234, -92.4610, 'General medical and surgical', 'Rochester'),
    ('Hennepin Healthcare', 44.9738, -93.2605, 'Teaching hospital', 'Minneapolis'),
    ('St. Francis Regional Medical Center', 44.7658, -93.5143, 'Community hospital', 'Shakopee'),
    ('Lakeview Hospital', 45.0422, -92.8137, 'Community hospital', 'Stillwater'),
    ('St. Luke\'s Hospital', 46.7831, -92.1043, 'Community hospital', 'Duluth')
]

# Annotate distances and paths for each medical center
add_medical_center_paths(m2, source_location, minnesota_med_centers)
folium_static(m2)
```

# California:

```
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import googlemaps
from datetime import datetime
import os

# Initialize Google Maps
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_KEY'))

# Function to fetch directions
def get_directions_and_coords(source, destination):
    now = datetime.now()
    directions_info = gmaps.directions(source, destination, mode='driving', departure_time=now)
    if directions_info:
        steps = directions_info[0]['legs'][0]['steps']
        coords = [(step['start_location']['lat'], step['start_location']['lng']) for step in steps]
        return steps, coords
    else:
        return None, None

# Function to render map with directions
def render_folium_map(coords):
    m = folium.Map(location=[coords[0][0], coords[0][1]], zoom_start=13)
    folium.PolyLine(coords, color="blue", weight=2.5, opacity=1).add_to(m)
    return m

# Function to add medical center paths and annotate distance
def add_medical_center_paths(m, source, med_centers):
    for name, lat, lon, specialty, city in med_centers:
        _, coords = get_directions_and_coords(source, (lat, lon))
        if coords:
            folium.PolyLine(coords, color="red", weight=2.5, opacity=1).add_to(m)
            folium.Marker([lat, lon], popup=name).add_to(m)
            distance_info = gmaps.distance_matrix(source, (lat, lon), mode='driving')
            distance = distance_info['rows'][0]['elements'][0]['distance']['text']
            folium.map.Marker(
                [coords[-1][0], coords[-1][1]],
                icon=folium.DivIcon(
                    icon_size=(150, 36),
                    icon_anchor=(0, 0),
                    html=f'<div style="font-size: 10pt; color : red;">{distance}</div>',
                    )
                ).add_to(m)

# Streamlit UI
st.title('Google Maps and California Medical Centers 🌴')
st.sidebar.header('Directions')

source_location = st.sidebar.text_input("Source Location", "Venice Beach, CA")
destination_location = st.sidebar.text_input("Destination Location", "Santa Monica, CA")

if st.sidebar.button('Get Directions'):
    steps, coords = get_directions_and_coords(source_location, destination_location)
    if steps and coords:
        st.subheader('Driving Directions:')
        for i, step in enumerate(steps):
            st.write(f"{i+1}. {step['html_instructions']}")
        st.subheader('Route on Map:')
        m1 = render_folium_map(coords)
        folium_static(m1)
    else:
        st.write("No available routes.")

# Top 10 medical centers in California
california_med_centers = [
    ('UCLA Medical Center', 34.0665, -118.4467, 'General medical and surgical', 'Los Angeles'),
    ('Cedars-Sinai Medical Center', 34.0762, -118.3801, 'Heart specialty', 'Los Angeles'),
    ('UCSF Medical Center', 37.7631, -122.4576, 'Teaching hospital', 'San Francisco'),
    ('Stanford Health Care-Stanford Hospital', 37.4331, -122.1754, 'Teaching hospital', 'Stanford'),
    ('Scripps La Jolla Hospitals', 32.8844, -117.2256, 'General medical and surgical', 'La Jolla'),
    ('Sharp Memorial Hospital', 32.8002, -117.1542, 'Community hospital', 'San Diego'),
    ('UCSD Medical Center-Hillcrest', 32.7550, -117.1711, 'Teaching hospital', 'San Diego'),
    ('Hoag Memorial Hospital Presbyterian', 33.6117, -117.8771, 'Community hospital', 'Newport Beach'),
    ('UCI Medical Center', 33.7886, -117.8934, 'Teaching hospital', 'Orange'),
    ('Long Beach Memorial Medical Center', 33.8034, -118.1689, 'Community hospital', 'Long Beach')
]

# Annotate distances and paths for each medical center
st.markdown("## 🏥 California Medical Centers 🌴")
m2 = folium.Map(location=[34.0522, -118.2437], zoom_start=6)
marker_cluster = MarkerCluster().add_to(m2)
add_medical_center_paths(m2, source_location, california_med_centers)
folium_static(m2)
```
