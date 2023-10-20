# Google Maps Datasets

Google Maps has large dataset files that can be downloaded to get ultra high resolution 3d simulated views of locations in map context.  To do this requires a map account on google cloud along with a map project like below:

https://console.cloud.google.com/apis/library?project=eng-diagram-312111

Note ways to restrict includes referrers which allows you to constrained the domain URL that you can come from.  The other I like is the API restriction which allows type based restriction for example Javascript API only or Directions only which limits which features can be used with the secured API Key:

![image](https://github.com/AaronCWacker/AIMapFest/assets/30595158/329e2419-fa1c-41ab-b6a5-5b456737c719)


# List of Map Projects.
1. https://huggingface.co/spaces/awacke1/Northern.Lights.Map.Streamlit.Folium
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



import streamlit as st
import altair as alt
from vega_datasets import data
import pandas as pd
import pydeck as pdk

# Define the data source for the map
iceland_geojson = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/iceland/iceland-counties.json"

# Define the mythological cities with their respective latitude and longitude
cities = {
    "Asgard": [64.7938, -17.3413],
    "Helheim": [63.8278, -21.1865],
    "Jotunheim": [64.8441, -19.1669],
    "Midgard": [63.9863, -22.6210],
    "Muspellheim": [65.3201, -16.4235],
    "Nidavellir": [64.9011, -18.0580],
    "Svartalfheim": [64.0114, -21.4504],
    "Valhalla": [63.7267, -19.6133],
    "Vanaheim": [64.7381, -17.4497],
    "Yggdrasil": [64.8999, -19.0044]
}

# Define the colors to use for each city marker
colors = {
    "Asgard": [255, 0, 0],
    "Helheim": [255, 255, 0],
    "Jotunheim": [0, 0, 255],
    "Midgard": [0, 255, 0],
    "Muspellheim": [255, 153, 0],
    "Nidavellir": [153, 0, 255],
    "Svartalfheim": [0, 255, 255],
    "Valhalla": [255, 0, 255],
    "Vanaheim": [153, 255, 0],
    "Yggdrasil": [255, 255, 255]
}

# Define the Streamlit app layout
st.set_page_config(layout="wide")
st.title("Mythological Cities in Iceland")
st.sidebar.title("Select a City to View the Northern Lights From")
selected_city = st.sidebar.selectbox("", sorted(cities.keys()))

# Load the Icelandic county boundaries and prepare the data for the 3D map
iceland_data = alt.topo_feature(iceland_geojson, "iceland-counties")
iceland_df = pd.DataFrame(iceland_data["features"])

# Create the 3D map with Deck.gl and Altair
view_state = pdk.ViewState(latitude=64.9, longitude=-18.5, zoom=5, pitch=40)
layers = [
    pdk.Layer(
        "PolygonLayer",
        data=iceland_data,
        get_polygon="coordinates",
        filled=True,
        extruded=True,
        get_elevation="properties.avg_elevation",
        elevation_scale=1000,
        get_fill_color=[200, 200, 200, 200]
    ),
    pdk.Layer(
        "ScatterplotLayer",
        data=pd.DataFrame({"latitude": [cities[selected_city][0]], "longitude": [cities[selected_city][1]]}),
        get_position="[longitude, latitude]",
        get_color=colors[selected_city],
        get_radius=20000
    )
]

r = pdk.Deck(layers=layers, initial_view_state=view_state)
altair_chart = alt.Chart(iceland_df).mark_geoshape(
stroke="black",
strokeWidth=0.5
    ).encode(
        color=alt.Color("properties.avg_elevation:Q", scale=alt.Scale(scheme="viridis")),
        tooltip=[alt.Tooltip("properties.name", title="County"), alt.Tooltip("properties.avg_elevation:Q", title="Elevation (m)")]
    ).transform_lookup(
    lookup="id",
    from_=alt.LookupData(iceland_data, "id", ["properties.avg_elevation", "properties.name"])
    ).properties(
    width=900,
    height=600
).interactive()

# Display the 3D map and the Altair chart
st.pydeck_chart(r)
st.altair_chart(altair_chart)
