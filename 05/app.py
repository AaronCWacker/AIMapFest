import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
import folium
from folium import Choropleth, Circle, Marker, Popup, LayerControl
from folium.plugins import HeatMap
import pandas as pd

def heatmap_of_revenue_by_state(df):
    m1 = folium.Map(location=[37.7749, -100.4194], zoom_start=4)
    heat_data = [[row['Latitude'], row['Longitude'], row['Revenue']] for index, row in df.iterrows()]
    HeatMap(heat_data).add_to(m1)
    return m1

def top_corporations_by_state(df):
    m2 = folium.Map(location=[37.7749, -100.4194], zoom_start=4)
    for idx, row in df.iterrows():
        Marker([row['Latitude'], row['Longitude']], popup=f"{row['Corporation']} - Revenue: ${row['Revenue']}M").add_to(m2)
    return m2

def revenue_bands_by_state(df):
    m3 = folium.Map(location=[37.7749, -100.4194], zoom_start=4)
    def color_producer(val):
        if val < 2000:
            return 'green'
        elif val < 5000:
            return 'orange'
        else:
            return 'red'
    for idx, row in df.iterrows():
        Circle(
            location=[row['Latitude'], row['Longitude']],
            radius=int(row['Revenue']),
            color=color_producer(row['Revenue'])).add_to(m3)
    return m3

def multi_layer_map(df):
    m4 = folium.Map(location=[37.7749, -100.4194], zoom_start=4)
    heat_data = [[row['Latitude'], row['Longitude'], row['Revenue']] for index, row in df.iterrows()]
    HeatMap(heat_data).add_to(folium.FeatureGroup(name='Heat Map').add_to(m4))
    LayerControl().add_to(m4)
    for idx, row in df.iterrows():
        Marker([row['Latitude'], row['Longitude']], popup=f"{row['Corporation']} - Revenue: ${row['Revenue']}M").add_to(folium.FeatureGroup(name='Corporations').add_to(m4))
    LayerControl().add_to(m4)
    return m4

    # 5. Revenue Change Over Time (Simulated)
def revenue_change_over_time(df):
    df['Year'] = [2019 + i % 3 for i in range(len(df))]
    m5 = folium.Map(location=[37.7749, -100.4194], zoom_start=4)
    for year in [2019, 2020, 2021]:
        df_year = df[df['Year'] == year]
        heat_data_year = [[row['Latitude'], row['Longitude'], row['Revenue']] for index, row in df_year.iterrows()]
        HeatMap(heat_data_year, name=f"Revenue in {year}").add_to(folium.FeatureGroup(name=f"Year {year}").add_to(m5))
    LayerControl().add_to(m5)
    return m5

