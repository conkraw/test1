# results.py

import streamlit as st
import os

def display_results_image(results_file_path='test1/utils/results.txt'):
    # Read the results from the text file
    with open(results_file_path, 'r') as file:
        results = [line.strip() for line in file.readlines()]

    # Create a dropdown in Streamlit for the user to select a result
    selected_result = st.selectbox("Select a result", results)

    # Prepare the corresponding image file name
    image_filename = selected_result.replace(" ", "_")  # Replace spaces with underscores
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', 
                       '.JPG', '.JPEG', '.PNG', '.GIF']  # Define possible extensions, including uppercase

    # Look for the image file in the same directory
    image_path = None
    for ext in image_extensions:
        potential_path = f"test1/utils/{image_filename}{ext}"
        if os.path.exists(potential_path):
            image_path = potential_path
            break

    # Display the selected result and the image
    if image_path:
        st.image(image_path, caption=selected_result, use_column_width=True)
    else:
        st.write("No image found for this result.")

    # Add a button to go to the next page
    if st.button("Next Page"):
        st.session_state.page = "Laboratory Features"  # Change to the Simple Success page
        st.rerun()  # Rerun to update the app

