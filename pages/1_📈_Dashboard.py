#necessary libraries
import streamlit as st
import plotly.express as px
import pandas as pd 
import os
import warnings
warnings.filterwarnings('ignore')


st.set_page_config(page_title="TerraScope", page_icon=":chart_with_upwards_trend:",layout="wide")
#setting title
st.title (":chart_with_upwards_trend: Smart-Soil Dashboard") 
st.markdown('<style>div.block-container{padding-top:1rem}</style>', unsafe_allow_html=True)


#browse and upload files
fl= st.file_uploader(":file_folder: Upload a file",type=(["csv"]))
if fl is not None:
    filename=fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding="ISO-8859-1")
else:
    os.chdir(r"C:\Users\ashle\OneDrive\Документы\smart_soil")
    df = pd.read_csv("crop_data.csv", encoding="ISO-8859-1")

#####################################################

#create a date picker object
col1,col2 = st.columns((2))
df['Test Date']= pd.to_datetime(df["Test Date"])

startDate = pd.to_datetime(df['Test Date']).min()
endDate = pd.to_datetime(df['Test Date']).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Test Date"] >= date1) & (df["Test Date"] <= date2)].copy()

#filter pane for crops
############

st.sidebar.header("Choose a filter:")
#for crop type
crop_type = st.sidebar.multiselect("Pick your Crop type:", df["Category"].unique())
if not crop_type:
    df2= df.copy()
else:
    df2 = df[df["Category"].isin(crop_type)]
#for crop
crop = st.sidebar.multiselect("Pick your Crop:", df2["Crop"].unique())
if not crop:
    df3= df2.copy()
else:
    df3 = df2[df2["Crop"].isin(crop)]

#applying filters

if not crop_type and not crop:
    filtered_df = df
elif not crop:
    filtered_df = df[df["Category"].isin(crop_type)]
elif crop:
    filtered_df = df3[df3["Crop"].isin(crop)]
else:
    filtered_df = df3[df3["Category"].isin(crop_type) & df3["Crop"].isin(crop)]

###################################################
#creating the charts

crops_df = df['Crop'].unique()  # Get unique crops

def show_crops_in_category(selected_category):
    crops_list = df[df['Category'] == selected_category]['Crop'].tolist()
    crops_text = "\n".join(crops_list)  # Create a string with list items separated by newlines
    st.tooltip(f"Crops in '{selected_category}':\n{crops_text}")  # Set tooltip text

with col1:
    # User interface for selecting factors 
    st.subheader("Category Comparison")
    selected_factors = st.multiselect("Select Factors to categorize:", df.columns[1:], default=["Temperature"]) 
    if selected_factors:
        columns = st.columns(len(selected_factors))
        colors = px.colors.qualitative.Plotly

        # Plot category against each selected factor in separate columns
        for factor in selected_factors:
            fig = px.bar(df, x=factor, y="Category", title=f"Total {factor} per category", color=factor, color_discrete_sequence=colors[:len(selected_factors)])
            st.plotly_chart(fig, use_container_width= True)
    else:
        st.warning("Please select at least one factor for comparison.")

    


category_df= filtered_df.groupby(by = ["Category"], as_index=False)[selected_factors].sum()


with col2:
    st.subheader("Crop wise comparison")
    selected_crop_factors = st.multiselect("Select Factors to categorize crop:", df.columns[1:], default = ['Rainfall(mm)'])

    # Check if any factors are selected
    if selected_crop_factors:
        crop_df = filtered_df.groupby(by=["Crop"], as_index=False)[selected_crop_factors].sum()

        # Plot each selected factor in separate pie charts
        for factor in selected_crop_factors:
            # Check if the current factor is a valid column name
            if factor in crop_df.columns:
                fig = px.pie(crop_df, values=factor, names="Crop", hole=0.5, title=f"Total {factor} per Crop")
                fig.update_traces(text=crop_df["Crop"], textposition="outside")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"Selected factor '{factor}' not found in data. Skipping...")

    else:
        st.warning("Please select at least one factor for comparison.")

#Download charted data
cm1,cm2 = st.columns(2)
with cm1:
    with st.expander("Category View Data"):
        st.write(category_df)
        cat_csv=category_df.to_csv(index = False).encode("utf8")
        st.download_button("Download Data", data= cat_csv, file_name="Category Data.csv", mime= "csv/txt",
                           help = "Click to download data as CSV" )

with cm2:
    with st.expander("Crop View Data"):
        crop_type = filtered_df.groupby(by ="Crop", as_index=False)["Rainfall(mm)"].sum()
        st.write(crop_type)
        reg_csv=crop_type.to_csv(index = False).encode("utf8")
        st.download_button("Download Data", data= reg_csv, file_name="crop Data.csv", mime= "csv/txt",
                           help = "Click to download data as CSV" )
        
#################################################################################

# User interface for selecting factors 

st.subheader("Factor Comparison")
selected_factors = st.multiselect("Select Factors to Compare with Rain:", df.columns[1:], default=["Temperature"]) 
columns = st.columns(len(selected_factors))

# Plot rain against each selected factor
for factor in selected_factors:
    fig = px.bar(df, x=factor, y="Rainfall(mm)", title=f"Rainfall(mm) vs. {factor}")
    st.plotly_chart(fig, use_container_width= True)

#####################################################
selected_factors = st.multiselect("Select Factors to Compare:", df.columns[1:])  # Exclude Crop column

# Handling potential selection errors
if len(selected_factors) < 2:
  st.warning("Please select at least two factors for comparison.")
  st.stop()  # Stop execution if not enough factors are selected


columns = st.columns(len(selected_factors) - 1)  

# Plot each factor against the first selected factor 
reference_factor = selected_factors[0]
for i, factor in enumerate(selected_factors[1:]):  
  with columns[i]:
    fig = px.bar(df, x=factor, y=reference_factor, title=f"{factor} vs. {reference_factor}")
    st.plotly_chart(fig, use_container_width= True)

##############################################
st.subheader("Environmental Stats")
# User interface for selecting factors 
selected_factors_env = st.multiselect("Select Environmental Factors:", ["Temperature", "Humidity (%)", "Rainfall(mm)"])

# Handle potential selection errors (optional)
if not selected_factors_env:
  st.warning("Please select at least one environmental factor.")
  st.stop()

# Line Charts: Environmental factors over time
dates = pd.to_datetime(df['Test Date'])
st.subheader("Line Charts: Environmental Factors Over Time")
fig_env = px.line(df, x="Test Date", y=selected_factors_env, title="Environmental Factors Over Time", height = 500, width = 1200, template = "gridon")
st.plotly_chart(fig_env, use_container_width= True)
#######


