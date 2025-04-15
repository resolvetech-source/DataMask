# streamlit_app.py

import streamlit as st
import requests

st.title("🦙 Local LLaMA Chat")

prompt = st.text_area("Enter your prompt:", "What is the capital of France?")

if st.button("Submit"):
    with st.spinner("Thinking..."):
        res = requests.post("http://localhost:8000/completion", json={
            "prompt": prompt,
            "n_predict": 50
        })

        if res.ok:
            output = res.json()["content"]
            st.success("Response:")
            st.write(output)
        else:
            st.error(f"Error: {res.status_code}")
