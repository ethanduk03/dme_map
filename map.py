# Import necessary libraries
import pandas as pd
import plotly.express as px
import streamlit as st

suppliers = pd.read_excel("Data/MedicalEquipmentSuppliers.xls")
accepted = suppliers[suppliers["acceptsassignement"] == True]

st.title("Map of DME Suppliers Accepting Assignment")

map = px.scatter_map(suppliers,
                    lat = suppliers.latitude,
                    lon = suppliers.longitude,
                    hover_name = "practicename",
                    hover_data = ["practicecity", "practicestate"],
                    color = "acceptsassignement",
                    color_discrete_map = {0: "IndianRed", 1: "Green"},
                    map_style = "carto-darkmatter",
                    zoom = 2.5,
                    width = 1400,
                    height = 800)
st.plotly_chart(map)