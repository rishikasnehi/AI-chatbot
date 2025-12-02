import streamlit as st
import os
from PIL import Image
from io import BytesIO
from google.genai.errors import APIError

from main import (
    chat, 
    total_token_used, 
    enforce_token_budget, 
    MODEL, 
    INITIAL_SYSTEM_PROMPT
)
 
st.set_page_config(page_title = "Chatbot", page_icon = "🤖", layout = "wide")
st.title("💖 Bubbly Gemini Chatbot")

if "GEMINI_API_KEY" not in os.environ:
    st.error("Error: GEMINI_API_KEY environment variable not found. Please set it.")
    st.stop()

if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'system_prompt' not in st.session_state:
    st.session_state['system_prompt'] = INITIAL_SYSTEM_PROMPT
if 'token_budget' not in st.session_state:
    st.session_state['token_budget'] = 4096

with st.sidebar:

    st.header("⚙️ Configuration")
    new_system_prompt = st.text_area(
        "Set Assistant Persona (System Prompt):",
        st.session_state['system_prompt'],
        height=150
    )

    if new_system_prompt != st.session_state['system_prompt']:
        st.session_state['system_prompt'] = new_system_prompt
        st.session_state['history'] = [] 
        st.toast("Persona updated and chat history cleared!")

    #Creates a slider for the user to select a value between 0.0 and 1.0.
    st.subheader("Model Settings")
    temperature = st.slider(
        "Creativity (Temperature)", min_value = 0.0, max_value = 1.0, value = 0.7, step = 0.05
    )

    current_tokens = total_token_used(st.session_state['history'])

    st.subheader(f"History Tokens: {current_tokens}")
    st.progress(min(current_tokens / st.session_state['token_budget'], 1.0), 
                text=f"{current_tokens} / {st.session_state['token_budget']} tokens used")

    if st.button("Clear Chat History", use_container_width=True):
        st.session_state['history'] = []
        st.toast("Chat history cleared!")
        st.experimental_rerun()
