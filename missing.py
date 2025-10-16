# Import necessary libraries
import io
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data from session_state
suppliers = st.session_state.suppliers
states = st.session_state.states

st.subheader("Missing Values")
st.write(f"""In its {len(suppliers)} rows, The Medical Equipment Suppliers dataset has many missing values. The "practiceaddress2" column has {len(suppliers[suppliers["practiceaddress2"].isna()])} missing entries, the "specialitieslist" column has {len(suppliers[suppliers["specialitieslist"].isna()])} missing entries, the "providertypelist" column has {len(suppliers[suppliers["providertypelist"].isna()])} missing entries, and the "supplieslist" column has {len(suppliers[suppliers["supplieslist"].isna()])} missing entries. As you can see in the heatmaps below, almost all of the entries in "practiceaddress2" and "providertypelist" have missing values. However, this does not pose any threat to my analysis. I do not need "providertypelist" for any of my project goals, and I will only need "practiceaddress2" when providing users with locational information on suppliers matching their needs, where it will be straightforward to pull in the value of "practiceaddress2" if it exists. However the missing values in "specialitieslist" and "supplieslist" are more of an issue, as these are two of my main columns of interest.""")

missing_cols = ["practiceaddress2", "specialitieslist", "providertypelist", "supplieslist"]
buffer = io.StringIO()
suppliers[missing_cols].info(buf = buffer)
st.text(buffer.getvalue())

st.write("""The Kaggle dataset has 3 entries missing values in its 52 rows, a much more manageable number than the last dataset. The variables "Medicaid Enrollment (2013)" and "Medicaid Enrollment Change (2013-2016)" have missing values for the rows concerning Connecticut and Maine, and the "State Medicaid Expansion (2016)" is missing a value for the row concerning the entire United States. "State Medicaid Expansion (2013)" having no entry for the U.S. row makes sense, as the U.S. isn't a state. However, "Medicaid Enrollment (2013)" and "Medicaid Enrollment Change (2013-2016)" having missing values is an issue, as these are not logical omissions but rather holes in the data.""")

states[["State", "State Medicaid Expansion (2016)", "Medicaid Enrollment (2013)", "Medicaid Enrollment Change (2013-2016)"]].loc[[6, 19, 51],]

# Create heatmaps to show missing data in each dataset
fig, axes = plt.subplots(1, 2, figsize = (35, 15))
sns.heatmap(suppliers.isna().transpose(), cmap = "magma", ax = axes[0])
sns.heatmap(states.isna().transpose(), cmap = "magma", ax = axes[1])
st.pyplot(fig)

st.write("""Now that I know this missingness exists, I need to address it. In the Medical Equipment Suppliers dataset, I determined that "practiceaddress2" will be fine as it is, and that "providertypelist" is irrelevant to the project goal. However, the missingness in "specialitieslist" and "supplieslist" is more of an issue. Since this is the most important information I would want from an entry in this dataset, an entry where one of these pieces of information is not valuable to me. Additionally, its categorical nature makes it very difficult to impute, or fill in, this missing data. Therefore, since these offending entries make up such a small percentage of the dataset, I will simply drop them from the dataset, getting rid of any entries with missingness in these columns.""")

clean_suppliers = st.session_state["clean_suppliers"]

st.write("""For the Health Insurance Coverage dataset, I determined that the missingness in "State Medicaid Expansion (2013)" was logical, but that the missingness for "Medicaid Enrollment (2013)" and "Medicaid Enrollment Change (2013-2016)" would need to be addressed. The Medicaid enrollment change was only missing because the value for Medicaid enrollment in 2013 was missing, so if I could impute the values of "Medicaid Enrollment (2013)" I could then calculate the corresponding "Medicaid Enrollment Change (2013-2016)". I decided to use regression to perform this imputation, using a linear regression model to predict the missing values of Medicaid enrollment in 2013 using the existing values of "Medicaid Enrollment (2016)" and "Medicare Enrollment (2016)". I then subtracted "Medicaid Enrollment (2013)" from "Medicaid Enrollment (2016)" in the two missing rows to fill in the missing values of "Medicaid Enrollment Change (2013-2016)".""")

clean_states = st.session_state["clean_states"]
st.write("""As you can see in the tables below, we have fixed the missingness in our data, and can proceed to the next step of our quality checks: looking for duplicate entries.""")

col1, col2 = st.columns([1, 2])
with col1:
    missing_cols = ["specialitieslist", "supplieslist"]
    buffer1 = io.StringIO()
    clean_suppliers[missing_cols].info(buf = buffer1)
    st.text(buffer1.getvalue())
    
with col2:
    clean_states[["State", "Medicaid Enrollment (2013)", "Medicaid Enrollment Change (2013-2016)"]].loc[[6, 19],]