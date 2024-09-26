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

        # Get Firestore client
        db = firestore.client()

        def upload_to_firebase(entry):
            db.collection('your_collection_name').add(entry)  # Change 'your_collection_name' to your collection name
            return ""

        # Main Streamlit App
        def main():
            st.title("Intervention Description Entry")

            # Prompt for user input
            st.header("Describe any interventions that you would currently perform.")
            interventions = st.text_area("Interventions Description", height=200)

            # Button to upload to Firebase
            if st.button("Upload Intervention"):
                if interventions:
                    entry = {'interventions': interventions}
                    # Immediately upload to Firebase
                    result = upload_to_firebase(entry)
                    st.success(result)
                    st.success("Your proposed interventions have been stored for review.")
                else:
                    st.error("Please enter a description of the interventions.")

        if __name__ == '__main__':
            main()

    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")

