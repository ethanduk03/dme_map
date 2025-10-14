# Import necessary libraries
import io
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st

# Load datasets
suppliers = pd.read_excel("Data/MedicalEquipmentSuppliers.xls")
states = pd.read_csv("Data/states.csv")

st.title("Initial Data Analysis")
st.write("In this section, I will be running through an initial analysis of the datasets I will be using for this project. Looking at their origin, structure, and quality, the goal of this section is to gain a better understanding of these datasets in their raw form, and make a plan for how I can utilize these datasets to achieve my project goals.")





# -------------------------------------------------------------------------------------------------------------------- #
#                                                    Data Collection                                                   #
# -------------------------------------------------------------------------------------------------------------------- #
st.header("Data Collection")
st.write("""This project utilizes two datasets, the [Medical Equipment Suppliers](https://data.cms.gov/provider-data/dataset/ct36-nrcq#overview) dataset from Data.CMS.gov and the [Health Insurance Coverage](https://www.kaggle.com/datasets/hhs/health-insurance) dataset from Kaggle.\n\nInitially published on December 17th, 2020 but most recently updated on September 28th, 2025, the Medical Equipment Suppliers dataset comes directly from the U.S. Centers for Medicare and Medicaid Services, containing information on the location of Durable Medical Equipment (DME) suppliers, the services they provide, and if they are partnered with Medicare services.""")
st.write(suppliers.head())
st.write("""The Health Insurance Coverage dataset on Kaggle was published in a collaboration by the U.S. Department of Health and Human Services and Abigail Larion, a Data Intern at Kaggle. This dataset contains one entry for each of the 50 states, as well as one for the District of Columbia and one for the U.S. as a whole, and looks to compare health insurance coverage rates across these regions, looking at the effects of the Affordable Care Act (ACA). Each entry contains the average coverage rates for the corresponding region in 2010 and 2015, Medicaid and marketplace health insurance enrollment numbers in 2013 and 2016, and the number of people in each region that changed their health insurance coverage during this time. """)
st.write(states.head())





# -------------------------------------------------------------------------------------------------------------------- #
#                                              Data Quality and Integrity                                              #
# -------------------------------------------------------------------------------------------------------------------- #
st.divider()
st.header("Quality and Integrity of Data")


# -------------------------------------------------- Missing Values -------------------------------------------------- #
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

clean_suppliers = suppliers.copy(deep = True)
clean_suppliers = clean_suppliers.dropna(subset = ["specialitieslist", "supplieslist"]).reset_index(drop = True)

st.write("""For the Health Insurance Coverage dataset, I determined that the missingness in "State Medicaid Expansion (2013)" was logical, but that the missingness for "Medicaid Enrollment (2013)" and "Medicaid Enrollment Change (2013-2016)" would need to be addressed.""")
#TODO: Fix this missingness

st.write("""As you can see in the tables below, we have fixed the missingness in our data, and can proceed to the next step of our quality checks: looking for duplicate entries.""")

col1, col2 = st.columns(2)
with col1:
    missing_cols = ["specialitieslist", "supplieslist"]
    buffer1 = io.StringIO()
    clean_suppliers[missing_cols].info(buf = buffer1)
    st.text(buffer1.getvalue())
    
# TODO: replace with clean_states    
with col2:
    states[["State", "State Medicaid Expansion (2016)", "Medicaid Enrollment (2013)", "Medicaid Enrollment Change (2013-2016)"]].loc[[6, 19, 51],]

# ------------------------------------------------- Duplicate Entries ------------------------------------------------ #
st.subheader("Duplicate Entries")
st.write("As can be seen below, there are no duplicate entries in either dataset, as the number of total records and the number of unique records are the same.")
data = {
    "Dataset": ["Medical Equipment Suppliers", "Medical Equipment Suppliers", "Health Insurance Coverage", "Health Insurance Coverage"],
    "Record Type": ["Total", "Unique", "Total", "Unique"],
    "Count": [len(suppliers), len(suppliers.drop_duplicates()), len(states), len(states.drop_duplicates())],
}
missing_df = pd.DataFrame(data)
fig = px.bar(missing_df, x = "Record Type", y = "Count", color = "Dataset", barmode = "group", text = "Count", color_discrete_map = {"Medical Equipment Suppliers": "PaleGoldenRod", "Health Insurance Coverage": "Purple"})
st.plotly_chart(fig)


