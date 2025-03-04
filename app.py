import streamlit as st
import pandas as pd
import json
import os

print(os.getcwd())

st.title("Lockable Table")

# Define the path to the JSON file where the table data will be stored
data_file_path = "table_data.json"

# Initialize session state if not already
if 'locked_cells' not in st.session_state:
    st.session_state['locked_cells'] = {}

if 'is_locked' not in st.session_state:
    st.session_state['is_locked'] = False

# Function to load data from JSON file
def load_data():
    if os.path.exists(data_file_path):
        with open(data_file_path, "r") as file:
            data = json.load(file)
        return pd.DataFrame(data)
    else:
        # Default data if the file doesn't exist
        return pd.DataFrame({
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

# Function to save data to JSON file
def save_data(data):
    with open(data_file_path, "w") as file:
        json.dump(data.to_dict(orient="records"), file)

# Load the table data when the app starts
st.session_state['table_data'] = load_data()

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

# Function to update table data
def update_table_data(new_data):
    for idx, record in enumerate(new_data):
        for col, value in record.items():
            st.session_state['table_data'].at[idx, col] = value

# Create a copy of the table data and mark the locked cells
locked_table_data = st.session_state['table_data'].copy()

# Render the table only if the table is not locked
if not st.session_state['is_locked']:
    # If the table is not locked, render it as editable
    edited_data = st.data_editor(
        locked_table_data.to_dict(orient='records'),
    )
    # Update the table data in session state when edited
    if edited_data is not None:
        update_table_data(edited_data)
        save_data(st.session_state['table_data'])  # Save updated data to file

else:
    # If the table is locked, display it as read-only (no editing allowed)
    st.dataframe(locked_table_data)  # This will display a static table (read-only)

# Button to lock the table values
if st.button("Lock Table Values"):
    lock_cells()  # Lock the cells
    st.session_state['is_locked'] = True  # Mark the table as locked
    st.success("Table values locked successfully! The values cannot be edited now.")
    save_data(st.session_state['table_data'])  # Save data after locking
