import streamlit as st
import requests

BASE_URL = "https://marketplace-validator.onrender.com"

st.title("📝 Validate Your Credit Card Listing")

# API Key input (using saved session key if available)
api_key = st.text_input(
    "Enter your API key",
    value=st.session_state.get("api_key", "")
)

listing = st.text_area(
    "Paste your credit card listing here",
    height=250,
    placeholder="Enter your full credit card offer details here..."
)

if st.button("Validate Listing"):
    if not api_key.strip():
        st.warning("Please enter your API key.")
    elif not listing.strip():
        st.warning("Please enter a listing.")
    else:
        headers = {"x-api-key": api_key,
                   "Content-Type": "text/plain"}
        response = requests.post(
            f"{BASE_URL}/validate",
            data=listing.encode("utf-8"),  # send as plain text
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()

            st.subheader("✅ Validation Result" if data["is_valid"] else "❌ Validation Issues")
            st.markdown(f"**Is Valid:** {'Yes ✅' if data['is_valid'] else 'No ❌'}")

            if data["issues"]:
                st.markdown("### ⚠️ Issues Found:")
                for idx, issue in enumerate(data["issues"], start=1):
                    st.markdown(f"{idx}. {issue}")

            if data["suggestions"]:
                st.markdown("### 💡 Suggestions for Improvement:")
                for idx, suggestion in enumerate(data["suggestions"], start=1):
                    st.markdown(f"{idx}. {suggestion}")

            if data["is_valid"]:
                st.success("Your listing meets all the marketplace standards! 🎉")
        else:
            st.error(f"Error {response.status_code}: {response.text}")
