#necessary libraries
import streamlit as st
import plotly.express as px
import pandas as pd 
import os
import warnings
warnings.filterwarnings('ignore')
import csv
from pickle import load


#prompting user input
st.subheader("Please enter soil data :")
#
text_input_date = st.date_input("Enter Date:")
number_inputs = st.columns(4)
n_value = number_inputs[0].number_input("Nitrogen (N)", min_value=0)
p_value = number_inputs[1].number_input("Phosphorus (P)", min_value=0)
k_value = number_inputs[2].number_input("Potassium (K)", min_value=0)
p_value = number_inputs[3].number_input("pH",min_value= 1, max_value= 14)
num_inputs=st.columns(2)
temp_value = num_inputs[0].number_input("Temperature (C)")
rain_value = num_inputs[1].number_input("Rainfall (mm)")

# Button to trigger prediction and saving
save_button = st.button("Save Inputs and Prediction to CSV")


# Make prediction and save data to CSV file (triggered on button click)
if save_button:
    #dictionary to store input data
  user_data = {
      "Date": text_input_date.strftime('%Y-%m-%d'),
      "Nitrogen (N)": n_value,
      "Phosphorus (P)": p_value,
      "Potassium (K)": k_value,
      "pH": p_value,
      "Temperature (C)": temp_value,
      "Rainfall (mm)": rain_value
  }
  