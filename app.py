import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os
import json

# Function to read diagnoses from a file
def read_diagnoses_from_file():
    with open('dx_list.txt', 'r') as file:
        diagnoses = [line.strip() for line in file.readlines() if line.strip()]
    return diagnoses

# Set the page config to normal
st.set_page_config(layout="wide")

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
            return "Data uploaded to Firebase."

        # Initialize session state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "diagnoses"
        if 'diagnoses' not in st.session_state:
            st.session_state.diagnoses = [""] * 5
        if 'prioritized_diagnoses' not in st.session_state:
            st.session_state.prioritized_diagnoses = []

        # Title of the app
        st.title("Differential Diagnosis Tool")

        # Diagnoses Page
        if st.session_state.current_page == "diagnoses":
            st.markdown("""
                ## DIFFERENTIAL DIAGNOSIS
                Please select 5 possible diagnoses you would consider. Do not provide duplicates.
            """)

            # Load diagnoses from file
            dx_options = read_diagnoses_from_file()
            dx_options.insert(0, "")  # Insert a blank option
            
            # Create columns for each diagnosis input
            cols = st.columns(5)
            for i, col in enumerate(cols):
                with col:
                    st.session_state.diagnoses[i] = st.selectbox(
                        f"Diagnosis {i + 1}",
                        options=dx_options,
                        index=0,
                        key=f"diagnosis_{i}"
                    )

            # Button to submit the diagnoses
            if st.button("Submit Diagnoses"):
                diagnoses = [d.strip() for d in st.session_state.diagnoses]
                if all(diagnosis for diagnosis in diagnoses):
                    if len(diagnoses) == len(set(diagnoses)):
                        st.session_state.prioritized_diagnoses = diagnoses.copy()  # Save for prioritization
                        st.session_state.current_page = "prioritize"  # Move to Prioritization page
                        st.rerun()  # Rerun the app to refresh the page
                    else:
                        st.error("Please do not provide duplicate diagnoses.")
                else:
                    st.error("Please select all 5 diagnoses.")

        # Prioritization Page
        elif st.session_state.current_page == "prioritize":
            st.markdown("""
                ## RANK YOUR DIAGNOSES
                Please rank your diagnoses in the sidebar.
            """)

            rank_options = ["", "Most Likely", "Second Most Likely", "Third Most Likely", "Fourth Most Likely", "Least Likely"]
            rankings = {}
            used_ranks = set()

            with st.sidebar:
                st.subheader("Rank Your Diagnoses")
                for diagnosis in st.session_state.prioritized_diagnoses:
                    available_ranks = [rank for rank in rank_options if rank not in used_ranks]
                    rank = st.selectbox(f"Rank for {diagnosis}", options=available_ranks, key=diagnosis)
                    if rank:  # Only add to rankings if a rank is selected
                        rankings[diagnosis] = rank
                        used_ranks.add(rank)

                # Button to submit rankings
                if st.button("Submit Rankings"):
                    entry = {
                        'ranked_diagnoses': rankings  # Create a dictionary for ranked diagnoses
                    }
                    result = upload_to_firebase(entry)
                    st.success(result)  # Display success message

                    # Optionally: Reset state if desired, or keep current state
                    st.session_state.current_page = "diagnoses"  # Uncomment this line to go back
                    # st.session_state.diagnoses = [""] * 5  # Uncomment this line to reset for the next round
                    # st.session_state.prioritized_diagnoses = []  # Uncomment this line to clear prioritized diagnoses
                    # st.rerun()  # Uncomment to refresh the app

    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")
