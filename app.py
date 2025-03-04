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
def export_to_google_sheets(sheet_url):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
        client = gspread.authorize(creds)
        
        sheet = client.open_by_url(sheet_url).sheet1
        
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
st.data_editor(
    st.session_state['table_data'].to_dict(orient='records'),  # Convert to list of records
    disabled=[(idx, col) for (idx, col) in st.session_state['locked_cells'].keys()],
    height=(len(st.session_state['table_data']) * 35) + 50,  # Dynamic height
    use_container_width=True  # Dynamic width
)

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
