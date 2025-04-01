import streamlit as st
import pandas as pd
import os
from utils import extract_text_from_file
from data_masking import generate_masked_text

st.title("AI-Powered Content Masking App (Gemini)")
st.write("This app is powered by AI to mask sensitive information in your content.")
st.write("Upload a **text, PDF, or csv file**, select a role, and let AI mask sensitive data")

# File uploader
uploaded_file = st.file_uploader("Upload Files", type=['txt', 'pdf', 'csv'])

# Select role
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