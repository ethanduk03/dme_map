# Import necessary libraries
import streamlit as st

st.set_page_config(layout="wide")

home_page = st.Page("home.py", title="Home", icon="🏠")
missing_data_page = st.Page("missingness.py", title="Missing Data", icon="🔍")
map_page = st.Page("map.py", title="Map", icon="🗺️")
citations_page = st.Page("citations.py", title="Citations", icon="📖")

pg = st.navigation([home_page, missing_data_page, map_page, citations_page])
pg.run()