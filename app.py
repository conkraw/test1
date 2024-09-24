import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os
import json

# Load Firebase credentials from environment variable
FIREBASE_KEY_JSON = os.getenv('FIREBASE_KEY')

if FIREBASE_KEY_JSON is None:
    st.error("FIREBASE_KEY environment variable not set.")
else:
    try:
        # Parse the JSON string into a dictionary
        firebase_credentials = json.loads(FIREBASE_KEY_JSON)

        # Initialize Firebase only if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_credentials)
            firebase_admin.initialize_app(cred)

        # Upload data to Firestore
        db = firestore.client()

        def upload_to_firebase(data):
            for entry in data:
                db.collection('your_collection_name').add(entry)  # Change 'your_collection_name' to your collection name
            return "Data uploaded to Firebase."

        # Main Streamlit App
        def main():
            st.title("Data Entry and Upload to Firebase")

            # Input form for user data
            st.header("Enter Data")
            name = st.text_input("Enter Name")
            age = st.number_input("Enter Age", min_value=0)

            # Button to add data to the list
            if st.button("Add Entry"):
                if name:
                    if 'data' not in st.session_state:
                        st.session_state['data'] = []
                    st.session_state['data'].append({'name': name, 'age': age})
                    st.success(f"Added: {name}, Age: {age}")
                else:
                    st.error("Please enter a name.")

            # Show entered data
            if 'data' in st.session_state and st.session_state['data']:
                st.write("Current Entries:")
                st.write(st.session_state['data'])

            # Button to upload to Firebase
            if st.button("Upload to Firebase"):
                if 'data' in st.session_state and st.session_state['data']:
                    result = upload_to_firebase(st.session_state['data'])
                    st.success(result)

                    # Clear the data after upload
                    st.session_state['data'] = []
                else:
                    st.error("No data to upload.")

        if __name__ == '__main__':
            main()

    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")


