# Import necessary libraries
import pandas as pd
import plotly.express as px
import streamlit as st

suppliers = pd.read_excel("Data/MedicalEquipmentSuppliers.xls")
accepted = suppliers[suppliers["acceptsassignement"] == True]

st.title("Map of DME Suppliers Accepting Assignment")
st.map(accepted, latitude="latitude", longitude="longitude")
#map = px.scatter_geo(accepted, lat="latitude", lon="longitude")
#st.plotly_chart(map)