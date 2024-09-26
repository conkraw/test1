import streamlit as st
import pandas as pd
from docx import Document
from pdf2image import convert_from_path
import os

st.set_page_config(layout="wide")

# Load users from CSV
@st.cache_data
def load_users():
    return pd.read_csv('users.csv')

# Function to convert DOCX to PDF and then to images
def docx_to_images(docx_path):
    # Convert DOCX to PDF
    pdf_path = docx_path.replace(".docx", ".pdf")
    document = Document(docx_path)
    document.save(pdf_path)

    # Convert PDF to images
    images = convert_from_path(pdf_path)
    
    # Save images to a temporary directory
    image_paths = []
    for i, image in enumerate(images):
        image_path = f"temp_image_{i}.png"
        image.save(image_path, "PNG")
        image_paths.append(image_path)

    # Clean up the PDF file
    os.remove(pdf_path)

    return image_paths

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
            st.rerun()  # Rerun the app to show the new content

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
                        st.rerun()
                    else:
                        st.error("Invalid code. Please try again.")
                except ValueError:
                    st.error("Please enter a valid code.")
            else:
                st.error("Please enter a code.")

    # Display the assessment page if the flag is set
    if "show_assessment" in st.session_state and st.session_state.show_assessment:
        st.subheader("Assessment Document")
        # Convert the DOCX file to images and display them
        image_paths = docx_to_images("ptinfo.docx")
        
        for image_path in image_paths:
            st.image(image_path)

        # Clean up image files after displaying
        for image_path in image_paths:
            os.remove(image_path)

if __name__ == "__main__":
    main()

