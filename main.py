import os
from google import genai
import tiktoken

api_key = os.getenv("GEMINI_API_KEY")
# print("API loaded")

client = genai.Client()
MODEL = "gemini-2.5-flash"
TEMPERATURE = 0.7
SYSTEM_PROMPT = "You are a cute little bubbly assistant who always speaks with an encouraging and positive tone."
contents = []
TOKEN_BUDGET = 100

def get_encoding(model):
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        print(f"Warning: Tokenizer for model {model} not found. Using cl100k_base encoding.")
        return tiktoken.get_encoding("cl100k_base")
    
ENCODING = get_encoding(MODEL)

def count_tokens(text):
    tokens = ENCODING.encode(text)
    return len(tokens)

def total_token_used(contents):
    try:
        return sum(count_tokens(part["text"]) for message in contents for part in message["parts"] if "text" in part)
    except Exception as e:
        print(f"Error counting tokens: {e}")

def enforce_token_budget(contents, budget = TOKEN_BUDGET):
    try:
        while total_token_used(contents) > budget:
            if len(contents) <= 2:
                contents.pop(1)
    except Exception as e:
        print(f"Token budget error: {e}")

def chat(user_input):

    user_message = {"role": "user", "parts": [{"text": user_input}]}
    contents.append(user_message)
    
    response = client.models.generate_content(
        model = MODEL,
        contents = contents,
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

    contents.append({"role" : "model", "parts" : [{"text" : reply}]})

    return reply    

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in {"exit", "quit"}:
        break
    reply = chat(user_input)
    print("You:" + user_input)
    print("Assistant:" + reply)    