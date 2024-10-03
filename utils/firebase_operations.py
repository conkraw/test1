# firebase_operations.py
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Define a global variable
FIREBASE_COLLECTION_NAME = None

# Initialize Firebase
def initialize_firebase():
    global FIREBASE_COLLECTION_NAME  # Use the global variable

    FIREBASE_KEY_JSON = os.getenv('FIREBASE_KEY')
    FIREBASE_COLLECTION_NAME = os.getenv('FIREBASE_COLLECTION_NAME')
    
    if FIREBASE_KEY_JSON is None:
        raise ValueError("FIREBASE_KEY environment variable not set.")

    try:
        firebase_credentials = json.loads(FIREBASE_KEY_JSON)

        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_credentials)
            firebase_admin.initialize_app(cred)

        return firestore.client()
    except Exception as e:
        raise Exception(f"Error initializing Firebase: {e}")

def upload_to_firebase(db, document_id, entry):
    global FIREBASE_COLLECTION_NAME  # Access the global variable
    db.collection(FIREBASE_COLLECTION_NAME).document(document_id).set(entry, merge=True) 
    return "Data uploaded to Firebase."
