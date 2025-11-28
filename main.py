import os
from google import genai


api_key = os.getenv("GEMINI_API_KEY")
print("API loaded")

client = genai.Client()
MODEL = "gemini-2.5-flash"
TEMPERATURE = 0.7
SYSTEM_PROMPT = "You are a cute little bubbly assistant who always speaks with an encouraging and positive tone."

def chat(user_input):
    response = client.models.generate_content(
        model = MODEL,
        contents = [
            {"role" : "user", "parts" : [{"text" : user_input}]}
        ],
        config = genai.types.GenerateContentConfig(
            temperature = TEMPERATURE,
            system_instruction = SYSTEM_PROMPT
        )
    )

    reply = response.text

    if reply is None or reply == "":
        print("\n--- ⚠️ API Response Failed ---")
        print(f"Text output (reply): {reply}")
        print("\nPrompt Feedback (Reason for Failure):")
        # This will print the detailed reason for the block/failure
        print(response.prompt_feedback)

    return reply    

print(chat("Hello, how are you today?"))