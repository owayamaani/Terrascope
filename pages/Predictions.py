#necessary libraries
import streamlit as st
import plotly.express as px
import pandas as pd 
import os
import warnings
warnings.filterwarnings('ignore')
import csv
from pickle import load

#####
label_mapping = {'apple': 0,
                  'avocado': 1,
                  'banana': 2, 
                  'chickpea': 3, 
                  'coconut': 4, 'coffee': 5, 'cotton': 6, 'kidneybeans': 7, 'lemon': 8, 'lentil': 9, 'maize': 10, 'mango': 11, 'millet': 12, 'mothbeans': 13, 'mungbean': 14, 'orange': 15, 'papaya': 16, 'pigeonpeas': 17, 'potatoes': 18, 'rice': 19, 'sorghum': 20, 'tomatoes': 21, 'watermelon': 22}


#load ML model
model_path = "pages\model.pkl"
if model_path:
  with open(model_path, 'rb') as file:
    model = load(file)
###################

#prompting user input
st.subheader("Please enter soil data :")
#
#text_input_date = st.date_input("Enter Date:")
number_inputs = st.columns(4)
n_value = number_inputs[0].number_input("Nitrogen(N)", min_value=0)
p_value = number_inputs[1].number_input("Phosphor0us(P)", min_value=0)
k_value = number_inputs[2].number_input("Potassium(K)", min_value=0)
p_value = number_inputs[3].number_input("ph",min_value= 1, max_value= 14)
num_inputs=st.columns(3)
temp_value = num_inputs[0].number_input("temperature")
rain_value = num_inputs[1].number_input("rainfall")
humidity_value = num_inputs[2].number_input("humidity")

# Button to trigger prediction and saving
save_button = st.button("Save Inputs and Prediction to CSV")

# Load crop labels (assuming a CSV file with format "label,crop_name")
crop_labels_df = pd.read_csv("crop_labels.csv")
label_to_name_map = dict(zip(crop_labels_df["label"], crop_labels_df["crop_name"]))


# Make prediction and save data to CSV file (triggered on button click)
if save_button:
  # Create a dictionary to store input data
  user_data = {
      #"Date": text_input_date.strftime('%Y-%m-%d'),
      "Nitrogen(N)": n_value,
      "Phosphorous(P)": p_value,
      "Potassium(K)": k_value,
      "temperature": temp_value,
      "humidity": humidity_value,
      "ph": p_value,
      "rainfall": rain_value

  
      
  }

 # Prepare data for prediction
  new_data = pd.DataFrame([user_data])
  predicted_crop = model.predict(new_data)[0]  # Get the first prediction

  # Map predicted label to crop name using the mapping dictionary
  predicted_crop_name = label_to_name_map[predicted_crop]

  # Update user data dictionary with prediction
  user_data["Predicted Crop"] = predicted_crop_name

  
  # Display the predicted crop name
  st.success(f"Predicted Crop: {predicted_crop_name}")

  # Open the CSV file in append mode (avoids overwriting)
  with open("user_inputs.csv", "a", newline='') as csvfile:
    # Create a CSV writer object with fieldnames
    fieldnames = list(user_data.keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write header row if the file is empty
    if csvfile.tell() == 0:
      writer.writeheader()
    
    # Write user data with prediction as a dictionary row
    writer.writerow(user_data)
  
  st.success(f"Data saved successfully to user_inputs.csv!")

  