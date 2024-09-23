import os
import streamlit as st
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Virtual Patient Chatbot")

user_input = st.text_input("Describe your symptoms:")

if st.button("Submit"):
    if user_input:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        st.write(response.choices[0].message['content'])
    else:
        st.warning("Please enter your symptoms.")
