# Import necessary libraries
import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Integrating Health Insurance Coverage and 2016 Medicare Enrollment datasets")

eda_states = st.session_state.eda_states
years = st.session_state.years

st.write("""The goal of this section is to integrate the Health Insurance Coverage and 2016 Medicare Enrollment datasets, to hopefully inspire deeper insights into national patterns of insurance coverage over the time span covered by these datasets. By combining the 2016 Medicare Enrollment data with the United States' entry in the Health Insurance Coverage dataset, we can hopefully identify new patterns and draw significant comparisons.""")
st.write(eda_states[eda_states["State"] == "United States"])

st.write("""Above is the United States' entry in the Health Insurance Coverage dataset. By appending each entry in the 2016 row from the 2016 Medicare Enrollment dataset, a more detailed picture can be painted, with new statistics like yearly enrollment percentage increases and enrollment counts from different programs and sources. The new data below is the result of this integration.""")

us = eda_states[eda_states["State"] == "United States"]
us["Medicare Enrollment (2016)"] = years.loc[5, "Total Enrollment"]

for col in years.columns[2:]:
    us[col + " (2016)"] = years.loc[5, col]
    
us["Medicare Enrollment (2013)"] = years.loc[2, "Total Enrollment"]
us["Medicare Enrollment Change (2013-2016)"] = years.loc[5, "Total Enrollment"] - years.loc[2, "Total Enrollment"]

st.write(us)
st.write(f"""One such insight is shown below, with this next plot shows the different enrollment counts for Medicare and Medicaid in the years 2013 and 2016, with Medicare in blue and Medicaid in orange. It is interesting to observe the very minor increase in Medicare enrollment, especially when contrasted with the enormous jump that Medicaid enrollment took over this same three year period. Medicare enrollment only increased by {us.loc[51, "Medicare Enrollment Change (2013-2016)"]}, while Medicaid enrollment increased by a staggering {us.loc[51, "Medicaid Enrollment Change (2013-2016)"]}, quite a difference.""")

data = {
    "Year": [2013, 2016, 2013, 2016],
    "Program": ["Medicare", "Medicare", "Medicaid", "Medicaid"],
    "Enrollment": [us.loc[51, "Medicare Enrollment (2013)"], us.loc[51, "Medicare Enrollment (2016)"], us.loc[51, "Medicaid Enrollment (2013)"], us.loc[51, "Medicaid Enrollment (2016)"]]
}
df = pd.DataFrame(data)

fig = px.bar(df, x = "Year", y = "Enrollment", color = "Program", barmode = "group", text = "Enrollment", color_discrete_map = {"Medicare": "SkyBlue", "Medicaid": "Orange"})
st.plotly_chart(fig)