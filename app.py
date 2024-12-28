from dotenv import load_dotenv
import streamlit as st
import os
import base64
import pathlib
import textwrap
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API Key is not configured. Please set it in the environment.")
    st.stop()
genai.configure(api_key=api_key)

# Utility functions
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    if not os.path.exists(png_file):
        st.error("Background image not found.")
        return
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

def get_gemini_response(question):
    try:
        response = genai.generate_text(model="gemini-pro", prompt=question)
        return response.result  # Adjust based on API response structure
    except Exception as e:
        st.error(f"Error fetching response: {e}")
        return None

# Streamlit app setup
st.set_page_config(page_title="Advance Bot")

st.header("Ask to Judo...")

user_input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# Set background image
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
set_background(os.path.join(BASE_DIR, "bg.jpeg"))

if submit:
    if not user_input.strip():
        st.warning("Please enter a question before submitting.")
    else:
        response = get_gemini_response(user_input)
        if response:
            st.subheader("The Response is")
            st.write(response)
