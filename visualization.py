import streamlit as st
import pandas as pd
import os
from utils import extract_text_from_file
from data_masking import generate_masked_text
from PIL import Image
# Load company logo (Make sure the logo file is in the same directory or provide the correct path)
logo = Image.open("resolve_tech_solutions_logo.jpg")  # Replace with your actual logo file

# Layout for top section with logo
col1, col2 = st.columns([1, 4])
with col1:
    st.image(logo, width=100)  # Adjust width as needed
with col2:
    st.title("Data Privacy Application")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Masking"])

# Page Routing
if page == "Home":
    st.write("Welcome to the Data Privacy Application!")
    st.write("Select an option from the sidebar.")

elif page == "Data Masking":
    st.subheader("Data Masking Tool")
    st.write("Upload a document and apply masking.")
    
    uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf","csv"])
    role = st.selectbox("Select Role", ["General","HR", "IT", "Manager", "Finance", "Legal"])
    st.write("You selected:", role)

    if uploaded_file and role:
        text = extract_text_from_file(uploaded_file)
        st.write("Uploaded text:")
        st.write(text)

        if text:
            st.subheader(" Processing with Gemini...")
            masked_text = generate_masked_text(role, text)

            st.subheader("Masked Output:")
            st.text_area("Masked Text", value=masked_text, height=400, max_chars=None)

            st.download_button(
                label="Download Masked Text",
                data=masked_text,
                file_name="masked_text.txt",
                mime="text/plain",
            )
        else:
            st.error("Error:Unable to extract text from the uploaded file")

# # File uploader
# uploaded_file = st.file_uploader("Upload Files", type=['txt', 'pdf', 'csv'])

# # Select role
# role = st.selectbox("Select Role", ["General","HR", "IT", "Manager", "Finance", "Legal"])
# st.write("You selected:", role)

# if uploaded_file and role:
#     text = extract_text_from_file(uploaded_file)
#     st.write("Uploaded text:")
#     st.write(text)

#     if text:
#         st.subheader(" Processing with Gemini...")
#         masked_text = generate_masked_text(role, text)

#         st.subheader("Masked Output:")
#         st.text_area("Masked Text", value=masked_text, height=400, max_chars=None)

#         st.download_button(
#             label="Download Masked Text",
#             data=masked_text,
#             file_name="masked_text.txt",
#             mime="text/plain",
#         )
#     else:
#         st.error("Error:Unable to extract text from the uploaded file")