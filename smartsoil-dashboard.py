#necessary libraries
import streamlit as st
import plotly.express as px
import pandas as pd 
import os
import warnings
warnings.filterwarnings('ignore')


st.set_page_config(page_title="Smart Soil Dashboard", page_icon=":chart_with_upwards_trend:",layout="wide")
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


#creating the charts
category_df= filtered_df.groupby(by = ["Category"], as_index=False)["Rainfall(mm)"].sum()

with col1:
    st.subheader("Category-wise rainfall")
    fig = px.bar(category_df, x= "Category", y= "Rainfall(mm)", text = ['{:,.2f}'.format(x) for x in category_df["Rainfall(mm)"]],
                 template = "seaborn")
    st.plotly_chart(fig, use_container_width=True, height = 200)

with col2:
    st.subheader("Crop wise Rainfall")
    fig = px.pie(filtered_df, values = "Rainfall(mm)", names ="Crop", hole = 0.5 )
    fig.update_traces(text = filtered_df["Crop"], textposition ="outside")
    st.plotly_chart(fig, use_container_width=True, height = 200)

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
        
#time series analysis month-year(extract month)
#filtered_df["Test Date"] = filtered_df["Test Date"].dt.to_period("M")
#st.subheader('Time series analysis')

#linechart = pd.DataFrame(filtered_df.groupby(filtered_df["Test Date"].dt.strftime("%Y : %b"))["Rainfall(mm)"].sum()).reset_index()
#fig2 = px.line(linechart, x = "Test Date", y = "Rainfall(mm)", labels={"Rainfall":"Rainfall(mm)"}, height = 500, width = 1000, template = "gridon")
#st.plotly_chart(fig2, use_container_width= True)


# User interface for selecting factors 
st.subheader("Factor Comparison")
selected_factors = st.multiselect("Select Factors to Compare with Rain:", df.columns[1:], default=["Temperature"]) 
columns = st.columns(len(selected_factors))

# Plot rain against each selected factor in separate columns
for i, factor in enumerate(selected_factors):
  with columns[i]:
    fig = px.bar(df, x=factor, y="Rainfall(mm)", title=f"Rainfall(mm) vs. {factor}")
    st.plotly_chart(fig)

selected_factors = st.multiselect("Select Factors to Compare:", df.columns[1:])  # Exclude Crop column

# Handling potential selection errors
if len(selected_factors) < 2:
  st.error("Please select at least two factors for comparison.")
  st.stop()  # Stop execution if not enough factors are selected


columns = st.columns(len(selected_factors) - 1)  

# Plot each factor against the first selected factor 
reference_factor = selected_factors[0]
for i, factor in enumerate(selected_factors[1:]):  
  with columns[i]:
    fig = px.bar(df, x=factor, y=reference_factor, title=f"{factor} vs. {reference_factor}")
    st.plotly_chart(fig)


st.subheader("Environmental Stats")
# User interface for selecting factors 
selected_factors_env = st.multiselect("Select Environmental Factors:", ["Temperature", "Humidity (%)", "Rainfall(mm)"])

# Handle potential selection errors (optional)
if not selected_factors_env:
  st.error("Please select at least one environmental factor.")
  st.stop()

# Line Charts: Environmental factors over time
dates = pd.to_datetime(df['Test Date'])
st.subheader("Line Charts: Environmental Factors Over Time")
fig_env = px.line(df, x="Test Date", y=selected_factors_env, title="Environmental Factors Over Time", height = 500, width = 1200, template = "gridon")
st.plotly_chart(fig_env)
#######


