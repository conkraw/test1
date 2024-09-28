import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    # Load Firebase credentials from environment variable
    FIREBASE_KEY_JSON = os.getenv('FIREBASE_KEY')

    if FIREBASE_KEY_JSON is None:
        raise ValueError("FIREBASE_KEY environment variable not set.")

    # Parse the JSON string into a dictionary
    firebase_credentials = json.loads(FIREBASE_KEY_JSON)

    # Initialize Firebase only if not already initialized
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_credentials)
        firebase_admin.initialize_app(cred)

    # Get Firestore client
    db = firestore.client()

    return db

# Function to upload data to Firebase
def upload_to_firebase(db, entry):
    db.collection('your_collection_name').add(entry)  # Change 'your_collection_name' to your collection name
    return "Data uploaded to Firebase."
