import gradio as gr
import pandas as pd
import plotly.graph_objects as go
from datasets import load_dataset

dataset = load_dataset('text', data_files={'train': ['NPI_2023_01_17-05.10.57.PM.csv'], 'test': 'NPI_2023_01_17-05.10.57.PM.csv'})
#1.6GB NPI file with MH therapy taxonomy provider codes (NUCC based) with human friendly replacement labels (e.g. Counselor rather than code)
datasetNYC = load_dataset("gradio/NYC-Airbnb-Open-Data", split="train")
df = datasetNYC.to_pandas()

def MatchText(pddf, name):
    pd.set_option("display.max_rows", None)
    data = pddf
    swith=data.loc[data['text'].str.contains(name, case=False, na=False)]
    return swith

def getDatasetFind(findString):
    #finder = dataset.filter(lambda example: example['text'].find(findString))
    finder = dataset['train'].filter(lambda example: example['text'].find(findString))
    finder = finder = finder.to_pandas()
    g1=MatchText(finder, findString)
    return g1

def filter_map(min_price, max_price, boroughs):
    filtered_df = df[(df['neighbourhood_group'].isin(boroughs)) & (df['price'] > min_price) & (df['price'] < max_price)]
    names = filtered_df["name"].tolist()
    prices = filtered_df["price"].tolist()
    text_list = [(names[i], prices[i]) for i in range(0, len(names))]
    
    fig = go.Figure(go.Scattermapbox(
            customdata=text_list,
            lat=filtered_df['latitude'].tolist(),
            lon=filtered_df['longitude'].tolist(),
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=6
            ),
            hoverinfo="text",
            hovertemplate='Name: %{customdata[0]}Price: $%{customdata[1]}'
        ))

    fig.update_layout(
        mapbox_style="open-street-map",
        hovermode='closest',
        mapbox=dict(
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=40.67,
                lon=-73.90
            ),
            pitch=0,
            zoom=9
        ),
    )
    return fig

def centerMap(min_price, max_price, boroughs):
    filtered_df = df[(df['neighbourhood_group'].isin(boroughs)) & (df['price'] > min_price) & (df['price'] < max_price)]
    names = filtered_df["name"].tolist()
    prices = filtered_df["price"].tolist()
    text_list = [(names[i], prices[i]) for i in range(0, len(names))]
    
    latitude = 44.9382
    longitude = -93.6561
    
    fig = go.Figure(go.Scattermapbox(
            customdata=text_list,
            lat=filtered_df['latitude'].tolist(),
            lon=filtered_df['longitude'].tolist(),            mode='markers',
            marker=go.scattermapbox.Marker(
                size=6
            ),
            hoverinfo="text",
            #hovertemplate='Lat: %{lat} Long:%{lng} City: %{cityNm}'
        ))

    fig.update_layout(
        mapbox_style="open-street-map",
        hovermode='closest',
        mapbox=dict(
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=latitude,
                lon=longitude
            ),
            pitch=0,
            zoom=9
        ),
    )
    return fig


with gr.Blocks() as demo:
    with gr.Column():
        
        # Price/Boroughs/Map/Filter for AirBnB
        with gr.Row():
            min_price = gr.Number(value=250, label="Minimum Price")
            max_price = gr.Number(value=1000, label="Maximum Price")
        boroughs = gr.CheckboxGroup(choices=["Queens", "Brooklyn", "Manhattan", "Bronx", "Staten Island"], value=["Queens", "Brooklyn"], label="Select Boroughs:")
        btn = gr.Button(value="Update Filter")
        map = gr.Plot().style()
        
        # Mental Health Provider Finder
        with gr.Row():
            df20 = gr.Textbox(lines=4, default="", label="Find Mental Health Provider e.g. City/State/Name/License:")
            btn2 = gr.Button(value="Find")
        with gr.Row():
            df4 = gr.Dataframe(wrap=True, max_rows=10000, overflow_row_behaviour= "paginate")

        # City Map
        with gr.Row():
            df2 = gr.Textbox(lines=1, default="Mound", label="Find City:")
            latitudeUI = gr.Textbox(lines=1, default="44.9382", label="Latitude:")
            longitudeUI = gr.Textbox(lines=1, default="-93.6561", label="Longitude:")
            btn3 = gr.Button(value="Lat-Long")

    demo.load(filter_map, [min_price, max_price, boroughs], map)
    
    btn.click(filter_map, [min_price, max_price, boroughs], map)
    btn2.click(getDatasetFind,df20,df4 )
    # Lookup on US once you have city to get lat/long
    # US	55364	Mound	Minnesota	MN	Hennepin	053			44.9382	-93.6561	4
    #latitude = 44.9382
    #longitude = -93.6561
    #btn3.click(centerMap, map)
        
    btn3.click(centerMap, [min_price, max_price, boroughs], map)

demo.launch()