import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
import base64

st.title("Lockable Table with QR Code & Excel Export")

# Initialize session state if not already
if 'locked_cells' not in st.session_state:
    st.session_state['locked_cells'] = {}

if 'table_data' not in st.session_state:
    st.session_state['table_data'] = pd.DataFrame({
        'Column 1': ["", "", ""],
        'Column 2': ["", "", ""],
        'Column 3': ["", "", ""]
    })

# Function to lock cells
def lock_cells():
    for row in st.session_state['table_data'].iterrows():
        idx, data = row
        st.session_state['locked_cells'][idx] = data.to_dict()

# Function to export table data to Excel
def export_to_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        st.session_state['table_data'].to_excel(writer, index=False, sheet_name='Locked Table')
    output.seek(0)
    return output

# Render the table
edited_df = st.data_editor(st.session_state['table_data'], disabled=list(st.session_state['locked_cells'].keys()))

st.session_state['table_data'] = edited_df

if st.button("Lock Filled Cells"):
    lock_cells()
    st.success("Cells locked!")


# Button to export data to Excel
st.header("Export Locked Table to Excel")
if st.button("Export to Excel"):
    excel_file = export_to_excel()
    st.download_button(
        label="Download Excel File",
        data=excel_file,
        file_name="locked_table.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# Run with: streamlit run app.py
# Let me know if you’d like help deploying or refining this further! 🚀
