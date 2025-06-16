import streamlit as st
import requests

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")

st.title("🤖 Gemini Chatbot with Prompt Versioning")

# API endpoint
API_URL = "http://localhost:8000/chat"  # Change to your deployed URL if hosted

# Prompt version options
prompt_versions = ["v1", "v2"]

# User input
user_input = st.text_input("Enter your message:")
prompt_version = st.selectbox("Choose Prompt Version:", prompt_versions)

if st.button("Ask Gemini"):
    if user_input.strip() == "":
        st.warning("Please enter a message.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={
                    "message": user_input,
                    "prompt_version": prompt_version
                })
                if response.status_code == 200:
                    st.success("Response:")
                    st.write(response.json()["response"])
                else:
                    st.error(f"Error: {response.status_code} - {response.json().get('detail')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection Error: {e}")
