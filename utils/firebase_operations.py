import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os
import json

# Initialize Firebase
def initialize_firebase():
    # Load Firebase credentials from environment variable
    FIREBASE_KEY_JSON = os.getenv('FIREBASE_KEY')

    if FIREBASE_KEY_JSON is None:
        st.error("FIREBASE_KEY environment variable not set.")
        return None

    try:
        # Parse the JSON string into a dictionary
        firebase_credentials = json.loads(FIREBASE_KEY_JSON)

        # Initialize Firebase only if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_credentials)
            firebase_admin.initialize_app(cred)

        # Get Firestore client
        return firestore.client()
    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")
        return None

def upload_to_firebase(db, entry):
    if db is not None:
        db.collection('your_collection_name').add(entry)  # Change 'your_collection_name' to your collection name
        return "Data uploaded to Firebase."
    else:
        return "Failed to upload data. Firebase not initialized."
