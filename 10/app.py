import streamlit as st
import graphviz as gv
from graphviz import Graph
import folium
from streamlit_folium import folium_static

# Define the cluster relations graph using gvmap
g = Graph(format='svg')
g.graph_attr['bgcolor'] = '#FFFFFF'
g.graph_attr['outputorder'] = 'edgesfirst'
g.graph_attr['size'] = '10,10'
g.node_attr['style'] = 'filled'
g.node_attr['shape'] = 'box'
g.node_attr['fillcolor'] = '#FFDAB9'

with g.subgraph(name='cluster_NJ') as c:
    c.graph_attr['bgcolor'] = '#ADD8E6'
    c.node_attr['color'] = '#000000'
    c.node_attr['fontcolor'] = '#000000'
    c.attr(label='New Jersey', fontsize='24')
    c.node('Hackensack Meridian Health', URL='https://www.hackensackmeridianhealth.org/', target='_blank', tooltip='Hackensack Meridian Health: Hackensack University Medical Center')
    c.node('RWJBarnabas Health', URL='https://www.rwjbh.org/', target='_blank', tooltip='RWJBarnabas Health: Robert Wood Johnson University Hospital')
    c.node('Atlantic Health System', URL='https://www.atlantichealth.org/', target='_blank', tooltip='Atlantic Health System: Morristown Medical Center')
    c.node('Virtua Health', URL='https://www.virtua.org/', target='_blank', tooltip='Virtua Health: Virtua Memorial Hospital')
    c.node('Inspira Health', URL='https://www.inspirahealthnetwork.org/', target='_blank', tooltip='Inspira Health: Inspira Medical Center Vineland')
    c.node('Cooper University Health Care', URL='https://www.cooperhealth.org/', target='_blank', tooltip='Cooper University Health Care: Cooper University Hospital')
    c.node('University Hospital', URL='https://www.uhnj.org/', target='_blank', tooltip='University Hospital: University Hospital')
    c.node('Robert Wood Johnson University Hospital Hamilton', URL='https://www.rwjbh.org/robert-wood-johnson-university-hospital-hamilton/', target='_blank', tooltip='Robert Wood Johnson University Hospital Hamilton: Robert Wood Johnson University Hospital Hamilton')
    c.node('Trinitas Regional Medical Center', URL='https://www.trinitasrmc.org/', target='_blank', tooltip='Trinitas Regional Medical Center: Trinitas Regional Medical Center')
    c.node('Capital Health Regional Medical Center', URL='https://www.capitalhealth.org/', target='_blank', tooltip='Capital Health Regional Medical Center: Capital Health Regional Medical Center')

# Render the graph using streamlit
st.graphviz_chart(g)

# Define hospitals data
hospitals = [('Hackensack Meridian Health', 'Hackensack University Medical Center', 40.899886, -74.039179),
             ('RWJBarnabas Health', 'Robert Wood Johnson University Hospital', 40.491301, -74.450611),
             ('Atlantic Health System', 'Morristown Medical Center', 40.787231, -74.473851),
             ('Virtua Health', 'Virtua Memorial Hospital', 39.931229, -75.025831),
             ('Inspira Health', 'Inspira Medical Center Vineland', 39.460225, -75.035542),
             ('Cooper University Health Care', 'Cooper University Hospital', 39.942743, -75.119090),
            ('University Hospital', 'University Hospital', 40.742310, -74.177609),
            ('Robert Wood Johnson University Hospital Hamilton', 'Robert Wood Johnson University Hospital Hamilton', 40.214008, -74.679619),
            ('Trinitas Regional Medical Center', 'Trinitas Regional Medical Center', 40.661474, -74.215013),
            ('Capital Health Regional Medical Center', 'Capital Health Regional Medical Center', 40.266778, -74.796452)]

#Create a map centered on New Jersey
m = folium.Map(location=[40.0583, -74.4057], zoom_start=8)

#Add markers for each hospital
for hospital in hospitals:
    folium.Marker(
        location=[hospital[2], hospital[3]],
        popup=f'{hospital[1]}<br>{hospital[2]},{hospital[3]}'
    ).add_to(m)

#Display the map in Streamlit
folium_static(m)
