# Import necessary libraries
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load datasets
suppliers = pd.read_excel("Data/MedicalEquipmentSuppliers.xls")
states = pd.read_csv("Data/states.csv")

st.title("Initial Data Analysis")


st.header("Collection")


st.header("Quality and Integrity")
fig, axes = plt.subplots(1, 2, figsize=(35, 8))
sns.heatmap(suppliers.isna().transpose(), cmap = "magma", ax=axes[0])
sns.heatmap(states.isna().transpose(), cmap = "magma", ax=axes[1])
st.write(fig)


st.header("Structure and Context")
split_suppliers = suppliers.copy(deep=True)
split_suppliers = split_suppliers.dropna(subset=['specialitieslist', 'supplieslist']).reset_index(drop=True)
split_suppliers["specialitieslist"] = split_suppliers["specialitieslist"].str.split('|')
split_suppliers["supplieslist"] = split_suppliers["supplieslist"].str.split('|')

specialities = set()
for row in split_suppliers.itertuples():
    row_specialities = row.specialitieslist
    for supply in row_specialities:
        specialities.add(supply)

supplies = set()
for row in split_suppliers.itertuples():
    row_supplies = row.supplieslist
    for supply in row_supplies:
        supplies.add(supply)

mlb = MultiLabelBinarizer()
encoded = pd.DataFrame(
    mlb.fit_transform(split_suppliers['specialitieslist']),
    columns=mlb.classes_,
    index=split_suppliers.index
)
df_encoded = pd.concat([split_suppliers, encoded], axis=1)


st.header("Analysis Readiness Evaluation")
