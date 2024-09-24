import os
import pandas as pd
import streamlit as st
import openai
from dotenv import load_dotenv
import boto3
from botocore.exceptions import NoCredentialsError

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# AWS S3 configuration
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
bucket_name = os.getenv("BUCKET_NAME")

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

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
                    csv_file_path = 'user_responses.csv'
                    responses_df.to_csv(csv_file_path, mode='a', header=not os.path.isfile(csv_file_path), index=False)

                    # Upload the CSV file to Amazon S3
                    upload_to_s3(bucket_name, csv_file_path)

                    st.success("Responses saved and uploaded to Amazon S3 successfully!")

                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please enter your symptoms.")
    else:
        st.error("Code not recognized. Please try again.")

def upload_to_s3(bucket_name, file_path):
    """Uploads a file to the specified S3 bucket."""
    try:
        s3_client.upload_file(file_path, os.path.basename(file_path), file_path)
        st.success(f"File {file_path} uploaded to {bucket_name} on S3.")
    except FileNotFoundError:
        st.error("The file was not found.")
    except NoCredentialsError:
        st.error("Credentials not available.")
    except Exception as e:
        st.error(f"Failed to upload to S3: {e}")




