import os
import json
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

st.title("Lockable Table with Google Sheets Export")

# Load environment variables from .env file (if you have it)
load_dotenv()

# Initialize session state if not already
if 'locked_cells' not in st.session_state:
    st.session_state['locked_cells'] = {}

if 'table_data' not in st.session_state:
    st.session_state['table_data'] = pd.DataFrame({
        'Number': ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
        'OMAT No.': ["OMat 4-70", "OMat 1001A", "OMat 4-51", "OMat 8-121", "OMat 150", "OMat 4-43", "OMat 4/71", "OMat 4/74", "OMat 4/76"],
        'Description': ["Air Dry, Molybdenum\nDisulphide\nDry Film Lubricant (1L)", "Plus gas, Dry Film Lubricant (1L)\nEnamel (1L)", "Molykote\nD321R", "Loctite 641\nBearing Fit", "Acetone", "Molydisulphide\nDry Film Lubricant", "Rapid Re-lube Kit T700", "Rapid Re-lube Kit T800", "Rapid Re-lube Kit T800"],
        'Minimum Stock Level\nMaximum Allowable\nVolume': ["10 Bottles (0.125 litre/bottle)\n20 Bottles", "", "", "", "", "", "", "", ""],
        'Batch No.': ["", "", "", "", "", "", "", "", ""],
        'Expiry Date\n(DD/MM/YYYY)': ["", "", "", "", "", "", "", "", ""],
        'Quantity\n(Week 1)': ["", "", "", "", "", "", "", "", ""],
        'Quantity\n(Week 2)': ["", "", "", "", "", "", "", "", ""],
        'Quantity\n(Week 3)': ["", "", "", "", "", "", "", "", ""],
        'Quantity\n(Week 4)': ["", "", "", "", "", "", "", "", ""],
    })

if 'timestamps' not in st.session_state:
    st.session_state['timestamps'] = {}

# Function to lock pre-filled cells
def lock_prefilled_cells():
    for idx, data in st.session_state['table_data'].iterrows():
        for col, value in data.items():
            if (idx, col) not in st.session_state['locked_cells'] and value.strip():
                st.session_state['locked_cells'][(idx, col)] = value
                st.session_state['timestamps'][(idx, col)] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Lock pre-filled cells when the app starts
lock_prefilled_cells()

# Function to lock cells and timestamp
def lock_cells():
    for idx, data in st.session_state['table_data'].iterrows():
        for col, value in data.items():
            if (idx, col) not in st.session_state['locked_cells'] and value.strip():
                st.session_state['locked_cells'][(idx, col)] = value
                st.session_state['timestamps'][(idx, col)] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Function to export locked table data to Google Sheets
def export_to_google_sheets():
    try:
        # Retrieve the Google Sheets credentials from the environment variable
        service_account_json = os.getenv('GOOGLE_SHEET_CREDENTIALS')

        # Check if the environment variable is set
        if service_account_json is None:
            raise ValueError("The GOOGLE_SHEET_CREDENTIALS environment variable is not set.")

        # Parse the JSON string into a dictionary
        credentials_dict = json.loads(service_account_json)

        # Define the Google Sheets scope
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

        # Use the credentials dictionary to create the credentials object
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)

        # Authorize gspread client with credentials
        client = gspread.authorize(creds)
        
        # Hardcoded Google Sheets key
        sheet_key = "1aBcDeFgHiJkLmNoPqRsTUVwXyz1234567"  # Replace with your actual Google Sheets key
        
        # Open the sheet by key
        sheet = client.open_by_key(sheet_key).sheet1
        
        # Clear existing data and write new data
        sheet.clear()
        locked_data = {}
        
        for (idx, col), value in st.session_state['locked_cells'].items():
            if idx not in locked_data:
                locked_data[idx] = {}
            locked_data[idx][col] = value
            locked_data[idx]['Timestamp'] = st.session_state['timestamps'].get((idx, col), '')
        
        data = pd.DataFrame.from_dict(locked_data, orient='index')
        
        # Convert DataFrame to list of lists and update the sheet
        sheet.update([data.columns.values.tolist()] + data.fillna(" ").values.tolist())
        
        st.success("Data exported to Google Sheets successfully!")
    except Exception as e:
        st.error(f"Failed to export data to Google Sheets: {e}")

# Render the table with dynamic height and width
table_data = st.session_state['table_data'].copy()
for (idx, col), value in st.session_state['locked_cells'].items():
    # Mark locked cells (for display)
    if value.strip():
        table_data.at[idx, col] = f"LOCKED: {value}"

# Render the editable table
edited_data = st.data_editor(
    table_data.to_dict(orient='records'),
    height=350,
)

# Automatically submit to Google Sheets
if st.button("Export to Google Sheets"):
    lock_cells()
    export_to_google_sheets()
