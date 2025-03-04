import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.title("Lockable Table with Google Sheets Export")

# Initialize session state if not already
if 'locked_cells' not in st.session_state:
    st.session_state['locked_cells'] = {}

if 'table_data' not in st.session_state:
    st.session_state['table_data'] = pd.DataFrame({
        'Column 1': ["", "", ""],
        'Column 2': ["", "", ""],
        'Column 3': ["", "", ""]
    })

if 'timestamps' not in st.session_state:
    st.session_state['timestamps'] = {}

# Function to lock cells and timestamp
def lock_cells():
    for idx, data in st.session_state['table_data'].iterrows():
        if idx not in st.session_state['locked_cells']:
            st.session_state['locked_cells'][idx] = data.to_dict()
            st.session_state['timestamps'][idx] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Function to export locked table data to Google Sheets
def export_to_google_sheets(sheet_url):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
        client = gspread.authorize(creds)
        
        sheet = client.open_by_url(sheet_url).sheet1
        
        # Clear existing data and write new data
        sheet.clear()
        data = pd.DataFrame.from_dict(st.session_state['locked_cells'], orient='index')
        data['Timestamp'] = [st.session_state['timestamps'].get(idx, '') for idx in data.index]
        
        # Convert DataFrame to list of lists and update the sheet
        sheet.update([data.columns.values.tolist()] + data.values.tolist())
        
        st.success("Data exported to Google Sheets successfully!")
    except Exception as e:
        st.error(f"Failed to export data to Google Sheets: {e}")

# Render the table
edited_df = st.data_editor(st.session_state['table_data'], disabled=list(st.session_state['locked_cells'].keys()))

st.session_state['table_data'] = edited_df

# Google Sheet URL input
google_sheet_url = st.text_input("Enter your Google Sheet URL")

if st.button("Lock Filled Cells and Export to Google Sheets"):
    lock_cells()
    if google_sheet_url.strip():
        export_to_google_sheets(google_sheet_url)
    else:
        st.warning("Please enter a valid Google Sheet URL")

st.info("This app works well on mobile devices via the Streamlit web interface.")

# Run with: streamlit run app.py
# Let me know if you’d like me to refine anything or add new features! 🚀
