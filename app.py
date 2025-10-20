# Import necessary libraries
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
import streamlit as st

# -------------------------------------------------------------------------------------------------------------------- #
#                           Create datasets and save to session_state for use in other pages                           #
# -------------------------------------------------------------------------------------------------------------------- #

# ------------------------------------ Load original suppliers and states datasets, save to session_state ----------------------------------- #
if "suppliers" not in st.session_state:
    st.session_state.suppliers = pd.read_excel("Data/MedicalEquipmentSuppliers.xls")
if "states" not in st.session_state:
    st.session_state.states = pd.read_csv("Data/states.csv")
    
suppliers = st.session_state.suppliers
states = st.session_state.states
    
# ---------------------- Copy original datasets, perform data cleaning and save to session_state --------------------- #
clean_suppliers = suppliers.copy(deep = True)
clean_suppliers = clean_suppliers.dropna(subset = ["specialitieslist", "supplieslist"]).reset_index(drop = True)

clean_states = states.copy(deep = True)
X = clean_states[["Medicaid Enrollment (2016)", "Medicare Enrollment (2016)"]]
y = clean_states["Medicaid Enrollment (2013)"]
X_train = X.drop([6, 19])
X_test = X.iloc[[6, 19]]
y_train = y.drop([6, 19])
y_test = y.iloc[[6, 19]]
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
y_pred = linear_model.predict(X_test)
clean_states.loc[6, "Medicaid Enrollment (2013)"] = int(y_pred[0])
clean_states.loc[19, "Medicaid Enrollment (2013)"] = int(y_pred[1])
clean_states.loc[6, "Medicaid Enrollment Change (2013-2016)"] = clean_states.loc[6, "Medicaid Enrollment (2016)"] - clean_states.loc[6, "Medicaid Enrollment (2013)"]
clean_states.loc[19, "Medicaid Enrollment Change (2013-2016)"] = clean_states.loc[19, "Medicaid Enrollment (2016)"] - clean_states.loc[19, "Medicaid Enrollment (2013)"]

clean_states["State"] = clean_states["State"].str.strip()
clean_states["Uninsured Rate (2010)"] = clean_states["Uninsured Rate (2010)"].str.rstrip("%").astype("float") / 100.0
clean_states["Uninsured Rate (2015)"] = clean_states["Uninsured Rate (2015)"].str.rstrip("%").astype("float") / 100.0
clean_states["Uninsured Rate Change (2010-2015)"] = clean_states["Uninsured Rate Change (2010-2015)"].str.rstrip()
clean_states["Uninsured Rate Change (2010-2015)"] = clean_states["Uninsured Rate Change (2010-2015)"].str.rstrip("%").astype("float") / 100.0
clean_states["Average Monthly Tax Credit (2016)"] = clean_states["Average Monthly Tax Credit (2016)"].str.lstrip("$").astype("int")
clean_states["Medicaid Enrollment (2013)"] = clean_states["Medicaid Enrollment (2013)"].astype("int")
clean_states["Medicaid Enrollment Change (2013-2016)"] = clean_states["Medicaid Enrollment Change (2013-2016)"].astype("int")

if "clean_suppliers" not in st.session_state:
    st.session_state.clean_suppliers = clean_suppliers
if "clean_states" not in st.session_state:
    st.session_state.clean_states = clean_states

# ---------------- Copy cleaned datasets, restructure and better organize data, save to session_state ---------------- #

# Create new copy of suppliers dataset for cleaning process
split_suppliers = clean_suppliers.copy(deep = True)

# Rename misspelled acceptsassignement column, reformat columns for clean appearance in web app
split_suppliers.rename(columns = {"acceptsassignement": "Accepts Assignment"})

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
encoded_suppliers = pd.concat([split_suppliers, encoded_specialities, encoded_supplies], axis = 1)

if "encoded_suppliers" not in st.session_state:
    st.session_state.encoded_suppliers = encoded_suppliers


# -------------------------------------------------------------------------------------------------------------------- #
#                                                   Streamlit styling                                                  #
# -------------------------------------------------------------------------------------------------------------------- #

st.set_page_config(layout = "wide")

# Overview
context_page = st.Page("context.py", title = "Context")
goals_page = st.Page("goals.py", title = "Project Goals")

# IDA
collection_page = st.Page("collection.py", title = "Data Collection")
missing_page = st.Page("missing.py", title = "Missing Data")
duplicates_page = st.Page("duplicates.py", title = "Duplicated Data")
structure_page = st.Page("structure.py", title = "Dataset Structure")

# EDA
combinations_page = st.Page("combinations.py", title = "Speciality and Supply Combinations")
supplier_states_page = st.Page("supplier_states.py", title = "Suppliers by State")
variables_page = st.Page("variables.py", title = "Key Variables")

# Results
map_page = st.Page("map.py", title = "Map")

pg = st.navigation({
    "Overview": [context_page, goals_page],
    "IDA": [collection_page, missing_page, duplicates_page, structure_page],
    "EDA": [combinations_page, supplier_states_page, variables_page],
    "Results": [map_page]
})
pg.run()