import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from fastkml import kml
from shapely.geometry import Polygon
import requests

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

def parse_kml(kml_url):
    """Parses the KML file and extracts polygon data."""
    # Download the KML file
    kml_data = requests.get(kml_url).text

    k = kml.KML()
    k.from_string(kml_data)

    polygons = []
    for feature in list(k.features()):
        for placemark in list(feature.features()):
            if isinstance(placemark.geometry, Polygon):
                polygons.append(placemark.geometry)

    return polygons

def display_detailed_map():
    st.write("### Detailed Map with Polygon Data from KML:")

    # Read the CSV data
    df = pd.read_csv(CSV_URL)

    # Get the KML URL from the CSV file (assuming it's the last row in your dataset)
    kml_url = df.iloc[-1]["KML"]
    
    if not kml_url:
        st.error("No KML URL found in the CSV file.")
        return

    # Create a Folium map centered on the first project
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12)

    # Add project locations to the map
    for i, row in df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['description']}<br><a href='{row['KML']}' target='_blank'>View KML File</a>",
        ).add_to(m)

    # Parse KML and add polygons to the map
    polygons = parse_kml(kml_url)
    
    for polygon in polygons:
        # Convert shapely polygon object to a list of coordinates
        coords = [(pt[1], pt[0]) for pt in polygon.exterior.coords]  # Lat, Lon format
        folium.Polygon(locations=coords, color='blue', fill=True, fill_opacity=0.4).add_to(m)

    # Display the Folium map in Streamlit
    st_folium(m, width=700, height=500)

# Streamlit Page Layout
st.title("Scan Your Releafs' Token")

# Add a button to show token details
if st.button("Show Token Details"):
    display_token_details()

# Display detailed map with polygons
display_detailed_map()
