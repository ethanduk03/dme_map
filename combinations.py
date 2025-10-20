# Import necessary libraries
import plotly.express as px
import streamlit as st

st.title("Speciality and Supply Combinations")

# Load data from session_state
clean_suppliers = st.session_state.clean_suppliers
clean_states = st.session_state.clean_states
encoded_suppliers = st.session_state.encoded_suppliers

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

st.write("""This section explores the different combinations of specialities and supplies that exist in the Medical Equipment Suppliers dataset. Selecting a speciality and a supply from the dropdowns will display a view of the dataset, showing all suppliers that offer that speciality and that supply, as well as the number of such suppliers. Below this, a plot will be displayed, showing the true and false counts for the accepts_assignement variable, showing the balance of suppliers offering this supply and speciality that do or don't accept Medicare assignment. Below this plot is a bar chart, showing the amount of these suppliers in each state, again divided by accepts_assignement.""")

# Implement dropdown menu, save into variable for interactive use
chosen_speciality = st.selectbox("Specialities", list(specialities))
chosen_supply = st.selectbox("Supplies", list(supplies))

# Subset dataset based on selected attributes
result_suppliers = encoded_suppliers[(encoded_suppliers[chosen_speciality] == True) & (encoded_suppliers[chosen_supply] == True)]
st.write(result_suppliers)

# Print number of results, generate histogram of resulting dataframe based on who does/doesn't accept assignment
st.write(f"Out of {len(result_suppliers)} results:")
fig = px.histogram(result_suppliers, x = "acceptsassignement", color = "acceptsassignement", color_discrete_map = {0: "IndianRed", 1: "Green"})
st.plotly_chart(fig)

# Show distribution of all suppliers across states, divided by acceptsassignement
fig = px.histogram(result_suppliers, x = "practicestate", color = "acceptsassignement", color_discrete_map = {0: "IndianRed", 1: "Green"}, barmode = "group")
st.plotly_chart(fig)