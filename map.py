# Import necessary libraries
import plotly.express as px
import streamlit as st

# --------------------------------------------------- Results: Map --------------------------------------------------- #

# Load final suppliers dataset for map
encoded_suppliers = st.session_state.encoded_suppliers
st.title("Map of DME Suppliers Accepting Assignment")



# Iterate through datasets to get lists of unique specialities and supplies in the dataset
specialities = set()
for row in encoded_suppliers.itertuples():
    row_specialities = row.specialitieslist
    for supply in row_specialities:
        specialities.add(supply)
specialities = sorted(list(specialities))
        
supplies = set()
for row in encoded_suppliers.itertuples():
    row_supplies = row.supplieslist
    for supply in row_supplies:
        supplies.add(supply)
supplies = sorted(list(supplies))

chosen_speciality = st.selectbox("Specialities", list(specialities))
chosen_supply = st.selectbox("Supplies", list(supplies))

selected_suppliers = encoded_suppliers.copy(deep = True)
    
if chosen_speciality != "All":
    selected_suppliers = selected_suppliers[selected_suppliers['specialitieslist'].apply(lambda x: chosen_speciality in x)]

if chosen_supply != "All":
    selected_suppliers = selected_suppliers[selected_suppliers['supplieslist'].apply(lambda x: chosen_supply in x)]

# Create map using lat/long, add hover interactivity to display locational information and specialities
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