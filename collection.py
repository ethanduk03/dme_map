# Import necessary libraries
import streamlit as st

# ----------------------------------------------- IDA: Data Collection ----------------------------------------------- #

st.header("Data Collection")
st.write("""This project utilizes three datasets, the [Medical Equipment Suppliers](https://data.cms.gov/provider-data/dataset/ct36-nrcq#overview) dataset from Data.CMS.gov, the [Health Insurance Coverage](https://www.kaggle.com/datasets/hhs/health-insurance) dataset from Kaggle, and the [CMS Program Statistics - Medicare Total Enrollment - MDCR ENROLL AB 1](https://data.cms.gov/summary-statistics-on-beneficiary-enrollment/medicare-and-medicaid-reports/cms-program-statistics-medicare-total-enrollment) dataset, also from Data.CMS.gov.""")

st.write("""Initially published on December 17th, 2020 but most recently updated on September 28th, 2025, the Medical Equipment Suppliers dataset comes directly from the U.S. Centers for Medicare and Medicaid Services, containing information on the location of Durable Medical Equipment (DME) suppliers, the services they provide, and if they are partnered with Medicare services.""")
st.write(st.session_state["suppliers"].head())

st.write("""The Health Insurance Coverage dataset on Kaggle was published in a collaboration by the U.S. Department of Health and Human Services and Abigail Larion, a Data Intern at Kaggle. This dataset contains one entry for each of the 50 states, as well as one for the District of Columbia and one for the U.S. as a whole, and looks to compare health insurance coverage rates across these regions, looking at the effects of the Affordable Care Act (ACA). Each entry contains the average coverage rates for the corresponding region in 2010 and 2015, Medicaid and marketplace health insurance enrollment numbers in 2013 and 2016, and the number of people in each region that changed their health insurance coverage during this time. """)
st.write(st.session_state["states"].head())

st.write("""Containing data on Medicare enrollments from the years 2011 - 2016, the MDCR ENROLL AB 1 dataset, which I will refer to from now on as the 2016 Medicare Enrollment dataset, is part of a collection of datasets collected in 2016 available on the CMS Program Statistics - Medicare Total Enrollment webpage. Clicking download and subsetting down to a date range allows you to select which time period you gather data from. This dataset has no missing or duplicated values, and its contents are logically structured, so it is already prepped for EDA.""")
st.write(st.session_state["years"])