🚀 FoodTech AI Feedback Engine
An intelligent backend service designed to automate customer feedback analysis for cloud kitchens. This engine leverages Google Gemini 2.0 Flash to transform raw customer reviews into actionable data, enabling real-time brand monitoring and crisis management.

🎯 The Problem & Solution
The Problem: Cloud kitchens receive thousands of reviews across platforms (Zomato, Swiggy, WhatsApp). Manually identifying which brand the feedback is for and whether it's an emergency (hygiene/safety) is slow and error-prone.

The Solution: This API acts as an automated "First Responder." It:

Identifies the Brand: Distinguishes between Pink Adrak, Great Indian Khichdi, and other portfolio brands.

Analyzes Sentiment: Converts emotional text into a numerical score (1-10).

Flags Urgency: Uses AI to detect critical safety or service failures for immediate escalation.

Categorizes: Tags feedback as Food, Delivery, or Service for internal routing.

🛠️ Tech Stack
Framework: FastAPI (High-performance Python framework)

AI Model: Google Gemini 2.0 Flash (State-of-the-art LLM)

Validation: Pydantic v2 (Strict type safety)

Environment: Python-Dotenv (Secure secret management)

📂 Project Structure
Plaintext
foodtech-ai-engine/
├── .venv/               # Virtual environment (ignored by git)
├── .env                 # API Keys (ignored by git)
├── .gitignore           # Safety rules for GitHub
├── analyzer.py          # Core FastAPI logic & AI Integration
├── requirements.txt     # Project dependencies
└── README.md            # Documentation
🚦 Getting Started
1. Installation
Bash
git clone https://github.com/iamsashi/foodtech-ai-engine.git
cd foodtech-ai-engine
python -m venv .venv
# Activate: .venv\Scripts\activate (Windows)
pip install -r requirements.txt
2. Configuration
Create a .env file in the root directory:

Plaintext
GEMINI_API_KEY=your_key_here
3. Execution
Bash
python -m uvicorn analyzer:app --reload
📖 API Documentation
Endpoint: POST /analyze
Request Payload:

JSON
{
  "review": "My order from Pink Adrak arrived 40 mins late and the food was cold.",
  "source": "Zomato"
}
AI-Generated Response:

JSON
{
  "brand": "Pink Adrak",
  "sentiment_score": 3,
  "category": "Delivery",
  "is_urgent": true,
  "summary": "Customer reports significant delivery delay and cold food."
}
🧪 Testing the AI
This project includes a built-in UI for testing. Once the server is running, visit:
👉 http://127.0.0.1:8000/docs
