from google import genai

# 1. Hand the VIP pass to the Gemini client
client = genai.Client(api_key="GEMINI_API_KEY")

print("Sending message to Gemini...")

# 2. Make the request to the AI model
# We use gemini-2.5-flash because it is lightning fast and great for coding tasks
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hi there! Can you tell me a one-sentence joke about Python programming?"
)

# 3. Print the AI's reply
print("\nGemini says:", response.text)