import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

st.title("Lockable Table with Excel Export")

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

# Function to export locked table data to Excel
def export_to_excel():
    output = BytesIO()
    locked_df = pd.DataFrame.from_dict(st.session_state['locked_cells'], orient='index')
    locked_df['Timestamp'] = [st.session_state['timestamps'].get(idx, '') for idx in locked_df.index]
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        locked_df.to_excel(writer, index=False, sheet_name='Locked Table')
    output.seek(0)
    return output

# Render the table
edited_df = st.data_editor(st.session_state['table_data'], disabled=list(st.session_state['locked_cells'].keys()))

st.session_state['table_data'] = edited_df

if st.button("Lock Filled Cells and Export to Excel"):
    lock_cells()
    excel_file = export_to_excel()
    st.success("Cells locked and table exported!")
    st.download_button(
        label="Download Locked Table as Excel",
        data=excel_file,
        file_name="locked_table.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.info("This app works well on mobile devices via the Streamlit web interface.")

# Run with: streamlit run app.py

