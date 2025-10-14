# Import necessary libraries
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
import plotly.express as px
import streamlit as st

suppliers = pd.read_excel("Data/MedicalEquipmentSuppliers.xls")
st.title("Map of DME Suppliers Accepting Assignment")


# Rename misspelled acceptsassignement column, reformat columns for clean appearance in web app
suppliers.rename(columns = {
    "acceptsassignement": "Accepts Assignment"
    })

# Create new copy of suppliers dataset for cleaning process
split_suppliers = suppliers.copy(deep = True)

# Drop any rows missing values in our columns of interest (specialitieslist and suppliestlist)
split_suppliers = split_suppliers.dropna(subset = ["specialitieslist", "supplieslist"]).reset_index(drop = True)

# Break up each entry in columns of interest into lists, splitting on vertical bars
split_suppliers["specialitieslist"] = split_suppliers["specialitieslist"].str.split("|")
split_suppliers["supplieslist"] = split_suppliers["supplieslist"].str.split("|")

# Use MultiLabelBinarizer to one-hot encode columns of interest, concatenate with original data
# Note: This code block was generated with assistance from ChatGPT (Version 5), accessed on 10/13/2025
mlb = MultiLabelBinarizer()
encoded_specialities = pd.DataFrame(
    mlb.fit_transform(split_suppliers["specialitieslist"]),
    columns = mlb.classes_,
    index = split_suppliers.index
)
encoded_supplies = pd.DataFrame(
    mlb.fit_transform(split_suppliers["supplieslist"]),
    columns = mlb.classes_,
    index = split_suppliers.index
)
suppliers_encoded = pd.concat([split_suppliers, encoded_specialities, encoded_supplies], axis = 1)




selected_specialities = ["Pharmacy"]
selected_supplies = []

selected_suppliers = suppliers_encoded.copy(deep = True)
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