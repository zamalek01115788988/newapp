import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import linregress
import plotly.graph_objects as go
from scipy.interpolate import interp1d

     # Function to calculate TVD using Minimum Curvature Method
def calculate_tvd(data, rkb=0):
    data['TVD'] = 0.0 +rkb # Initialize TVD column
    for i in range(1, len(data)):
        md1, md2 = data.loc[i - 1, 'MD'], data.loc[i, 'MD']
        inc1, inc2 = np.radians(data.loc[i - 1, 'Inclination']), np.radians(data.loc[i, 'Inclination'])
        az1, az2 = np.radians(data.loc[i - 1, 'Azimuth']), np.radians(data.loc[i, 'Azimuth'])
        
        delta_md = md2 - md1
        cos_dogleg = np.cos(inc2) * np.cos(inc1) + np.sin(inc2) * np.sin(inc1) * np.cos(az2 - az1)
        dogleg = np.arccos(np.clip(cos_dogleg, -1, 1))  # Clip to avoid numerical issues
        if dogleg > 1e-6:  # Avoid division by zero
            rf = (2 / dogleg) * np.tan(dogleg / 2)
        else:
            rf = 1.0
        
        delta_tvd = (delta_md / 2) * (np.cos(inc1) + np.cos(inc2)) * rf
        data.loc[i, 'TVD'] = data.loc[i - 1, 'TVD'] + delta_tvd
        data['TVD'] = data['TVD']
    return data
st.title("TVD Calculator using Minimum Curvature Method")
st.header("Upload Directional Survey Data")
survey_file = st.file_uploader("Upload your directional survey data (Excel)", type=[ 'xlsx'])
st.write(survey_file)
if survey_file:
     survey_data = pd.read_excel(survey_file)
     st.write(survey_data)
     well_names = survey_data["Well_Name"].unique()
     st.write(well_names)
     selected_well = st.sidebar.selectbox("Select Well Name", well_names)
     st.write(selected_well)
     survey_data_filtered= survey_data[survey_data["Well_Name"] == selected_well].reset_index(drop=True)
     st.write(survey_data_filtered)

     rkb= st.sidebar.number_input("Enter RKB (ft)", value=0.0, step=1.0)       
     tvd_calc = calculate_tvd(survey_data_filtered,rkb)
     st.write(survey_data_filtered)
