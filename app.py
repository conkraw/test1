import streamlit as st
import pandas as pd

# Set page layout to wide
st.set_page_config(layout="wide")

# Cache loading of users from CSV
@st.cache_data
def load_users():
    return pd.read_csv('users.csv')

# Function to read text from a TXT file
def read_text_file(txt_file_path):
    with open(txt_file_path, 'r') as file:
        return file.read()

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
    elif st.session_state.page == "login":
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
        st.rerun()  # Rerun to refresh the view

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

    # Read and display the text from ptinfo.txt
    txt_file_path = "ptinfo.txt"
    document_text = read_text_file(txt_file_path)
    
    if document_text:
        title_html = """
        <h2 style="font-family: 'DejaVu Sans'; font-size: 24px; margin-bottom: 10px; color: #2c3e50;">
            Patient Information:
        </h2>
        """
        st.markdown(title_html, unsafe_allow_html=True)

        custom_html = f"""
        <div style="font-family: 'DejaVu Sans'; font-size: 18px; line-height: 1.5; color: #34495e; background-color: #ecf0f1; padding: 15px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            {document_text.replace('\n', '<br>')}
        </div>
        """
        st.markdown(custom_html, unsafe_allow_html=True)
    else:
        st.write("No text found in the document.")

if __name__ == "__main__":
    main()


