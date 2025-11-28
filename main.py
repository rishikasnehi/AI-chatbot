import os
from google import genai


api_key = os.getenv("GEMINI_API_KEY")

# print("API loaded")

client = genai.Client(api_key = api_key)

# SYSTEM_INSTRUCTION = "You are a cute little bubbly assistant who always speaks with an encouraging and positive tone."

response = client.models.generate_content(
    model = "gemini-2.5-flash",
        contents = [
            {"role" : "user", "parts" : [{"text" : "Tell me a joke about dogs"}]}
    ],
    config = genai.types.GenerateContentConfig(
        temperature = 0.7,
        max_output_tokens = 150,
        system_instruction = "You are a cute little bubbly assistant who always speaks with an encouraging and positive tone."

    )
)
print(response)