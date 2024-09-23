import os
import pandas as pd
import streamlit as st
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load user data from CSV
user_data = pd.read_csv('users.csv')

st.title("Virtual Patient Chatbot")

# Ask for the user code
user_code = st.text_input("What is your code number?")

if st.button("Submit Code"):
    # Check if the code exists in the CSV
    user_row = user_data[user_data['code'] == int(user_code)]
    
    if not user_row.empty:
        user_name = user_row['name'].values[0]
        st.success(f"Hi {user_name}. Are you ready to get started?")
        
        # Proceed with the chatbot interaction
        question_list = [
            "Describe your symptoms:",
            "How long have you been experiencing these symptoms?",
            "Have you taken any medications for this?",
            "Do you have any allergies we should know about?"
        ]

        # Initialize session state for questions
        if 'current_question_index' not in st.session_state:
            st.session_state.current_question_index = 0
        
        # Function to get the current question
        def get_current_question():
            if st.session_state.current_question_index < len(question_list):
                return question_list[st.session_state.current_question_index]
            else:
                return None

        # Display the current question
        current_question = get_current_question()

        if current_question:
            user_input = st.text_input(current_question)

            if st.button("Submit"):
                if user_input:
                    try:
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": user_input}]
                        )
                        st.write(response.choices[0].message['content'])
                        
                        # Increment the question index for the next question
                        st.session_state.current_question_index += 1

                        # Clear the input field for the next question
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Please enter your response.")
        else:
            st.success("Thank you for your responses!")
    else:
        st.error("Code not recognized. Please try again.")