# ---------------------------------------------------- Data Types ---------------------------------------------------- #
st.subheader("Data Types")
st.write("""Some of the data types assigned to variables in the Health Insurance Coverage dataset do not make sense. Firstly, the variables measuring the proportion of the population without health insurance coverage "Uninsured Rate (2010)", "Uninsured Rate (2015)", and "Uninsured Rate Change (2010-2015)" are stored as strings with a percent symbol, rather than as floating points, or decimals. This will cause serious issues if any calculations are attempted, as they are not actually being stored as numbers but rather as groupings of characters, not intended for any calculations. Therefore, in my analysis, I will turn these into floats instead, so they can be treated like decimals. A similar issue is occurring on the "Average Monthly Tax Credit (2016)" column, as it supposed to be an integer representing a dollar amount but is instead being stored as a string with a dollar sign. I will need to change this to an integer. Finally, two of the columns, "Medicaid Enrollment (2013)" and "Medicaid Enrollment Change (2013-2016)", should be integers, representing people. However, they are being stored as floats, which is inefficient, so I will convert them back to integers.""")
st.write("""There is also an interesting data type choice in the Medical Equipment Suppliers dataset, where the "supplieslist" and "specialitieslist" entries are entered into the dataset as strings, with each entry consisting of a list of supplies or list of specialities all separated by vertical bars (|), like "Optometrist|Pharmacist". Knowing my end goal of one-hot encoding these different supplies and specialities, so that each row has a boolean value representing whether or not the corresponding supplier offers that good or service, this format is not very compatible. Therefore, I will go through these entries, use the split() function to divide these strings at each vertical bar, breaking them up into lists containing the individual supplies or specialities. I will then be using scikit-learn's [MultiLabelBinarizer()](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MultiLabelBinarizer.html) to one-hot encode these lists, making a new column for each possible value. Each of these columns' entries will be booleans, representing whether or not the corresponding row's supplier provides that good or service.""")





# -------------------------------------------------------------------------------------------------------------------- #
#                                              Data Structure and Context                                              #
# -------------------------------------------------------------------------------------------------------------------- #
st.divider()
st.header("Structure and Context of Data")

# --------------------------------------------------- Organization --------------------------------------------------- #
# TODO: how is the data organized?

# ----------------------------------------------------- Variables ---------------------------------------------------- #
# TODO: what variables do I have?

# --------------------------------------------------- Relationships -------------------------------------------------- #
# TODO: what are the relationships between our variables?

# ---------------------------------------------------- Granularity --------------------------------------------------- #
# TODO: what is the granularity of our observations?

# ------------------------------------------------------ Numbers ----------------------------------------------------- #
# TODO: what does each number actually represent?





# Rename misspelled acceptsassignement column, reformat columns for clean appearance in web app
suppliers.rename(columns = {"acceptsassignement": "Accepts Assignment"})

# Create new copy of suppliers dataset for cleaning process
split_suppliers = suppliers.copy(deep = True)

# Drop any rows missing values in our columns of interest (specialitieslist and suppliestlist)
split_suppliers = split_suppliers.dropna(subset = ["specialitieslist", "supplieslist"]).reset_index(drop = True)

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
suppliers_encoded = pd.concat([split_suppliers, encoded_specialities, encoded_supplies], axis = 1)





# -------------------------------------------------------------------------------------------------------------------- #
#                                       Analysis Readiness Evaluation of the Data                                      #
# -------------------------------------------------------------------------------------------------------------------- #
st.divider()
st.header("Analysis Readiness Evaluation of the Data")
# TODO: what can dataset tell us
# TODO: what questions can I reasonably answer
# TODO: what are the inherent limitations
# TODO: are the preconditions for our statistical methods met
