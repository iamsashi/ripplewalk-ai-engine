import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai

# 1. Load configuration
load_dotenv()
app = FastAPI(title="Ripplewalk AI Analytics Engine")

# 2. Setup Gemini Client
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY missing from .env file")
client = genai.Client(api_key=API_KEY)

# 3. Data Schemas
class FeedbackRequest(BaseModel):
    review: str = Field(..., min_length=10, max_length=1000)
    source: str = "customer_chat"

class AnalysisResponse(BaseModel):
    brand: str
    sentiment_score: int
    category: str 
    is_urgent: bool
    summary: str

# 4. Home Route
@app.get("/")
async def home():
    return {"status": "Online", "message": "Go to /docs to test"}

# 5. Core Logic
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_feedback(data: FeedbackRequest):
    prompt = f"""
    Analyze this customer review: "{data.review}"
    Return ONLY a JSON object with:
    - brand: (e.g., Pink Adrak, Great Indian Khichdi, or Unknown)
    - sentiment_score: (1-10)
    - category: (Food, Delivery, or Service)
    - is_urgent: (true/false)
    - summary: (Max 10 words)
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )
        
        result = json.loads(response.text)
        
        if result.get("is_urgent") or result.get("sentiment_score", 10) <= 3:
            print(f"🚨 ALERT: Escalating {result.get('brand')} issue!")
            
        return result

    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        if "429" in str(e):
            raise HTTPException(status_code=429, detail="API Limit reached. Wait 60s.")
        raise HTTPException(status_code=500, detail="AI Analysis Failed")