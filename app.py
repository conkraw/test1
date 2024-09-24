import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
FIREBASE_KEY_PATH = os.getenv('FIREBASE_KEY_PATH')
FIRESTORE_COLLECTION = os.getenv('FIRESTORE_COLLECTION')

# Initialize Firebase
def initialize_firebase():
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)

def upload_to_firebase(data):
    for entry in data:
        db.collection(FIRESTORE_COLLECTION).add(entry)
    return "Data uploaded to Firebase."

# Main Streamlit App
def main():
    st.title("Data Entry and Upload to Firebase")

    # Initialize Firebase only once
    if not firebase_admin._apps:
        initialize_firebase()
    
    db = firestore.client()

    # Input form for user data
    st.header("Enter Data")
    name = st.text_input("Enter Name")
    age = st.number_input("Enter Age", min_value=0)

    # Button to add data to the list
    if st.button("Add Entry"):
        if name:
            if st.session_state.get('data') is None:
                st.session_state['data'] = []
            st.session_state['data'].append({'name': name, 'age': age})
            st.success(f"Added: {name}, Age: {age}")
        else:
            st.error("Please enter a name.")

    # Show entered data
    if 'data' in st.session_state and st.session_state['data']:
        st.write("Current Entries:")
        st.write(st.session_state['data'])

    # Button to save data to CSV and upload to Firebase
    if st.button("Upload to Firebase"):
        if 'data' in st.session_state and st.session_state['data']:
            # Save to CSV
            df = pd.DataFrame(st.session_state['data'])
            csv_filename = "data.csv"
            df.to_csv(csv_filename, index=False)
            st.success(f"Data saved to {csv_filename}")

            # Upload to Firebase
            result = upload_to_firebase(st.session_state['data'])
            st.success(result)

            # Clear the data after upload
            st.session_state['data'] = []
        else:
            st.error("No data to upload.")

if __name__ == '__main__':
    main()






