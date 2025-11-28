import os
from google import genai


api_key = os.getenv("GEMINI_API_KEY")

# print("API loaded")

client = genai.Client()

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
reply = response.text
if reply is None or reply == "":
    print("\n--- ⚠️ API Response Failed ---")
    print(f"Text output (reply): {reply}")
    print("\nPrompt Feedback (Reason for Failure):")
    # This will print the detailed reason for the block/failure
    print(response.prompt_feedback)
print(reply)