import streamlit as st

import pandas as pd

import json

import os

 

st.title("Fan Blade Cell - Flammable Omats Weekly Checklist")

 

# Define the path to the JSON file where the table data will be stored

data_file_path = "table_data.json"

lock_file_path = "locked_cells.json"

 

# Initialize session state variables

if "is_locked" not in st.session_state:

    st.session_state["is_locked"] = False

 

if "table_data" not in st.session_state:

    st.session_state["table_data"] = None

 

if "locked_cells" not in st.session_state:

    st.session_state["locked_cells"] = {}

 

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

 

# Function to load locked cells from file

def load_locked_cells():

    if os.path.exists(lock_file_path):

        with open(lock_file_path, "r") as file:

            return json.load(file)

    return {}

 

# Function to save locked cells

def save_locked_cells():

    with open(lock_file_path, "w") as file:

        json.dump(st.session_state["locked_cells"], file)

 

# Load the table data and locked cells when the app starts

if st.session_state["table_data"] is None:

    st.session_state["table_data"] = load_data()

 

st.session_state["locked_cells"] = load_locked_cells()

 

# Function to lock filled cells and persist them

def lock_cells():

    for idx, row in st.session_state["table_data"].iterrows():

        for col, value in row.items():

            if value.strip():  # Lock only if cell is not empty

                st.session_state["locked_cells"][(idx, col)] = value

    save_locked_cells()

    st.session_state["is_locked"] = True

    st.success("Table values locked successfully! The values cannot be edited now.")

 

# Function to unlock the table (does NOT clear locked cells)

def unlock_table():

    st.session_state["is_locked"] = False

    st.info("Table unlocked! You can now edit the values again.")

 

# Function to update table data

def update_table_data(new_data):

    for idx, record in enumerate(new_data):

        for col, value in record.items():

            if (str(idx), col) not in st.session_state["locked_cells"]:  # Prevent editing locked cells

                st.session_state["table_data"].at[idx, col] = value

    save_data(st.session_state["table_data"])

 

# Prepare a display-friendly version of the table

display_data = st.session_state["table_data"].copy()

 

# Lock cells by marking them as read-only

for (idx, col), value in st.session_state["locked_cells"].items():

    display_data.at[int(idx), col] = f"🔒 {value}"  # Add lock icon

 

# Render the table

if not st.session_state["is_locked"]:

    edited_data = st.data_editor(display_data.to_dict(orient="records"))

    if edited_data:

        update_table_data(edited_data)

else:

    st.dataframe(display_data)  # Read-only display when locked

 

# Lock and Unlock buttons

if st.button("Lock Table Values"):

    lock_cells()

 

if st.button("Unlock Table Values"):

    unlock_table()
