import streamlit as st
import pandas as pd
import os
from utils import extract_text_from_file, fetch_employee_details
from data_masking import generate_masked_and_policy_text,generating_sql_query
from PIL import Image
# Load company logo (Make sure the logo file is in the same directory or provide the correct path)
logo = Image.open("resolve_tech_solutions_logo.jpg")

# Layout for top section with logo
col1, col2 = st.columns([1, 4])
with col1:
    st.image(logo, width=100)  # Adjust width as needed
with col2:
    st.title("Data Privacy Application")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Employee Lookup"])

# Page Routing
if page == "Home":
    st.write("Welcome to the Data Privacy Application!")
    st.write("Select an option from the sidebar.")

elif page == "Employee Lookup":
    st.subheader("Fetching Employee Records")

    user_query = st.text_input("Enter your query")
    role = st.selectbox("Select the Role",["General","HR","IT","Manager","Finance","Legal","Admin"])

    if st.button("Fetch Employee Details"):
        sql_query = generating_sql_query(user_query)
        st.write("Generated SQL Query:",sql_query)
        column_names,records = fetch_employee_details(sql_query)
        if records:
            masked_text = generate_masked_and_policy_text(role, column_names,records)

            st.subheader("Masked Output:")
            st.text_area("Masked Text", value = masked_text, height = 400 )

            # st.subheader(f"{role} Policy Information")
            # st.text_area("Generated Policy", value=policy_text,height=400)
        else:
            st.error("No matching employee records")

