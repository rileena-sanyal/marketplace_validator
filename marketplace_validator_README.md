# Marketplace Validator

**Live Streamlit Apps:**
- [Main App](https://marketplacevalidator-app.streamlit.app/)
- [Generate API Key App](https://marketplace-validator-generatekey.streamlit.app/)
- [Validate Listing App](https://marketplace-validator-validatelisting.streamlit.app/)

**Backend:**
- [FastAPI Render Backend](https://marketplace-validator.onrender.com/)

---

## Project Overview
Marketplace Validator is a tool that validates credit card listings for compliance, clarity, and transparency. It uses a FastAPI backend for validation logic powered by OpenAI's GPT models and a set of Streamlit frontends for user interaction.

### Features
- Generate a unique API key for a lender.
- Validate credit card listings using a plain-text input.
- Get structured feedback including compliance issues and suggested improvements.
- Independent Streamlit apps for generating API keys and validating listings.

---

## Repository Structure
```
marketplace_validator/
│
├── repo_backend/            # FastAPI backend
│   ├── main.py              # Backend API code
│   ├── marketplace_validator_prompt.txt  # Validator prompt for LLM
│
├── repo_frontend/           # Streamlit frontend apps
│   ├── app.py               # Main Streamlit app
│   ├── generate_key_app.py  # Generate API Key app
│   ├── validate_listing_app.py # Validate Listing app
│
├── .gitignore               # Git ignore file (includes .env and venv)
├── Procfile                 # For deployment (Streamlit)
├── requirements.txt         # Project dependencies
└── README.md
```

---

## Setup Instructions

### Backend (FastAPI) Setup
1. Clone the repository:
```bash
git clone https://github.com/rileena-sanyal/marketplace_validator.git
cd marketplace_validator/repo_backend
```
2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Create a `.env` file in `repo_backend` with the following content:
```
OPENAI_API_KEY=your_openai_api_key
```
5. Run the FastAPI backend locally:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend (Streamlit) Setup
1. Navigate to the frontend directory:
```bash
cd ../repo_frontend
```
2. Install Streamlit:
```bash
pip install -r requirements.txt
```
3. Update the `BASE_URL` in each app to point to your backend:
```python
BASE_URL = "http://127.0.0.1:8000"  # or your deployed Render backend URL
```
4. Run any app locally:
```bash
streamlit run app.py
# or generate_key_app.py / validate_listing_app.py
```

---

## Deployment

### Backend (Render)
1. Connect your GitHub repository in Render.
2. Choose `repo_backend` as the root directory.
3. Set environment variables (OPENAI_API_KEY).
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy your backend.

### Frontend (Streamlit Cloud)
1. Connect your GitHub repository in Streamlit Cloud.
2. Select the branch `main`.
3. For each app, set the `Main file path` to the respective Streamlit app file:
   - `repo_frontend/app.py`
   - `repo_frontend/generate_key_app.py`
   - `repo_frontend/validate_listing_app.py`
4. Set the `BASE_URL` secret in Streamlit to point to your Render backend.
5. Deploy each app independently.

---

## Usage
1. **Generate API Key:** Navigate to the Generate API Key app and create a key.
2. **Validate Listing:** Use the Validate Listing app with your API key to check credit card listings.
3. **Main App:** Users can generate an API key and validate listings in a single interface.

---

## Notes
- `.env` files and `venv` are excluded from GitHub via `.gitignore`.
- Streamlit apps are independent but can share the same backend.
- API keys are stored in-memory in the backend for demo purposes. Use a database for production.

---

**Author:** Rileena Sanyal
**Date:** 27th Sept 2025

