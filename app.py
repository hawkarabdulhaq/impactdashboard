import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from fastkml import kml
from shapely.geometry import Polygon
import requests
import base64

# Define the URL to your CSV file hosted on GitHub 
CSV_URL = "https://raw.githubusercontent.com/hawkarabdulhaq/impactdashboard/main/impactdata.csv"

def load_image(image_path):
    """Load an image and convert it to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

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

        # Prepare the display DataFrame
        df_display = pd.DataFrame.from_dict(parameters, orient='index', columns=['Value']).reset_index().rename(columns={"index": "Parameter"})

        # Load SDG icons and replace text with image tags
        sdg_icons = {
            "SDG3": load_image("image/SDG3.jpg"),
            "SDG6": load_image("image/SDG6.jpg"),
            "SDG7": load_image("image/SDG7.jpg"),
            "SDG11": load_image("image/SDG11.jpg"),
            "SDG13": load_image("image/SDG13.jpg"),
        }

        # Replace SDG texts with HTML image tags
        sdg_images_html = []
        for sdg, img_data in sdg_icons.items():
            if sdg in last_row["SDGs"]:
                sdg_images_html.append(f'<img src="data:image/jpeg;base64,{img_data}" alt="{sdg}" width="50" height="50">')

        # Combine SDG images into a single string
        sdg_images_str = ' '.join(sdg_images_html)
        df_display.loc[df_display["Parameter"] == "SDGs", "Value"] = sdg_images_str

        # Load and replace "Hasar Organization" with the logo
        logo_data = load_image("image/Hasar_Organization.jpg")
        df_display.loc[df_display["Parameter"] == "Implementer Partner", "Value"] = f'<img src="data:image/jpeg;base64,{logo_data}" alt="Hasar Organization" width="50" height="50">'

        # Display the token information in a Streamlit table
        st.write("### Token Information:")
        st.markdown(df_display.to_html(escape=False), unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def parse_kml(kml_url):
    """Parses the KML file and extracts polygon data."""
    if "drive.google.com" in kml_url:
        # Convert the Google Drive link to a direct download link
        file_id = kml_url.split("/d/")[1].split("/")[0]
        kml_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    # Download the KML file
    response = requests.get(kml_url)

    # Check if the response is valid
    if response.status_code != 200:
        st.error("Failed to download KML file.")
        return []

    kml_data = response.text

    try:
        k = kml.KML()
        k.from_string(kml_data)

        polygons = []
        for feature in list(k.features()):
            for placemark in list(feature.features()):
                if isinstance(placemark.geometry, Polygon):
                    polygons.append(placemark.geometry)

        return polygons
    except Exception as e:
        st.error(f"An error occurred while parsing the KML file: {str(e)}")
        return []

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
