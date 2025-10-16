# Import necessary libraries
import pandas as pd
import plotly.express as px
import streamlit as st

# Load data from session_state
clean_suppliers = st.session_state.clean_suppliers
clean_states = st.session_state.clean_states

# ------------------------------------------------- Duplicate Entries ------------------------------------------------ #
st.subheader("Duplicate Entries")
st.write(f"""As can be seen below, there are no duplicate entries in either dataset, as the number of total records and the number of unique records are the same. You will notice that the total number of records in the Medical Equipment Suppliers dataset is now {len(clean_suppliers)}. That is because of the rows we dropped when handling the missing values, meaning there are {len(clean_suppliers)} entries in this dataset that have values for both "specialitieslist" and "supplieslist".""")

data = {
    "Dataset": ["Medical Equipment Suppliers", "Medical Equipment Suppliers", "Health Insurance Coverage", "Health Insurance Coverage"],
    "Record Type": ["Total", "Unique", "Total", "Unique"],
    "Count": [len(clean_suppliers), len(clean_suppliers.drop_duplicates()), len(clean_states), len(clean_states.drop_duplicates())],
}
missing_df = pd.DataFrame(data)
fig = px.bar(missing_df, x = "Record Type", y = "Count", color = "Dataset", barmode = "group", text = "Count", color_discrete_map = {"Medical Equipment Suppliers": "PaleGoldenRod", "Health Insurance Coverage": "Purple"})
st.plotly_chart(fig)