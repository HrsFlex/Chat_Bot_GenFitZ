# Q&A Chatbot

from dotenv import load_dotenv

load_dotenv()  

import streamlit as st
import os
import base64
import pathlib
import textwrap

import google.generativeai as genai

# from IPython.display import display
# from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center center;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
  



def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text



st.set_page_config(page_title="Advance Bot")

st.header("Ask to Judo...")

input=st.text_input("Input: ",key="input")


submit=st.button("Ask the question")




BASE_DIR = os.path.dirname(os.path.abspath(__file__))
set_background(f"{BASE_DIR}/bg.jpeg")


if submit:
    
    response=get_gemini_response(input)
    st.subheader("The Response is")
    st.write(response)
