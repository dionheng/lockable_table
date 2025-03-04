import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO

st.title("Lockable Table with QR Code Generator")

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

# Render the table
edited_df = st.data_editor(st.session_state['table_data'], disabled=list(st.session_state['locked_cells'].keys()))

st.session_state['table_data'] = edited_df

if st.button("Lock Filled Cells"):
    lock_cells()
    st.success("Cells locked!")

# QR Code linking to live app
st.header("Generate QR Code to Access the Table")
app_url = st.text_input("Enter your deployed app URL (e.g., https://yourapp.streamlit.app)")

if st.button("Generate QR Code for Table Link"):
    if app_url.strip():
        img = qrcode.make(app_url)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        st.image(buffer, caption="Table Link QR Code", use_column_width=True)
        st.download_button(label="Download QR Code", data=buffer.getvalue(), file_name="table_link_qrcode.png", mime="image/png")
    else:
        st.warning("Please enter the deployed app URL to generate a QR code.")

st.info("This app works well on mobile devices via the Streamlit web interface.")

# Run with: streamlit run app.py
# Let me know if you’d like help deploying this! 🚀
