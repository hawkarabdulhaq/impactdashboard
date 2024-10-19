import pandas as pd
import streamlit as st

# Define the URL to your CSV file (which will be hosted on GitHub or another source)
CSV_URL = "https://raw.githubusercontent.com/<your-username>/<your-repository>/main/path-to-your-csv-file.csv"

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
            "Deleverable": last_row["Deleverable"],
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

# Streamlit Page Layout
st.title("Scan Your Releafs' Token")

# Add a button to show token details
if st.button("Show Token Details"):
    display_token_details()
