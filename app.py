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
        st.session_state.page = "welcome"  # Start on the welcome page

    # Check which page to display
    if st.session_state.page == "assessment":
        display_assessment()
    elif st.session_state.page == "welcome":
        welcome_page()
    else:
        login_page(users)

# Welcome page function
def welcome_page():
    st.write("Welcome to the Pediatric Clerkship Assessment!")
    st.write("This assessment is designed to evaluate your clinical reasoning skills.")
    st.write("### Instructions:")
    st.write("1. Please enter your unique code on the next page.")
    st.write("2. Follow the prompts to complete the assessment.")
    
    if st.button("Next"):
        st.session_state.page = "login"  # Change to login page
        st.experimental_rerun()  # Rerun to refresh the view

# Login page function
def login_page(users):
    st.write("Please enter your unique code to access the assessment.")
    unique_code = st.text_input("Unique Code:")
    
    if st.button("Submit"):
        if unique_code:
            try:
                unique_code = int(unique_code.strip())
                if unique_code in users['code'].values:
                    st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                    st.session_state.page = "assessment"  # Change to assessment page
                    st.experimental_rerun()  # Rerun to refresh the view
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
        # Custom HTML for "Patient Information" title
        title_html = """
        <h2 style="font-family: 'DejaVu Sans'; font-size: 24px; margin-bottom: 10px;">
            Patient Information:
        </h2>
        """
        st.markdown(title_html, unsafe_allow_html=True)

        # Use markdown with HTML for custom font and size for document text
        custom_html = f"""
        <div style="font-family: 'DejaVu Sans'; font-size: 18px;">
            {document_text.replace('\n', '<br>')}
        </div>
        """
        st.markdown(custom_html, unsafe_allow_html=True)
    else:
        st.write("No text found in the document.")

if __name__ == "__main__":
    main()
