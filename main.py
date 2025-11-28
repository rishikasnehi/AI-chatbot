import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

# print("API loaded")

client = genai.Client(api_key = api_key)
response = client.models.generate_content(
    model = "gemini-2.5-flash",
        contents = [
            {"role" : "user", "parts" : [{"text" : "Tell me a joke about dogs"}]}
    ]
)
print(response)