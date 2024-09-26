import os
import streamlit as st

# Function to load physical examination components from a text file
def load_phys_exam_components(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

# Load physical examination components
phys_exam_components = load_phys_exam_components('phys_exam.txt')

# Information prompt
st.header("Physical Examination Components")
st.write("Please select and review the physical examination components to help develop your differential diagnosis. Please note that any image provided requires interpretation.")

# Options for physical examination components
options = [
    "General Appearances", "Eyes", "Ears, Neck, Nose, Throat",
    "Lymph Nodes", "Cardiovascular", "Lungs", "Abdomen",
    "Skin", "Extremities", "Musculoskeletal", "Neurological",
    "Psychiatry", "Genitourinary", "Image"
]

# User selection
selected_option = st.selectbox("Select a component:", options)

# Display selected component description
if selected_option in phys_exam_components:
    index = options.index(selected_option)
    st.write(phys_exam_components[index])  # Display corresponding description

# Check for image files named 'image_1' with any common extension
image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
base_image_name = 'image_1'
image_found = False

for ext in image_extensions:
    image_file = f"{base_image_name}{ext}"
    if os.path.isfile(image_file):
        st.image(image_file)
        image_found = True
        break  # Exit loop if an image is found

if not image_found:
    st.write("No image file named 'image_1' found.")

