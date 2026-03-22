import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

# -----------------------------
# Create Gemini client
# -----------------------------
client = genai.Client(api_key=API_KEY)

# -----------------------------
# Create FastAPI app
# -----------------------------
app = FastAPI(title="Ripplewalk AI Feedback Engine")

# -----------------------------
# Data Models
# -----------------------------
class ReviewInput(BaseModel):
    review: str


class AnalysisResponse(BaseModel):
    brand: str
    sentiment_score: int
    category: str
    is_urgent: bool
    summary: str


# -----------------------------
# Home Route
# -----------------------------
@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Ripplewalk AI Feedback Engine running",
        "docs": "http://127.0.0.1:8000/docs"
    }


# -----------------------------
# Analyze Review Endpoint
# -----------------------------
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_review(input_data: ReviewInput):

    prompt = f"""
You are an AI assistant for a multi-brand cloud kitchen.

Analyze the following food review and extract structured information.

Return ONLY valid JSON with these keys:

brand: string  
sentiment_score: integer from 1 to 10  
category: "Food", "Delivery", or "Service"  
is_urgent: true if hygiene issue OR score < 4  
summary: short one sentence summary  

Review:
"{input_data.review}"
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        parsed = json.loads(response.text)

        return parsed

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI processing failed: {str(e)}"
        )


# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "analyzer:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )