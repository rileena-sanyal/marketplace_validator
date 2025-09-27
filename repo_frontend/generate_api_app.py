import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("🔑 Generate Your API Key")
st.write("Enter your lender name to generate a unique API key. This key will allow you to validate your credit card listings.")

lender_name = st.text_input("Lender Name")

if st.button("Generate API Key"):
    if not lender_name.strip():
        st.warning("Please enter a lender name.")
    else:
        response = requests.post(
            f"{BASE_URL}/generate-key",
            json={"lender_name": lender_name.strip()}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.api_key = data["api_key"]

            st.success(f"✅ API Key generated successfully:\n\n`{data['api_key']}`")
            st.info("You can now go to the **Validate Listing** page to test your listings.")
        else:
            st.error(f"Failed to generate key: {response.text}")
