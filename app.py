import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from fastkml import kml

# Define the URL to your CSV file hosted on GitHub
CSV_URL = "https://raw.githubusercontent.com/hawkarabdulhaq/impactdashboard/main/impactdata.csv"

def display_token_details():
    try:
        # Directly read the CSV data from the URL using Pandas
        df = pd.read_csv(CSV_URL)

        if df.empty:
            st.error("CSV file is empty.")
            return

        # Extract the last row from the DataFrame
        last_row = df.iloc[-1]
        parameters = {
            "Latitude": last_row["Latitude"],
            "Longitude": last_row["Longitude"],
            "Type of Token": last_row["Type of Token"],
            "Description": last_row["description"],
            "External URL": last_row["external_url"],
            "Starting Project": last_row["Starting Project"],
            "Unit": last_row["Unit"],
            "Deliverable": last_row["Deleverable"],
            "Years Duration": last_row["Years_Duration"],
            "Impact Type": last_row["Impact Type"],
            "SDGs": last_row["SDGs"],
            "Implementer Partner": last_row["Implementer Partner"],
            "Internal Verification": last_row["Internal Verification"],
            "Local Verification": last_row["Local Verification"],
            "Imv Document": last_row["Imv_Document"]
        }

        # Display the token information in a Streamlit table
        st.write("### Token Information:")
        st.table(pd.DataFrame.from_dict(parameters, orient='index', columns=['Value']).reset_index().rename(columns={"index": "Parameter"}))
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def display_basic_map():
    # Read the CSV data
    df = pd.read_csv(CSV_URL)
    
    # Rename columns to lowercase for Streamlit compatibility
    df.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'}, inplace=True)
    
    # Basic Streamlit map visualization using Latitude/Longitude
    st.write("### Basic Map of Project Locations:")
    st.map(df[['lat', 'lon']])

def display_detailed_map():
    st.write("### Detailed Map with Folium:")

    # Read the CSV data
    df = pd.read_csv(CSV_URL)

    # Create a Folium map centered on the first project
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=10)

    # Add project locations to the map
    for i, row in df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['description']}<br><a href='{row['KML']}' target='_blank'>View KML File</a>",
        ).add_to(m)

    # Display the Folium map in Streamlit
    st_folium(m, width=700, height=500)

# Streamlit Page Layout
st.title("Scan Your Releafs' Token")

# Display basic map
display_basic_map()

# Add a button to show token details
if st.button("Show Token Details"):
    display_token_details()

# Display detailed map
display_detailed_map()
