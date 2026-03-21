from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from google import genai

# 1. Setup the Web Server
app = FastAPI(title="Ripplewalk AI Feedback Router")

# 2. Setup Gemini
client = genai.Client(api_key="AIzaSyBfLJoHt33NDvwYpfbzS4F63AWJe4noMoA")

# 3. Define what the incoming request will look like
class ReviewInput(BaseModel):
    review_text: str

# 4. Create the API Endpoint
@app.post("/analyze")
async def analyze_review(data: ReviewInput):
    prompt = f"""
    You are an AI data extractor for a multi-brand cloud kitchen. 
    Analyze the following customer review and extract the key information into a structured JSON format.
    
    You must respond ONLY with a raw, valid JSON object. Do not include markdown formatting like ```json.
    
    Extract these exact keys:
    - "brand_name": The name of the restaurant.
    - "sentiment": "Positive", "Neutral", or "Negative".
    - "issue_category": "Food Quality", "Delivery Delay", "Customer Service", or "None".
    - "summary": A short, one-sentence summary of the problem.

    Review to analyze:
    "{data.review_text}"
    """
    
    try:
        # Ask Gemini to process the text
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        # Parse the JSON
        extracted_data = json.loads(response.text.strip())
        
        # Apply the business logic
        needs_escalation = False
        if extracted_data['sentiment'] == "Negative":
            needs_escalation = True
            
        # Send the final structured data back to the user/website
        return {
            "status": "success",
            "escalation_triggered": needs_escalation,
            "data": extracted_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))