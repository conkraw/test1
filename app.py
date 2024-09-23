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

        # Initialize session state for questions
        if 'current_question_index' not in st.session_state:
            st.session_state.current_question_index = 0
        
        # List of questions
        questions = [
            "Describe your symptoms:",
            "How long have you been experiencing these symptoms?",
            "Have you taken any medications for this?",
            "Do you have any allergies we should know about?"
        ]

        # Function to display the current question and get user input
        def ask_question(index):
            current_question = questions[index]
            user_input = st.text_input(current_question, key=f"input_{index}")

            if st.button("Submit", key=f"submit_{index}"):
                if user_input:
                    try:
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": user_input}]
                        )
                        st.write(response.choices[0].message['content'])
                        
                        # Increment the question index for the next question
                        st.session_state.current_question_index += 1

                        # Clear the input field and show the next question
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Please enter your response.")

        # Check if there are more questions to ask
        if st.session_state.current_question_index < len(questions):
            ask_question(st.session_state.current_question_index)
        else:
            st.success("Thank you for your responses!")
            # Optionally reset the question index for next time
            st.session_state.current_question_index = 0  # Reset if needed
    else:
        st.error("Code not recognized. Please try again.")


