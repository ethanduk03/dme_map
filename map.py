# Import necessary libraries
import plotly.express as px
import streamlit as st

encoded_suppliers = st.session_state.encoded_suppliers
st.title("Map of DME Suppliers Accepting Assignment")




selected_specialities = ["Pharmacy"]
selected_supplies = []

selected_suppliers = encoded_suppliers.copy(deep = True)
if len(selected_specialities):
    selected_suppliers = selected_suppliers[selected_suppliers[selected_specialities[0]] == True]

map = px.scatter_map(selected_suppliers,
                    lat = "latitude",
                    lon = "longitude",
                    hover_name = "practicename",
                    hover_data = ["practicecity", "practicestate", "specialitieslist"],
                    color = "acceptsassignement",
                    color_discrete_map = {0: "IndianRed", 1: "Green"},
                    map_style = "carto-darkmatter",
                    zoom = 2.5,
                    width = 1400,
                    height = 800)
st.plotly_chart(map)