import os
from google import genai
import tiktoken
import google.genai.types as types


# api_key = os.getenv("GEMINI_API_KEY")
# print("API loaded")

client = genai.Client()
MODEL = "gemini-2.5-flash"
# TEMPERATURE = 0.7
INITIAL_SYSTEM_PROMPT = "You are a cute little bubbly assistant who always speaks with an encouraging and positive tone."
# contents = []
# TOKEN_BUDGET = 100

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

# def enforce_token_budget(contents, budget = TOKEN_BUDGET):
#     try:
#         while total_token_used(contents) > budget:
#             if len(contents) <= 2:
#                 contents.pop(1)
#     except Exception as e:
#         print(f"Token budget error: {e}")

def enforce_token_budget(contents, budget):
    while total_token_used(contents) > budget and len(contents) >= 2:
        print(f"[INFO: Token budget exceeded ({total_token_used(contents)} > {budget}). Trimming history.]")
        contents.pop(0)
        if len(contents) >= 1:
            contents.pop(0)

# def chat(user_input):

#     user_message = {"role": "user", "parts": [{"text": user_input}]}
#     contents.append(user_message)
    
#     response = client.models.generate_content(
#         model = MODEL,
#         contents = contents,
#         config = genai.types.GenerateContentConfig(
#             temperature = TEMPERATURE,
#             system_instruction = SYSTEM_PROMPT
#         )
#     )

#     enforce_token_budget(contents)

#     reply = response.text

#     if reply is None or reply == "":
#         print("\n--- ⚠️ API Response Failed ---")
#         print(f"Text output (reply): {reply}")
#         print("\nPrompt Feedback (Reason for Failure):")
#         # This will print the detailed reason for the block/failure
#         print(response.prompt_feedback)

#     contents.append({"role" : "model", "parts" : [{"text" : reply}]})

#     return reply    


def chat(contents, user_input, uploaded_file_data, temperature, system_prompt, budget):
    
    # 1. Construct the user message, including image if present
    user_parts = [{"text": user_input}]
    if uploaded_file_data:
        # Streamlit provides the file-like object, use from_bytes
        user_parts.insert(0, types.Part.from_bytes(
            data = uploaded_file_data.getvalue(),
            mime_type = uploaded_file_data.type
        ))
        
    user_message = {"role": "user", "parts": user_parts}
    contents.append(user_message)
    
    # 2. Enforce budget
    enforce_token_budget(contents, budget)
    
    # 3. Call the API with STREAMING (Feature 4)
    response_stream = client.models.generate_content_stream(
        model = MODEL,
        contents = contents,
        config = types.GenerateContentConfig(
            temperature=temperature,
            system_instruction=system_prompt
        )
    )
    
    # Note: Streamlit handles the actual writing of the stream to the UI,
    # so we return the stream object here.
    return response_stream

# while True:
#     user_input = input("You: ")
#     if user_input.strip().lower() in {"exit", "quit"}:
#         break
#     reply = chat(user_input)
#     print("You:" + user_input)
#     print("Assistant:" + reply)    
#     print("Current token :", total_token_used(contents))