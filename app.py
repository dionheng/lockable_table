import streamlit as st
import pandas as pd
import json
import os

st.title("Fan Blade Cell - Flammable Omats Weekly Checklist")

data_file_path = "table_data.json"
lock_file_path = "lock_state.json"

if 'locked_cells' not in st.session_state:
    st.session_state['locked_cells'] = {}

if 'is_locked' not in st.session_state:
    st.session_state['is_locked'] = False


def load_data():
    if os.path.exists(data_file_path):
        with open(data_file_path, "r") as file:
            data = json.load(file)
        return pd.DataFrame(data)
    else:
        return pd.DataFrame({
            'Number': ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
            'OMAT No.': ["OMat 4-70", "OMat 1001A", "OMat 4-51", "OMat 8-121", "OMat 150", "OMat 4-43", "OMat 4/71", "OMat 4/74", "OMat 4/76"],
            'Batch No.': ["", "", "", "", "", "", "", "", ""],
            'Expiry Date': ["", "", "", "", "", "", "", "", ""]
        })


def load_lock_state():
    if os.path.exists(lock_file_path):
        with open(lock_file_path, "r") as file:
            state = json.load(file)
            st.session_state['locked_cells'] = state.get('locked_cells', {})
            st.session_state['is_locked'] = state.get('is_locked', False)


def save_data(data):
    with open(data_file_path, "w") as file:
        json.dump(data.to_dict(orient="records"), file)


def save_lock_state():
    with open(lock_file_path, "w") as file:
        json.dump({
            'locked_cells': st.session_state['locked_cells'],
            'is_locked': st.session_state['is_locked']
        }, file)


def lock_cells():
    for idx, data in st.session_state['table_data'].iterrows():
        for col, value in data.items():
            if (idx, col) not in st.session_state['locked_cells'] and value.strip():
                st.session_state['locked_cells'][(idx, col)] = value


def unlock_table():
    st.session_state['is_locked'] = False


def update_table_data(new_data):
    for idx, record in enumerate(new_data):
        for col, value in record.items():
            st.session_state['table_data'].at[idx, col] = value


st.session_state['table_data'] = load_data()
load_lock_state()

locked_table_data = st.session_state['table_data'].copy()

if not st.session_state['is_locked']:
    edited_data = st.data_editor(locked_table_data.to_dict(orient='records'))
    if edited_data is not None:
        update_table_data(edited_data)
        save_data(st.session_state['table_data'])
else:
    st.dataframe(locked_table_data)

if st.button("Lock Table Values"):
    lock_cells()
    st.session_state['is_locked'] = True
    save_lock_state()
    st.success("Table values locked successfully! They will remain locked even after a refresh.")

if st.button("Unlock Table Values"):
    unlock_table()
    save_lock_state()
    st.success("Table unlocked! You can now edit the values again.")
