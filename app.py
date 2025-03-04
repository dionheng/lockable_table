import streamlit as st
import pandas as pd
import json
import os

st.title("Lockable Table with Visual Indicators")

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
        try:
            with open(data_file_path, "r") as file:
                saved_data = json.load(file)
                
                # Load table data and locked cells separately
                table_data = pd.DataFrame(saved_data.get("table_data", []))
                st.session_state['locked_cells'] = saved_data.get("locked_cells", {})
                return table_data
        except json.JSONDecodeError:
            st.warning("Corrupted JSON file. Loading default table.")
    
    # Load default data if the file is missing or corrupted
    return pd.DataFrame({
        'Number': ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
        'OMAT No.': ["OMat 4-70", "OMat 1001A", "OMat 4-51", "OMat 8-121", "OMat 150", "OMat 4-43", "OMat 4/71", "OMat 4/74", "OMat 4/76"],
        'Description': ["Air Dry, Molybdenum Disulphide Dry Film Lubricant (1L)", "Plus gas, Dry Film Lubricant (1L)", "Molykote D321R", "Loctite 641", "Acetone", "Molydisulphide Lubricant", "Rapid Re-lube Kit T700", "Rapid Re-lube Kit T800", "Rapid Re-lube Kit T800"],
        'Batch No.': ["", "", "", "", "", "", "", "", ""],
        'Expiry Date': ["", "", "", "", "", "", "", "", ""],
    })


# Function to save data and locked cells to JSON file
def save_data(data):
    with open(data_file_path, "w") as file:
        json.dump({
            "table_data": data.to_dict(orient="records"),
            "locked_cells": st.session_state['locked_cells']
        }, file)


# Load the table data when the app starts
st.session_state['table_data'] = load_data()

# Function to lock pre-filled cells
def lock_prefilled_cells():
    for idx, data in st.session_state['table_data'].iterrows():
        for col, value in data.items():
            if (idx, col) not in st.session_state['locked_cells'] and value.strip():
                st.session_state['locked_cells'][(idx, col)] = value

# Lock pre-filled cells on page load
lock_prefilled_cells()

# Function to style locked cells
def highlight_locked(val, row, col):
    if (row, col) in st.session_state['locked_cells']:
        return 'background-color: lightgray; color: gray;'
    return ''


# Function to render the styled DataFrame
def render_styled_table(df):
    styled_df = df.style.apply(
        lambda row: [highlight_locked(val, row.name, col) for col, val in row.items()],
        axis=1
    )
    st.dataframe(styled_df)


# Function to update table data
def update_table_data(new_data):
    for idx, record in enumerate(new_data):
        for col, value in record.items():
            st.session_state['table_data'].at[idx, col] = value


# Render the table
if not st.session_state['is_locked']:
    # Editable table if unlocked
    edited_data = st.data_editor(
        st.session_state['table_data'].to_dict(orient='records'),
        disabled=[st.session_state['locked_cells'].get((i, col)) is not None for i in range(len(st.session_state['table_data'])) for col in st.session_state['table_data'].columns]
    )
    
    # Update and save data on edit
    if edited_data is not None:
        update_table_data(edited_data)
        save_data(st.session_state['table_data'])
else:
    # Read-only view if locked
    render_styled_table(st.session_state['table_data'])


# Button to lock the table values
if st.button("Lock Table Values"):
    lock_prefilled_cells()
    st.session_state['is_locked'] = True
    st.success("Table values locked successfully! The values cannot be edited now.")
    save_data(st.session_state['table_data'])

# Button to unlock the table
if st.button("Unlock Table Values"):
    st.session_state['is_locked'] = False
    st.success("Table unlocked! You can now edit the values again.")

    # Refresh the lock status without clearing locked cells
    save_data(st.session_state['table_data'])


st.info("Filled cells are automatically locked on page refresh, and locked cells are grayed out.")

# Debug view
if st.checkbox("Show Locked Cells (Debug)"):
    st.write(st.session_state['locked_cells'])


# 🚀 Let me know if you want me to refine anything else! 🚀
