#necessary libraries
import streamlit as st
import pandas as pd 
import warnings
warnings.filterwarnings('ignore')
import pickle
from pickle import load



#####
label_mapping = {'apple': 0,
                  'avocado': 1,
                  'banana': 2, 
                  'chickpea': 3, 
                  'coconut': 4, 'coffee': 5, 'cotton': 6, 'kidneybeans': 7, 'lemon': 8, 'lentil': 9, 'maize': 10, 'mango': 11, 'millet': 12, 'mothbeans': 13, 'mungbean': 14, 'orange': 15, 'papaya': 16, 'pigeonpeas': 17, 'potatoes': 18, 'rice': 19, 'sorghum': 20, 'tomatoes': 21, 'watermelon': 22}



#load rf ML model

with open('model.pkl', 'rb') as file:
  model = pickle.load(file)
#model_path = "pages\model.pkl"
#if model_path:
 # with open(model_path, 'rb') as file:
   # model = load(file)
###################

#prompting user input
st.subheader("Please enter soil data :")
#
#text_input_date = st.date_input("Enter Date:")
number_inputs = st.columns(4)
n_value = number_inputs[0].number_input("Nitrogen(N)", min_value=0)
p_value = number_inputs[1].number_input("Phosphorous(P)", min_value=0)
k_value = number_inputs[2].number_input("Potassium(K)", min_value=0)
ph_value = number_inputs[3].number_input("pH",min_value= 1, max_value= 14)
num_inputs=st.columns(3)
temp_value = num_inputs[0].number_input("Temperature")
rain_value = num_inputs[1].number_input("Rainfall")
humidity_value = num_inputs[2].number_input("Humidity")


# Load crop labels (
crop_labels_df = pd.read_csv("crop_labels.csv")
label_to_name_map = dict(zip(crop_labels_df["label"], crop_labels_df["crop_name"]))


# Button with combined functionality: prediction and download
download_button = st.button("Save User Input & Prediction as CSV")

# Load crop labels (assuming a CSV file with format "label,crop_name")
crop_labels_df = pd.read_csv("crop_labels.csv")
label_to_name_map = dict(zip(crop_labels_df["label"], crop_labels_df["crop_name"]))


def make_prediction_and_download(user_data):
    
    # Prepare data for prediction
    new_data = pd.DataFrame([user_data])
    predicted_crop = model.predict(new_data)[0]  

    # Map predicted label to crop name using the mapping dictionary
    predicted_crop_name = label_to_name_map[predicted_crop]

    # Update user data dictionary with prediction
    user_data["Recommended Crop"] = predicted_crop_name

    # Display the predicted crop name
    st.success(f"Recommended Crop: {predicted_crop_name}")

    # Download data as CSV
    csv_data = [user_data]
    df = pd.DataFrame(csv_data)
    csv_file = df.to_csv(index=False)

    st.download_button(label="Download User Input & Prediction", data=csv_file, mime="text/csv", file_name="user_input_recommendation.csv")


if download_button:
    # Create a dictionary to store
    user_data = {
        "nitrogen": n_value,
        "phosphorous": p_value,
        "potassium": k_value,
        "temperature": temp_value,
        "humidity": humidity_value,
        "ph": ph_value,
        "rainfall": rain_value
    }

    make_prediction_and_download(user_data)
    #warnings for ranges outside the recommended
    if n_value < 20:
        st.warning("Nitrogen deficiency detected! Consider adding nitrogen fertilizer to your soil.")
        
    elif n_value > 100:
        st.warning("Excess nitrogen detected!Crops with high nitrogen uptake that might be suitable: rice, banana, potatoes, cotton")

    if p_value < 8:
        st.warning("Phosphorus deficiency detected! Consider adding fertilizer with more phosphates to your soil.")
    elif p_value > 40:
        st.warning("Excess phosphorus detected! Crops with high phosphorus uptake that might be suitable: banana, cotton, mango")

    if k_value <20:
        st.warning("Potassium deficiency detected! Consider adding fertilizer with more potassium to your soil.")
    elif k_value >300:
        st.warning("Excess potassium detected! Crops with high potassium uptake that might be suitable: avocado, chickpea")

    if ph_value <5.5:
        st.warning("Low pH detected! Consider adding wood ash, lime(calcium carbonate) or dolomite Lime(calcium carbonate & magnesium carbonate) to your soil.")
    elif ph_value >7.5:
        st.warning("High pH detected! consider using fertilizer with more suphate content")
