import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Lockable Table")

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

# Function to lock pre-filled cells
def lock_prefilled_cells():
    for idx, data in st.session_state['table_data'].iterrows():
        for col, value in data.items():
            if (idx, col) not in st.session_state['locked_cells'] and value.strip():
                st.session_state['locked_cells'][(idx, col)] = value

# Lock pre-filled cells when the app starts
lock_prefilled_cells()

# Function to lock cells
def lock_cells():
    for idx, data in st.session_state['table_data'].iterrows():
        for col, value in data.items():
            if (idx, col) not in st.session_state['locked_cells'] and value.strip():
                st.session_state['locked_cells'][(idx, col)] = value

# Create a copy of the table data and mark the locked cells
locked_table_data = st.session_state['table_data'].copy()

# Mark locked cells in the dataframe
for (idx, col) in st.session_state['locked_cells'].keys():
    locked_table_data.at[idx, col] = f"Locked: {st.session_state['locked_cells'][(idx, col)]}"

# Render the table with dynamic height and width and mark the locked cells as read-only
st.data_editor(
    locked_table_data.to_dict(orient='records'),
    disabled_columns={col: True for _, col in st.session_state['locked_cells'].keys()},
)

if st.button("Lock Table Values"):
    lock_cells()
    st.success("Table values locked successfully! The values cannot be edited now.")
