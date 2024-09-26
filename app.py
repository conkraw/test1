import streamlit as st
import pandas as pd
from docx import Document

# Set page layout to wide
st.set_page_config(layout="wide")

# Cache loading of users from CSV
@st.cache_data
def load_users():
    return pd.read_csv('users.csv')

# Function to read the Word document and extract the table
def read_word_table(docx_file_path):
    doc = Document(docx_file_path)
    table_data = []
    
    # Assuming the table is the first one in the document
    table = doc.tables[0]
    
    for row in table.rows:
        row_data = [cell.text for cell in row.cells]
        table_data.append(row_data)
    
    return table_data

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

    # Read and display the table from ptinfo.docx
    docx_file_path = "ptinfo.docx"
    table_data = read_word_table(docx_file_path)
    
    if table_data:
        st.write("Table from Word Document:")
        st.table(table_data)
    else:
        st.write("No table found in the document.")

if __name__ == "__main__":
    main()


