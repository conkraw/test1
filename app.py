import streamlit as st
import pandas as pd
from docx import Document

st.set_page_config(layout="wide")

# Load users from CSV
@st.cache_data
def load_users():
    return pd.read_csv('users.csv')

# Function to read Word document
def read_word_file(file_path):
    doc = Document(file_path)
    content = []
    for para in doc.paragraphs:
        content.append(para.text)
    return "\n".join(content)

# Main app function
def main():
    st.title("Pediatric Clerkship Virtual Clinical Reasoning Assessment")

    # Load user data
    users = load_users()

    # Check if the user is logged in
    if "user_name" in st.session_state:
        # Display welcome message and instructions if user is logged in
        st.write(f"Welcome, {st.session_state.user_name}!")
        st.subheader("Instructions")
        st.write("""
            Please read the following instructions carefully before proceeding:
            - Step 1: Familiarize yourself with the assessment format.
            - Step 2: Ensure you have a quiet environment to take the assessment.
            - Step 3: Once ready, click on the 'Start Assessment' button below.
        """)
        
        # Add a button to start the assessment
        if st.button("Start Assessment"):
            st.session_state.show_assessment = True  # Set a flag to show the assessment page
            st.experimental_rerun()  # Rerun the app to show the new content

    else:
        st.write("Welcome! Please enter your unique code to access the assessment.")

        # Prompt user for unique code
        unique_code = st.text_input("Unique Code:", placeholder="Enter your unique code")

        if st.button("Next"):
            if unique_code:
                try:
                    unique_code = int(unique_code.strip())  # Convert input to integer
                    if unique_code in users['code'].values:
                        st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                        # Rerun to display the welcome page and instructions
                        st.experimental_rerun()
                    else:
                        st.error("Invalid code. Please try again.")
                except ValueError:
                    st.error("Please enter a valid code.")
            else:
                st.error("Please enter a code.")

    # Display the assessment page if the flag is set
    if "show_assessment" in st.session_state and st.session_state.show_assessment:
        st.subheader("Assessment Document")
        # Read and display content from the Word document
        content = read_word_file("ptinfo.docx")
        st.text_area("Document Content", content, height=400)

if __name__ == "__main__":
    main()


