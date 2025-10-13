# Import necessary libraries
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
st.write("This project utilizes two datasets, the [Medical Equipment Suppliers](https://data.cms.gov/provider-data/dataset/ct36-nrcq#overview) dataset from Data.CMS.gov and the [Health Insurance Coverage](https://www.kaggle.com/datasets/hhs/health-insurance) dataset from Kaggle.\n\nInitially published on December 17th, 2020 but most recently updated on September 28th, 2025, the Medical Equipment Suppliers dataset comes directly from the U.S. Centers for Medicare and Medicaid Services, containing information on the location of Durable Medical Equipment (DME) suppliers, the services they provide, and if they are partnered with Medicare services. All of the data in this dataset is categorical, except for the latitude and longitude coordinate pair describing each entry's geographical location, which are decimals.\n\nThe Health Insurance Coverage dataset on Kaggle was published in a collaboration by the U.S. Department of Health and Human Services and Abigail Larion, a Data Intern at Kaggle. This dataset contains one entry for each of the 50 states, as well as one for the District of Columbia and one for the U.S. as a whole, and looks to compare health insurance coverage rates across these regions, looking at the effects of the Affordable Care Act (ACA). Each entry contains the average coverage rates for the corresponding region in 2010 and 2015, Medicaid and marketplace health insurance enrollment numbers in 2013 and 2016, and the number of people in each region that changed their health insurance coverage during this time. The variables describing coverage rates are measured in percentages, and the population totals are measured in terms of people. There is also a variable tracking the average monthly tax credit from 2016, rounded to the nearest U.S. dollar.")





# -------------------------------------------------------------------------------------------------------------------- #
#                                              Data Quality and Integrity                                              #
# -------------------------------------------------------------------------------------------------------------------- #
st.divider()
st.header("Quality and Integrity of Data")


# -------------------------------------------------- Missing Values -------------------------------------------------- #
st.subheader("Missing Values")
missing_practiceaddress2 = len(suppliers[suppliers["practiceaddress2"].isna()])
missing_specialitieslist = len(suppliers[suppliers["specialitieslist"].isna()])
missing_providertypelist = len(suppliers[suppliers["providertypelist"].isna()])
missing_supplieslist = len(suppliers[suppliers["supplieslist"].isna()])
st.write(f"""In its {len(suppliers)} rows, The Medical Equipment Suppliers dataset has many missing values. The "practiceaddress2" column has {missing_practiceaddress2} missing entries, the "specialitieslist" column has {missing_specialitieslist} missing entries, the "providertypelist" column has {missing_providertypelist} missing entries, and the "supplieslist" column has {missing_supplieslist} missing entries. As you can see in the heatmaps below, almost all of the entries in "practiceaddress2" and "providertypelist" have missing values. However, this does not pose any threat to my analysis. I do not need "providertypelist" for any of my project goals, and I will only need "practiceaddress2" when providing users with information on suppliers matching their needs, where it will be straightforward to pull in the value of "practiceaddress2" if it exists. The missing values in "specialitieslist" and "supplieslist" are more of an issue, as these are two of my main columns of interest. To resolve this issue, since the number of offending rows is so little, I am simply going to drop the rows with missing speciality or supply entries from the dataframe.""")
st.write("""The Kaggle dataset has three entries missing values in its 52 rows, a much more manageable number than the last dataset. The variable "Medicaid Enrollment (2013)" has missing values for the rows concerning Connecticut and Maine, and the "State Medicaid Expansion (2016)" is missing a value for the row concerning the entire United States. "State Medicaid Expansion (2013)" having no entry for the U.S. row makes sense, as the U.S. isn"t a state. However, "Medicaid Enrollment (2013)" having missing values is an issue, as that is not a logical omission but rather a hole in the data. To resolve this, I cannot simply drop the offending rows, as there is only one row per state, meaning all of them are essential! I will need to implement an imputation technique to fill in this gap in data for a very important variable.""")

# Create heatmaps to show missing data in each dataset
fig, axes = plt.subplots(1, 2, figsize = (35, 15))
sns.heatmap(suppliers.isna().transpose(), cmap = "magma", ax = axes[0])
sns.heatmap(states.isna().transpose(), cmap = "magma", ax = axes[1])
st.pyplot(fig)


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
st.write("""Some of the data types assigned to variables in the Health Insurance Coverage dataset do not make sense. Firstly, the variables measuring the proportion of the population without health insurance coverage "Uninsured Rate (2010)", "Uninsured Rate (2015)", and "Uninsured Rate Change (2010-2015)" are stored as strings with a percent symbol, rather than as floating points, or decimals. This will cause serious issues if any calculations are attempted, as they are not actually being stored as numbers but rather as groupings of characters, not intended for any calculations. Therefore, in my analysis, I will turn these into floats instead, so they can be treated like decimals. A similar issue is occurring on the "Average Monthly Tax Credit (2016)" column, as it supposed to be an integer representing a dollar amount but is instead being stored as a string with a dollar sign. We will need to change this to an integer. Finally, two of the columns, "Medicaid Enrollment (2013)" and "Medicaid Enrollment Change (2013-2016)", should be integers, representing people. However, they are being stored as floats, which is inefficient, so I will convert them back to integers.""")
st.write("""There is also an interesting data type choice in the Medical Equipment Suppliers dataset, where the "supplieslist" and "specialitieslist" entries are entered into the dataset as strings, with each entry consisting of a list of supplies or list of specialities all separated by vertical bars (|), like "Optometrist|Pharmacist". Knowing my end goal of one-hot encoding these different supplies and specialities, so that each row has a boolean value representing whether or not the corresponding supplier offers that good or service, this format is not very compatible. Therefore, I will go through these entries, use the split() function to divide these strings at each vertical bar, breaking them up into lists containing the individual supplies or specialities. I will then be using scikit-learn's [MultiLabelBinarizer()](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MultiLabelBinarizer.html) to one-hot encode these lists, making a new column for each possible value. Each of these columns' entries will be booleans, representing whether or not the corresponding row's supplier provides that good or service.""")





# -------------------------------------------------------------------------------------------------------------------- #
#                                              Data Structure and Context                                              #
# -------------------------------------------------------------------------------------------------------------------- #
st.divider()
st.header("Structure and Context of Data")
# TODO: how is the data organized?
# TODO: what variables do we have?
# TODO: what are the relationships between our variables?
# TODO: what is the granularity of our observations?
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

# Construct set of all unique specialities in dataset
specialities = set()
for row in split_suppliers.itertuples():
    row_specialities = row.specialitieslist
    for supply in row_specialities:
        specialities.add(supply)

# Construct set of all unique supplies in dataset
supplies = set()
for row in split_suppliers.itertuples():
    row_supplies = row.supplieslist
    for supply in row_supplies:
        supplies.add(supply)

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
# TODO: what questions can we reasonably answer
# TODO: what are the inherent limitations
# TODO: are the preconditions for our statistical methods met
