import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# Define mythological places data for Iceland
mythological_places = [
    ('Ásbyrgi', 66.0082, -16.5096, 'Ásbyrgi is a horseshoe-shaped canyon, believed to have been formed by the hoof of Odin\'s eight-legged horse, Sleipnir.'),
    ('Dimmuborgir', 65.6083, -16.8996, 'Dimmuborgir, or "Dark Cities," is a lava field with dramatic rock formations. It is said to be the dwelling of trolls and elves.'),
    ('Hekla', 63.9920, -19.6656, 'Hekla is a stratovolcano believed to be the gateway to hell in the Middle Ages. It was also rumored to be a meeting place for witches.'),
    ('Elliðaey', 63.4845, -20.2785, 'Elliðaey is an isolated island, where, according to legend, a mythical monster called the skoffin, a hybrid of a cat and a fox, is said to have lived.'),
    ('Mývatn', 65.6039, -16.9965, 'Mývatn is a volcanic lake surrounded by unique geological formations. The area is steeped in folklore and is said to be home to various supernatural beings.'),
    ('Djúpalónssandur', 64.7439, -23.9033, 'Djúpalónssandur is a black sand beach, where, according to legend, a supernatural seal woman appeared and was captured by a fisherman.'),
    ('Reykjadalur', 64.0333, -21.2167, 'Reykjadalur, or "Steam Valley," is a geothermal area with hot springs. It is believed to be the home of hidden people, who live in the rocks and hills.'),
    ('Snaefellsjokull', 64.8080, -23.7767, 'Snaefellsjokull is a glacier-capped volcano that inspired Jules Verne\'s "Journey to the Center of the Earth." It is believed to hold mystical powers.'),
    ('Jokulsarlon', 64.0784, -16.2300, 'Jokulsarlon is a glacial lagoon that is said to be the site of an ancient Viking battle, where warriors fought for control of the area.'),
    ('Vatnajokull', 64.4150, -16.8333, 'Vatnajokull is Europe\'s largest glacier, and according to legend, it was formed by the tears of a grieving giantess.')
]

# Create a map centered on Iceland
m = folium.Map(location=[65.0, -18.0], zoom_start=7)

# Add markers for each mythological place and add them to a MarkerCluster
marker_cluster = MarkerCluster().add_to(m)
for place in mythological_places:
    folium.Marker(
        location=[place[1], place[2]],
        popup=f'<b>{place[0]}</b><br>{place[3]}',
        icon=folium.Icon(color='red')
    ).add_to(marker_cluster)

# Add PolyLine for paths between markers with animation
locations = [place[1:3] for place in mythological_places]
path = folium.PolyLine(locations, color='blue', opacity=0.8, weight=5, smooth_factor=0.5).add_to(m)
folium.plugins.PolyLineTextPath(polyline=path, text='\u25BA', repeat=True, offset=6, attributes={'fill': 'blue', 'font-weight': 'bold', 'font-size': '12'}).add_to(path)

folium_static(m)

st.markdown("""
# Icelandic Mythological Places

The map above shows the location of various mythological places in Iceland. Hover over the markers to learn more about the stories behind each location.

""")


# Add markers for each mythological place
for place in mythological_places:
    folium.Marker(
        location=[place[1], place[2]],
        popup=f'{place[0]}<br>{place[3]}',
        icon=folium.Icon(color='red')
    ).add_to(m)

# Function to update the map when a button is clicked
def update_map(place_data):
    m.location = [place_data[1], place_data[2]]
    m.zoom_start = 13
    folium_static(m)


for i in range(0, len(mythological_places), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(mythological_places):
            with cols[j]:
                if st.button(mythological_places[i + j][0]):
                    update_map(mythological_places[i + j])
folium_static(m)

st.markdown("""

Ásbyrgi: Thor, trying to prove his strength, challenged Sleipnir to a race. Odin agreed, but secretly fed Sleipnir his favorite snack, lightning bolts. With each step, Sleipnir left a massive print, and thus, Ásbyrgi was formed.

Dimmuborgir: Loki, the trickster, held a housewarming party for the trolls and elves in Dimmuborgir. He spiced the food with a touch of mischief, causing everyone to break into spontaneous, ridiculous dances that lasted for days.

Hekla: Freyja, the goddess of love, hosted a witches' convention on Hekla to improve their matchmaking skills. The witches accidentally brewed a love potion so powerful that it caused the volcano to erupt with passion.

Elliðaey: The skoffin, tired of its isolation, devised a plan to hitch a ride off the island. It disguised itself as a mythical creature tour guide, successfully luring a boat full of curious tourists to Elliðaey.

Mývatn: Balder, the god of light, organized a contest for the supernatural beings of Mývatn. The prize was an all-expenses-paid vacation to sunny Valhalla. The competition was fierce, with participants showing off their most impressive magic tricks.

""")


st.markdown("""
🏝️ Elliðaey Island: Home of the Skoffin
Elliðaey is a stunning and isolated island located off the southern coast of Iceland 🇮🇸. The island boasts a picturesque landscape and unique wildlife, including a legendary creature known as the skoffin 🐱‍🦲.

Legend has it that the skoffin is a rare hybrid of a cat 🐱 and a fox 🦊, with a long tail and sharp teeth. The creature is incredibly elusive and is said to only appear to those who are pure of heart ❤️. Those who are lucky enough to spot the skoffin will be blessed with good luck and fortune 🍀.

Despite its mythical reputation, Elliðaey has a long history of human habitation. In the 10th century, Viking settlers used the island for fishing 🎣 and farming 🌾. Throughout the centuries, the island has been used for a variety of purposes, including as a place of exile and as a hideaway for smugglers 🏴‍☠️.

In the 1950s, a hunting lodge was built on the island, attracting wealthy hunters who came to Elliðaey to hunt puffins 🐧. However, the lodge was abandoned in the 1980s, and the island is now uninhabited 🏚️.

Today, Elliðaey remains a popular destination for hikers 🚶‍♀️ and bird watchers 🦜 who come to enjoy the island's natural beauty and abundant wildlife 🌿. The island's fascinating history, legends, and stories continue to capture the imagination of those who visit 💭. Who knows, you might even catch a glimpse of the elusive skoffin 🤩!





Regenerate response
""")
                    