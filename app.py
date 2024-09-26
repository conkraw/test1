import streamlit as st
import pandas as pd
from docx import Document

# Set page layout to wide
st.set_page_config(layout="wide")

# Cache loading of users from CSV
@st.cache_data
def load_users():
    return pd.read_csv('users.csv')

# Function to read the Word document and extract text
def read_word_text(docx_file_path):
    doc = Document(docx_file_path)
    full_text = []
    
    # Extract all paragraphs from the document
    for para in doc.paragraphs:
        full_text.append(para.text)
    
    # Join paragraphs into a single string
    return "\n\n".join(full_text)

# Main app function
def main():
    st.title("Pediatric Clerkship Virtual Clinical Reasoning Assessment")

    # Load user data
    users = load_users()

    # Initialize session state for page if not already done
    if "page" not in st.session_state:
        st.session_state.page = "login"  # Start on the login page

    # Check which page to display
    if st.session_state.page == "assessment":
        display_assessment()
    else:
        login_page(users)

# Login page function
def login_page(users):
    st.write("Welcome! Please enter your unique code to access the assessment.")
    unique_code = st.text_input("Unique Code:")
    
    if st.button("Next"):
        if unique_code:
            try:
                unique_code = int(unique_code.strip())
                if unique_code in users['code'].values:
                    st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                    st.session_state.page = "assessment"  # Change to assessment page
                    st.rerun()  # Rerun to refresh the view
                else:
                    st.error("Invalid code. Please try again.")
            except ValueError:
                st.error("Please enter a valid code.")
        else:
            st.error("Please enter a code.")

# Function to display the assessment page
def display_assessment():
    st.write(f"Welcome {st.session_state.user_name}! Here is the assessment.")

    # Read and display the text from ptinfo.docx
    docx_file_path = "ptinfo.docx"
    document_text = read_word_text(docx_file_path)
    
    if document_text:
        st.write("Patient Information:")
        st.text(document_text)  # Display the text content
    else:
        st.write("No text found in the document.")

if __name__ == "__main__":
    main()


