import streamlit as st
import json
import requests
from streamlit_lottie import st_lottie
import warnings
warnings.filterwarnings('ignore')


st.set_page_config(page_title=" About TerraScope", page_icon=":earth_africa:",layout="wide")
st.title (":earth_africa: TerraScope Smart-Soil Dashboard") 
st.markdown('<style>div.block-container{padding-top:2rem}</style>', unsafe_allow_html=True)

col1,col2 = st.columns((2))
with col1: 

    st.subheader("About TerraScope")

    st.write("TerraScope is a Smart-Soil Monitoring System that allows users to dynamically view their soil data. There are beautiful visualizations to help gain insight from the data uploaded. The application also allows users to view historical soil data and environmental factors over time.")

    st.write("TerraScope was developed as part of the Smart-Soil project, a project aimed at integrating technology in agriculture.")

    st.write("The Smart-Soil project aims to develop a Smart-Soil Monitoring System that uses Machine Learning to predict soil health. It is a web-based application that allows users to input soil data and receive a prediction on what crops to plant with the help of a Machine learning model.")

with col2:
    def load_lottiefile(filepath:str):
        with open(filepath, "r") as file:
            return json.load(file)

    lottie_file = load_lottiefile("analysis.json")
    st_lottie(
        lottie_file,
        speed=0.5,
        loop=True,

    )