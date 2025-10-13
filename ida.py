# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load datasets
suppliers = pd.read_excel("Data/MedicalEquipmentSuppliers.xls")
states = pd.read_csv("Data/states.csv")

st.title("Missing Data")

col1, col2 = st.columns(2)
with col1:
    #fig1, ax1 = plt.subplots()
    #sns.heatmap(suppliers.isna().transpose(), cmap = "magma", ax=ax1)
    #st.write(fig1)
    fig1 = plt.figure(figsize=(20,16))
    ax1 = fig1.add_subplot(111)
    sns.heatmap(suppliers.isna().transpose(), cmap = "magma", ax=ax1)
    st.write(fig1)

    
with col2:
    #missing_row_indices = states[states.isna().any(axis=1)].index.tolist()
    #states.loc[missing_row_indices,]
    #fig2, ax2 = plt.subplots()
    #sns.heatmap(states.isna().transpose(), cmap = "magma", ax=ax2)
    #st.write(fig2)
    fig2 = plt.figure(figsize=(20,16))
    ax2 = fig2.add_subplot(111)
    sns.heatmap(states.isna().transpose(), cmap = "magma", ax=ax2)
    st.write(fig2)
