# AI Prompt Response Memory on Map Making Strategies in Gamification:

# Response 1:

import streamlit as st

# Game list and associated icons
games = [
    'Terraforming Mars', 
    'Twilight Imperium (Fourth Edition)', 
    'Scythe', 
    'Eclipse', 
    'Small World', 
    'Risk Legacy', 
    'Axis & Allies', 
    'Diplomacy', 
    'Pandemic Legacy: Season 1', 
    'Brass: Birmingham'
]

icons = ['🪐', '🚀', '🤖', '🌌', '🧝‍♂️', '🗺️', '⚔️', '🤝', '🦠', '🏭']

# Main code
st.title('Top Ten Board Games with Map-Making Strategies 🗺️')

for i, (game, icon) in enumerate(zip(games, icons)):
    st.markdown(f"{i + 1}. {game} {icon}")

    # Expanders for each game to outline map rules or strategies
    with st.expander(f"See Map Building & Gamification Strategy for {game}"):
        
        if game == 'Terraforming Mars':
            st.markdown("""
            🪐 **Terraforming Mars Map Strategies**
            1. 🌱 Opt for plant-heavy areas
            2. 💧 Prioritize water tiles
            3. 🏭 Position factories near energy resources
            4. 🌋 Leverage volcanic areas
            5. 🌐 Control key global parameters
            6. 💡 Plan your energy grid
            7. 🛤️ Connect your colonies
            8. 🌡️ Master temperature control
            9. 🎯 Aim for synergies
            10. 🚀 Upgrade spaceports for max mobility
            """)

        elif game == 'Twilight Imperium (Fourth Edition)':
            st.markdown("""
            🚀 **Twilight Imperium Map Strategies**
            1. 🌌 Position fleets in strategic nebulas
            2. 🏰 Fortify chokepoints
            3. ⚖️ Balance resources among systems
            4. 🌐 Establish effective trade routes
            5. 🛡️ Use PDS systems wisely
            6. 🌀 Be cautious around wormholes
            7. 🌟 Prioritize Mecatol Rex
            8. 🌕 Use moons for surprise attacks
            9. 🛠️ Optimize unit upgrades
            10. 🤝 Forge strategic alliances
            """)

        elif game == 'Scythe':
            st.markdown("""
            🤖 **Scythe Map Strategies**
            1. 🏞️ Choose starting positions wisely
            2. 🛠️ Optimize for factory cards
            3. 🗺️ Be aware of your neighbors
            4. 🌊 Control rivers for mobility
            5. 🏭 Maximize resource buildings
            6. 🛡️ Guard against backdoor attacks
            7. 🎯 Focus on objectives
            8. 🌾 Manage food resources
            9. 🎲 Play the probabilities
            10. 💎 Hunt for treasures
            """)

        # Add other games and their map strategies here in a similar manner

# Run the Streamlit app by navigating to your file in the command line and typing 'streamlit run [filename].py'


# Prompt 1:
Extend the program below to create a st.expander and emoji outline interface that shares an outline on the map building and gamification strategy for each game below that involves map making strategies or rulesets around a map.  itemize a 10 point emoji laden outline to share fun aspects of the map rules per game and create a streamlit interface extending this program:  # Top-Ten-Board-Games-Map-Making-Strategy
import streamlit as st

games = ['Terraforming Mars', 'Twilight Imperium (Fourth Edition)', 'Scythe', 'Eclipse', 'Small World', 'Risk Legacy', 'Axis & Allies', 'Diplomacy', 'Pandemic Legacy: Season 1', 'Brass: Birmingham']
icons = ['🪐', '🚀', '🤖', '🌌', '🧝‍♂️', '🗺️', '⚔️', '🤝', '🦠', '🏭']

for i, game in enumerate(games):
    st.markdown(f"{i+1}. {game} {icons[i]}")







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
