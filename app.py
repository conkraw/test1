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
    user_row = user_data[user_data['code'] == int(user_code)]
    
    if not user_row.empty:
        user_name = user_row['name'].values[0]
        st.success(f"Hi {user_name}. Are you ready to get started?")
        
        # Prepare to log responses
        user_responses = []

        # Proceed with the chatbot interaction
        user_input = st.text_input("Describe your symptoms:")
        
        if st.button("Submit Symptoms"):
            if user_input:
                # Log the user input
                user_responses.append({"Code": user_code, "Name": user_name, "Symptoms": user_input})
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": user_input}]
                    )
                    chatbot_response = response.choices[0].message['content']
                    st.write(chatbot_response)
                    
                    # Log the chatbot response
                    user_responses[-1]["Chatbot Response"] = chatbot_response
                    
                    # Save responses to CSV
                    responses_df = pd.DataFrame(user_responses)
                    responses_df.to_csv('user_responses.csv', mode='a', header=not os.path.isfile('user_responses.csv'), index=False)

                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please enter your symptoms.")
    else:
        st.error("Code not recognized. Please try again.")



