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

if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'system_prompt' not in st.session_state:
    st.session_state['system_prompt'] = INITIAL_SYSTEM_PROMPT
if 'token_budget' not in st.session_state:
    st.session_state['token_budget'] = 4096


