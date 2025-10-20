# Import necessary libraries
from datetime import datetime
import plotly.express as px
import streamlit as st

st.title("Suppliers by State")

eda_states = st.session_state.eda_states

st.write("This section explores the relationship between the number of suppliers in each state and the many variables present in the Health Insurance Coverage dataset corresponding to each state. I iterated over the Medical Equipment Suppliers dataset, and created three dictionaries storing counts. The first tracked the number of suppliers in each state, and the second and third track the number of suppliers in each state that do or don't accept assignment. I made sure to restrict the range of these entries using the participationbegindate variable, to only select points from the time frame of the Health Insurance Coverage dataset (2010-2016). I then used this to create four new columns in the Health Insurance Coverage dataset: Supplier Count (2010-2016), Assignment-Accepting Supplier Count (2010-2016), Assignment-Rejecting Supplier Count (2010-2016), and Assignment Acceptance Ratio. The last column, Assignment Acceptance Ratio, is the result of dividing a state's Assignment-Accepting Supplier Count by its Assignment-Rejecting Supplier Count, with a high ratio indicating more accepting and a low ratio indicating more rejecting assignment.")
st.write("Below is a sample of this data:")

st.write(eda_states[["State", "Assignment-Accepting Supplier Count (2010-2016)", "Assignment-Rejecting Supplier Count (2010-2016)", "Assignment Acceptance Ratio"]])

st.write("This plot graphs Supplier Count against Uninsured Rate Change, and two distinct trends are noticeable. Firstly, all of the points are less than zero (black line), indicating that every state saw a decrease in its proportion of residents who were uninsured from 2010 to 2015. Secondly, this data's line of best fit has a negative slope, with values decreasing as Supplier Count increases. This indicates that high supplier counts correlate to lower rates of uninsured residents.")

fig = px.scatter(eda_states, x = "Supplier Count (2010-2016)", y = "Uninsured Rate Change (2010-2015)", trendline = "ols")
fig.add_hline(y = 0)
st.plotly_chart(fig)

st.write("This next plot echoes the results shown in the last plot, but flips the logic. Graphing Supplier Count against Medicaid Enrollment Change, you can see that Medicaid Enrollment Change is all positive, and increases with Supplier Count, again showing a positive relationship between the two variables.")

fig = px.scatter(eda_states, x = "Supplier Count (2010-2016)", y = "Medicaid Enrollment Change (2013-2016)", trendline = "ols")
st.plotly_chart(fig)

st.write("This last plot is a histogram, showing the Assignment-Acceptance Ratio for each state. Some states have incredibly high ratios, indicating the majority of their suppliers accept assignment. Some notable states from this group include Arizona (18.125), Montana (8.667), and Wyoming (8.5). Other states have incredibly low ratios, like Arkansas (0.215), Louisiana (0.175), New Hampshire (0.175), and New Mexico (0.161). In these states, most suppliers do not accept assignment, making affordable healthcare much harder to come by.")

fig = px.histogram(eda_states, x = "State", y = "Assignment Acceptance Ratio")
fig.add_hline(y = eda_states["Assignment Acceptance Ratio"].mean(), line_color = "red")
st.plotly_chart(fig)