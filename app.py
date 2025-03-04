import streamlit as st
import pandas as pd
import json
import os

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
        return pd.DataFrame({
            'Number': ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
            'OMAT No.': ["OMat 4-70", "OMat 1001A", "OMat 4-51", "OMat 8-121", "OMat 150", "OMat 4-43", "OMat 4/71", "OMat 4/74", "OMat 4/76"],
            'Description': ["Air Dry, Molybdenum\nDisulphide\nDry Film Lubricant (1L)", "Plus gas, Dry Film Lubricant (1L)\nEnamel (1L)", "Molykote\nD321R", "Loctite 641\nBearing Fit", "Acetone", "Molydisulphide\nDry Film Lubricant", "Rapid Re-lube Kit T700", "Rapid Re-lube Kit T800", "Rapid Re-lube Kit T800"],
            'Minimum Stock Level\nMaximum Allowable\nVolume': ["10 Bottles (0.125 litre/bottle)/20 Bottles", "1 Can (0.125 litre/can)/ 1 Can", "10 Bottles (0.4 litre/can)/ 20 Bottles", "1 Bottle (3.5ml/bottle)/ 1 Bottle", "2 Bottles (5 litre/bottle)/ 20 Bottles", "05 Cans (1 litre/can)/ 20 Bottles", "1 Set/ 1 Set", "1 Set/ 1 Set", "1 Set/ 1 Set"],
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

# Function to lock pre-filled cells
def lock_prefilled_cells():
    for idx, data in st.session_state['table_data'].iterrows():
        for col, value in data.items():
            if (idx, col) not in st.session_state['locked_cells'] and value.strip():
                st.session_state['locked_cells'][(idx, col)] = value

# Function to lock cells
def lock_cells():
    for idx, data in st.session_state['table_data'].iterrows():
        for col, value in data.items():
            if (idx, col) not in st.session_state['locked_cells'] and value.strip():
                st.session_state['locked_cells'][(idx, col)] = value

# Function to unlock the table
def unlock_table():
    st.session_state['is_locked'] = False
    st.info("Table unlocked! You can now edit the values again.")

# Function to update table data
def update_table_data(new_data):
    for idx, record in enumerate(new_data):
        for col, value in record.items():
            st.session_state['table_data'].at[idx, col] = value

# Function to style locked cells as bold
def style_locked_cells(df):
    styled_df = df.copy()
    for idx, col in styled_df.iteritems():
        for row_idx, value in col.items():
            if (row_idx, idx) in st.session_state['locked_cells']:
                styled_df.at[row_idx, idx] = f"**{value}**"
    return styled_df

# Load the table data when the app starts
st.session_state['table_data'] = load_data()
lock_prefilled_cells()

# Create a copy of the table data and mark the locked cells
styled_table_data = style_locked_cells(st.session_state['table_data'])

# Render the table
if not st.session_state['is_locked']:
    edited_data = st.data_editor(
        styled_table_data.to_dict(orient='records'),
    )
    if edited_data is not None:
        update_table_data(edited_data)
        save_data(st.session_state['table_data'])
else:
    st.dataframe(styled_table_data)

# Button to lock the table values
if st.button("Lock Table Values"):
    lock_cells()
    st.session_state['is_locked'] = True
    st.success("Table values locked successfully! The values cannot be edited now.")
    save_data(st.session_state['table_data'])

# Button to unlock the table
if st.button("Unlock Table Values"):
    unlock_table()
    st.success("Table unlocked! You can now edit the values again.")
