# firebase_operations.py
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Initialize Firebase
def initialize_firebase():
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


#def upload_to_firebase(db, entry):
#    db.collection('your_collection_name').add(entry)  # Change 'your_collection_name' to your collection name
#    return "Data uploaded to Firebase."

def upload_to_firebase(db, collection_name, document_id, entry):
    db.collection(collection_name).document(document_id).set(entry, merge=True) 
    return "Data uploaded to Firebase."
