# Import necessary libraries
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

# ------------------------------------------------ EDA: Key Variables ------------------------------------------------ #

st.title("Key Variables")

st.write("First, this is a table featuring summary statistics for each numeric column in the Health Insurance Coverage dataset, including count, mean, standard deviation, and the quantiles.")

# Load post-EDA version (final) of Health Insurance Coverage dataset (states)
eda_states = st.session_state.eda_states

# Write summary statistics to web app
st.write(eda_states.describe())

st.write("Next, this is a heatmap of the correlations between each numeric variable, also in the Health Insurance Coverage dataset. Darker blue colored squares indicate strong negative correlations, and darker colored red squares indicate strong positive correlations.")

# Create correlation matrix on states dataset, dropping non-numeric columns
corr_matrix = eda_states.drop(["State", "State Medicaid Expansion (2016)"], axis = 1).corr()

# Generate heatmap using corr_matrix and seaborn, write to web app
plt.figure(figsize = (16, 12))
sns.heatmap(corr_matrix, annot = True, cmap = "coolwarm")
st.pyplot(plt)