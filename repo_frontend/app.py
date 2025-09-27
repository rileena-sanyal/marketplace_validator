import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"  # FastAPI backend

st.title("Marketplace Validator")

# Initialise session state
if "api_key" not in st.session_state:
    st.session_state.api_key = None
if "lender_name" not in st.session_state:
    st.session_state.lender_name = None

# ------------------------------
# Step 1: Generate API Key
# ------------------------------
if not st.session_state.api_key:
    st.header("Step 1: Generate your API Key")
    lender_name_input = st.text_input("Enter your lender name")

    if st.button("Generate API Key"):
        if not lender_name_input.strip():
            st.warning("Please enter a lender name")
        else:
            response = requests.post(
                f"{BASE_URL}/generate-key",
                json={"lender_name": lender_name_input.strip()}
            )
            if response.status_code == 200:
                data = response.json()
                st.session_state.api_key = data["api_key"]
                st.session_state.lender_name = data["lender_name"]
                st.success(f"API Key generated for {data['lender_name']}: {data['api_key']}")
                st.info("Now proceed to Step 2 below.")
            else:
                st.error(f"Failed to generate key: {response.text}")

# ------------------------------
# Step 2: Validate Listing
# ------------------------------
if st.session_state.api_key:
    st.header("Step 2: Validate Your Listing")
    st.info(f"API Key stored for lender: {st.session_state.lender_name}")

    listing = st.text_area(
        "Paste your credit card listing here",
        height=250
    )

    if st.button("Validate Listing"):
        if not listing.strip():
            st.warning("Please enter a listing")
        else:
            headers = {"x-api-key": st.session_state.api_key,
                       "Content-Type": "text/plain"}
            response = requests.post(
                f"{BASE_URL}/validate",
                data=listing.encode("utf-8"),  # plain string
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                st.subheader("✅ Validation Result" if data["is_valid"] else "❌ Validation Issues")

                # Display overall validity
                st.markdown(f"**Is Valid:** {'Yes ✅' if data['is_valid'] else 'No ❌'}")

                # Display issues
                if data["issues"]:
                    st.markdown("### ⚠️ Issues Found:")
                    for idx, issue in enumerate(data["issues"], start=1):
                        st.markdown(f"{idx}. {issue}")

                # Display suggestions
                if data["suggestions"]:
                    st.markdown("### 💡 Suggestions for Improvement:")
                    for idx, suggestion in enumerate(data["suggestions"], start=1):
                        st.markdown(f"{idx}. {suggestion}")

                # If listing is valid:-
                if data["is_valid"]:
                    st.success("Your listing meets all the marketplace standards! 🎉")
            else:
                st.error(f"Error {response.status_code}: {response.text}")
