# Import necessary libraries
import streamlit as st

st.set_page_config(layout = "wide")

home_page = st.Page("home.py", title = "Home", icon = "🏠")
ida_page = st.Page("ida.py", title = "Initial Data Analysis", icon = "🔍")
eda_page = st.Page("eda.py", title = "Exploratory Data Analysis", icon = "🚀")
map_page = st.Page("map.py", title = "Map", icon = "🗺️")

pg = st.navigation([home_page, ida_page, eda_page, map_page])
pg.run()