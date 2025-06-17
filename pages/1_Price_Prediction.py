import streamlit as st
import pickle
import pandas as pd

from downloader import download_file_from_google_drive


with open("price_predictor_data.pkl", "rb") as file:
    smartphones_df = pickle.load(file)

st.title("Welcome to Smartphone Price Prediction Module")


cols = ['processor_brand', 'brand', 'screen_type', 'spec_score_cat']


st.header("Enter the Desired Specifications")

# smartphone brand
brand_list = sorted(smartphones_df['brand'].unique())
brand = st.selectbox("Select Smartphone Brand", brand_list)

# processor brand
processor_brand_list = sorted(smartphones_df['processor_brand'].unique())
processor_brand = st.selectbox('Processor Brand', processor_brand_list)

# clock speed
clock_speed = float(st.slider(
    label = "Enter Clock Speed (GHz)",
    min_value = 1.0,
    max_value = 5.0,
    value = 2.0,
    step = 0.1
))

# NFC
has_nfc = st.selectbox("NFC Required", ["Yes", "No"])
has_nfc = 1 if has_nfc == "Yes" else 0

# Connectivity
has_5g = st.selectbox("Choose Connectivity Type", ["5G", "4G"])
has_5g = 1 if has_5g == "5G" else 0

# RAM
ram_gb = float(st.selectbox("Choose RAM Capacity (GB)", sorted(list(smartphones_df['ram_gb'].unique()))))

# ROM
rom_gb = float(st.selectbox("Choose ROM Capacity (GB)", sorted(list(smartphones_df['rom_gb'].unique()))))

# Battery Capacity
battery_capacity_mah = float(st.number_input("Enter Battery Capacity (mAh)"))

# fast charging
fast_charging_required = st.selectbox("Fast Charging Required?", ["Yes", "No"])
if fast_charging_required == "Yes":
    fast_charging_watt = float(st.number_input("Enter Fast Charging Capacity (Watt)"))
else:
    fast_charging_watt = 0.0

# display size
screen_size_inch = float(st.number_input("Enter Display Size (inch)"))

# foldable display
foldable_display = st.selectbox("Foldable Display Required?", ["Yes", "No"])
foldable_display = 1 if foldable_display == "Yes" else 0

# display_refresh_rate
display_refresh_rate = int(st.selectbox("Choose Display Refresh Rate (Hz)",
                                          list(smartphones_df['display_refresh_rate'].unique())))

# ppi
ppi = float(st.number_input("Enter PPI"))

# num_rear_cameras
num_rear_cameras = float(st.selectbox("Enter Number of Rear Cameras", [1, 2, 3, 4]))

# rear_primary_camera_mp
rear_primary_mp = float(st.number_input("Enter Rear Primary Camera Capacity (MP)"))

# front_primary_camera_mp
front_primary_mp = float(st.number_input("Enter Front Primary Camera Capacity (MP)"))

# screen_type
screen_type = st.selectbox("Choose Screen Type", ['AMOLED', 'LCD', 'OLED', 'OTHER', 'SUPER AMOLED'])

# spec_score_cat
spec_score_cat = st.selectbox("Select Specs Level (Low <74, Mid 74–81, High >81)", ['High', 'Low', 'Mid'])


if st.button('Predict'):
    # Downloading price predictor pipeline from google drive
    download_file_from_google_drive("1SlGyFxIr2mndxyV4t4A3vG-jykPYYWOe", "price_predictor_pipeline.pkl")
    with open("price_predictor_pipeline.pkl", "rb") as file:
        pipeline = pickle.load(file)

    # form a dataframe
    data = [[processor_brand, clock_speed, has_nfc, has_5g, ram_gb, rom_gb, brand, battery_capacity_mah,
             fast_charging_watt, screen_size_inch, foldable_display, display_refresh_rate, ppi, num_rear_cameras,
             rear_primary_mp, front_primary_mp, screen_type, spec_score_cat]]
    columns = ['processor_brand', 'clock_speed', 'has_nfc', 'has_5g', 'ram_gb', 'rom_gb', 'brand', 'battery_capacity_mah',
             'fast_charging_watt', 'screen_size_inch', 'foldable_display', 'display_refresh_rate', 'ppi', 'num_rear_cameras',
             'rear_primary_mp', 'front_primary_mp', 'screen_type', 'spec_score_cat']

    # Convert to DataFrame
    input_df = pd.DataFrame(data, columns=columns)

    # predict
    price = pipeline.predict(input_df)[0]

    # display
    st.markdown(f"### Estimated Price: ₹ {round(price, 2)}")



