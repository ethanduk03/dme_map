# Import necessary libraries
import streamlit as st

st.title("Exploratory Data Analysis")

# Load data from session_state
clean_suppliers = st.session_state.clean_suppliers
clean_states = st.session_state.clean_states


# -------------------------------------------------------------------------------------------------------------------- #
#                                                     Data Structure
# -------------------------------------------------------------------------------------------------------------------- #
st.divider()
st.header("Dataset Structure")

# --------------------------------------------------- Organization --------------------------------------------------- #
# TODO: how is the data organized?

# ----------------------------------------------------- Variables ---------------------------------------------------- #
# TODO: what variables do I have?


# ---------------------------------------------------- Data Types ---------------------------------------------------- #
st.subheader("Data Types")
st.write("""Some of the data types assigned to variables in the Health Insurance Coverage dataset do not make sense. Firstly, the variables measuring the proportion of the population without health insurance coverage "Uninsured Rate (2010)", "Uninsured Rate (2015)", and "Uninsured Rate Change (2010-2015)" are stored as strings with a percent symbol, rather than as floating points, or decimals. This will cause serious issues if any calculations are attempted, as they are not actually being stored as numbers but rather as groupings of characters, not intended for any calculations. Therefore, in my analysis, I will turn these into floats instead, so they can be treated like decimals. A similar issue is occurring on the "Average Monthly Tax Credit (2016)" column, as it supposed to be an integer representing a dollar amount but is instead being stored as a string with a dollar sign. I will need to change this to an integer. Finally, two of the columns, "Medicaid Enrollment (2013)" and "Medicaid Enrollment Change (2013-2016)", should be integers, representing people. However, they are being stored as floats, which is inefficient, so I will convert them back to integers.""")
st.write("""There is also an interesting data type choice in the Medical Equipment Suppliers dataset, where the "supplieslist" and "specialitieslist" entries are entered into the dataset as strings, with each entry consisting of a list of supplies or list of specialities all separated by vertical bars (|), like "Optometrist|Pharmacist". Knowing my end goal of one-hot encoding these different supplies and specialities, so that each row has a boolean value representing whether or not the corresponding supplier offers that good or service, this format is not very compatible. Therefore, I will go through these entries, use the split() function to divide these strings at each vertical bar, breaking them up into lists containing the individual supplies or specialities. I will then be using scikit-learn's [MultiLabelBinarizer()](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MultiLabelBinarizer.html) to one-hot encode these lists, making a new column for each possible value. Each of these columns' entries will be booleans, representing whether or not the corresponding row's supplier provides that good or service.""")


# --------------------------------------------------- Relationships -------------------------------------------------- #
# TODO: what are the relationships between our variables?

# ---------------------------------------------------- Granularity --------------------------------------------------- #
# TODO: what is the granularity of our observations?

# ------------------------------------------------------ Numbers ----------------------------------------------------- #
# TODO: what does each number actually represent?


# -------------------------------------------------------------------------------------------------------------------- #
#                                       Analysis Readiness Evaluation of the Data                                      #
# -------------------------------------------------------------------------------------------------------------------- #
st.divider()
#st.header("Analysis Readiness Evaluation of the Data")
# TODO: what can dataset tell us
# TODO: what questions can I reasonably answer
# TODO: what are the inherent limitations
# TODO: are the preconditions for our statistical methods met
