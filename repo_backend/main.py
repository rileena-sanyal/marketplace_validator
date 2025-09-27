import os
import json
import secrets
from fastapi import FastAPI, Header, HTTPException, Depends, Body
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Dict

load_dotenv()

# --------------------
# Setup LLM
## Using OpenRouter for OpenAI API key and base_url
# --------------------
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# --------------------
# Loading marketplace_validator_prompt.txt as base prompt
## This base prompt is modified further down to output text in a json format
# --------------------
with open("repo_backend/marketplace_validator_prompt.txt", "r", encoding="utf-8") as f:
    BASE_PROMPT = f.read()

# --------------------
# FastAPI app
# --------------------
app = FastAPI(title="Marketplace Validator API", version="0.1.0")

# --------------------
# In-memory lender API keys
## This can be further replaced with a db for production
# --------------------
lenders_db: Dict[str, str] = {}  # lender_name -> api_key

# --------------------
# Models
# --------------------
class GenerateKeyRequest(BaseModel):
    """This class is to take the lender_name as input"""
    lender_name: str

class GenerateKeyResponse(BaseModel):
    """This class is to respond with lender_name and api_key as outputs"""
    lender_name: str
    api_key: str

class ListingRequest(BaseModel):
    """This class is to take a listing as a string input"""
    listing: str

class ValidatorResponse(BaseModel):
    """The final output is generated as a json schema"""
    is_valid: bool
    issues: list[str]
    suggestions: list[str]

# --------------------
# Helper Functions
# --------------------
def generate_api_key(length: int = 32) -> str:
    """To generate a secret api key"""
    return secrets.token_hex(length)

def validate_api_key(x_api_key: str = Header(...)) -> str:
    """To verify API key and return lender name."""
    for lender_name, api_key in lenders_db.items():
        if api_key == x_api_key:
            return lender_name
    raise HTTPException(status_code=401, detail="Unauthorized: invalid API key")

def call_llm_validator(listing: str) -> dict:
    """To call the LLM to validate the listing."""
    structured_prompt = BASE_PROMPT + """

        Return your response as JSON with the following format:
        
        {
          "is_valid": true or false,
          "issues": ["list", "of", "issues", "if", "any"],
          "suggestions": ["list of suggested fixes or rewrites, if any. if not, leave empty"]
        }
        """   # enforcing final output in a json schema
    full_prompt = structured_prompt.replace("{{ listing }}", listing)

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a reasonable credit card listing validator."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0,  # for deterministic behaviour
    )

    raw_output = response.choices[0].message.content.strip()

    # Attempt to parse JSON
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        try:
            if raw_output.startswith("```json"):
                raw_output = raw_output.replace("```json", "").replace("```", "").strip()
            return json.loads(raw_output)
        except Exception:
            return {
                "is_valid": False,
                "issues": ["Failed to parse LLM output."],
                "suggestions": [raw_output]
            }

# --------------------
# API Endpoints
# --------------------
@app.post("/generate-key", response_model=GenerateKeyResponse)
def generate_key(req: GenerateKeyRequest):
    """Generate a unique API key for a lender."""
    lender_name = req.lender_name.strip()
    if lender_name in lenders_db:
        return GenerateKeyResponse(lender_name=lender_name, api_key=lenders_db[lender_name])

    api_key = generate_api_key()
    lenders_db[lender_name] = api_key
    return GenerateKeyResponse(lender_name=lender_name, api_key=api_key)

@app.post("/validate", response_model=ValidatorResponse)
async def validate_listing(listing: str = Body(..., media_type="text/plain"), lender: str = Depends(validate_api_key)):
    """
    Validate a credit card listing sent as a plain string.
    API key required in the x-api-key header.
    """
    result = call_llm_validator(listing)

    return ValidatorResponse(
        is_valid=result.get("is_valid", False),
        issues=result.get("issues", []),
        suggestions=result.get("suggestions", [])
    )

@app.get("/")
def root():
    return {
        "message": "Marketplace Validator API is running.",
        "instructions": "Use /generate-key (POST) to get API key, then use /validate (POST) to validate listings."
    }

# --------------------
# Run server
# --------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