# 6. Distribution of Corporations
def distribution_of_corporations(df):
    m6 = folium.Map(location=[37.7749, -100.4194], zoom_start=4)
    corporation_count = df['State'].value_counts().reset_index()
    corporation_count.columns = ['State', 'Count']
    for idx, row in corporation_count.iterrows():
        state_row = df[df['State'] == row['State']].iloc[0]
        Circle(
            location=[state_row['Latitude'], state_row['Longitude']],
            radius=row['Count']*1000,
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(m6)
    return m6

# 7. Type of Corporations (Simulated)
def type_of_corporations(df):
    df['Type'] = ['Tech', 'Health', 'Finance', 'Retail'] * (len(df) // 4)
    m7 = folium.Map(location=[37.7749, -100.4194], zoom_start=4)
    for corp_type in ['Tech', 'Health', 'Finance', 'Retail']:
        df_type = df[df['Type'] == corp_type]
        for idx, row in df_type.iterrows():
            Marker([row['Latitude'], row['Longitude']], 
                   popup=f"{row['Corporation']} - Type: {row['Type']}",
                   icon=folium.Icon(color='blue' if corp_type == 'Tech' else 'green' if corp_type == 'Health' else 'red' if corp_type == 'Finance' else 'orange')).add_to(m7)
    return m7

# 8. Interactive Map
def interactive_map(df):
    m8 = folium.Map(location=[37.7749, -100.4194], zoom_start=4)
    for idx, row in df.iterrows():
        popup_content = f"""
        <strong>Corporation:</strong> {row['Corporation']}<br>
        <strong>State:</strong> {row['State']}<br>
        <strong>Revenue:</strong> ${row['Revenue']}M<br>
        <strong>Type:</strong> {row['Type']}
        """
        Popup(popup_content, max_width=300).add_to(
            Marker([row['Latitude'], row['Longitude']]).add_to(m8)
        )
    return m8

# 9. Geographical Clusters of Revenue
from folium.plugins import MarkerCluster

def geographical_clusters_of_revenue(df):
    m9 = folium.Map(location=[37.7749, -100.4194], zoom_start=4)
    marker_cluster = MarkerCluster().add_to(m9)
    for idx, row in df.iterrows():
        Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Corporation']} - Revenue: ${row['Revenue']}M"
        ).add_to(marker_cluster)
    return m9

# 10. Revenue vs. Location (Simulated 3D Map)
def revenue_vs_location(df):
    m10 = folium.Map(location=[37.7749, -100.4194], zoom_start=4)
    for idx, row in df.iterrows():
        Circle(
            location=[row['Latitude'], row['Longitude']],
            radius=row['Revenue'],
            color='purple',
            fill=True,
            fill_color='purple'
        ).add_to(m10)
    return m10
    
    
# Function to create a download link
def create_download_link(file_path, link_title):
    with open(file_path, 'rb') as file:
        csv_data = file.read()
    b64 = base64.b64encode(csv_data).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{link_title}.csv">{link_title}</a>'

# Function to plot the map
def plot_map(data):
    fig = px.choropleth(locations=data['State'], locationmode="USA-states", scope="usa")
    grouped_data = data.groupby('State')
    for state, group in grouped_data:
        top_corp = group.nlargest(1, 'Revenue')
        text_label = f"{top_corp['Corporation'].iloc[0]} - ${top_corp['Revenue'].iloc[0]}B"
        lon = group['Longitude'].mean()
        lat = group['Latitude'].mean()
        fig.add_trace(go.Scattergeo(
            lon=[lon],
            lat=[lat],
            text=text_label,
            mode='text',
        ))
    fig.update_layout(title="Top Corporation by State in the United States")
    return fig

st.title('Top Corporation by State in the United States 🏢')

# Upload CSV
uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True, type="csv")

# Display map button
display_map_button = st.button('Display Map of CSV Data 🗺️')

if display_map_button:
    if uploaded_files:
        for uploaded_file in uploaded_files:
            data = pd.read_csv(uploaded_file)
            st.write(f"Map for {uploaded_file.name} 🌐")
            st.plotly_chart(plot_map(data))
    else:
        st.write("Please upload a CSV file to proceed. 📑")

# Download link for the CSV file
csv_file_path = 'top_corporation_per_state.csv'
download_link = create_download_link(csv_file_path, "Top Corporations by State")
st.markdown(download_link, unsafe_allow_html=True)





import streamlit as st
import folium
from folium import Marker, Popup, Circle, LayerControl
from folium.plugins import HeatMap, MarkerCluster
import pandas as pd
import base64

def get_map_html_string(m):
    m.save("tmp_map.html")
    with open("tmp_map.html", "r") as f:
        html_string = f.read()
    return html_string

# Functions to generate maps
#{code_listing_5_6}
#{code_listing_7_10}

# Function to provide download link for HTML string
def provide_download_link(html_string, filename):
    b64 = base64.b64encode(html_string.encode()).decode()
    download_link = f'<a href="data:text/html;charset=utf-8;base64,{b64}" download="{filename}">Download {filename}</a>'
    return download_link

# Streamlit App
st.title("Map Visuals")

# Load data
st.write("### Upload your CSV file containing the data:")
uploaded_file = st.file_uploader("Choose a file", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Generate Maps
    map_list = [
        ("Heatmap of Revenue by State", heatmap_of_revenue_by_state),
        ("Top Corporations by State", top_corporations_by_state),
        ("Revenue Bands by State", revenue_bands_by_state),
        ("Multi-layer Map", multi_layer_map),
        ("Revenue Change Over Time", revenue_change_over_time),
        ("Distribution of Corporations", distribution_of_corporations),
        ("Type of Corporations", type_of_corporations),
        ("Interactive Map", interactive_map),
        ("Geographical Clusters of Revenue", geographical_clusters_of_revenue),
        ("Revenue vs. Location", revenue_vs_location)
    ]

    for idx, (title, func) in enumerate(map_list):
        st.write(f"### {title}")
        m = func(df)
        html_string = get_map_html_string(m)
        st.components.v1.html(html_string, width=900, height=600)
        st.markdown(provide_download_link(html_string, f"{title.replace(' ', '_')}.html"), unsafe_allow_html=True)


#streamlit_file_path
