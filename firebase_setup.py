import os
import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    FIREBASE_KEY_JSON = os.getenv('FIREBASE_KEY')
    if FIREBASE_KEY_JSON is None:
        st.error("FIREBASE_KEY environment variable not set.")
    else:
        try:
            firebase_credentials = json.loads(FIREBASE_KEY_JSON)
            if not firebase_admin._apps:
                cred = credentials.Certificate(firebase_credentials)
                firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Error initializing Firebase: {e}")

def upload_to_firebase(entry):
    db = firestore.client()
    db.collection('your_collection_name').add(entry)
    return "Data uploaded to Firebase."
