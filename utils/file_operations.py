import pandas as pd
import streamlit as st

def load_users():
    return pd.read_csv('users.csv')

def read_text_file(txt_file_path):
    try:
        with open(txt_file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"File not found: {txt_file_path}. Please check the file path.")
        return ""
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return ""

def load_vital_signs(vital_signs_file):
    vital_signs = {}
    try:
        with open(vital_signs_file, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    key = parts[0].strip()  # Get type (e.g., heart_rate)
                    value = parts[1].strip()  # Get vital sign description
                    vital_signs[key] = value
    except FileNotFoundError:
        st.error(f"File not found: {vital_signs_file}. Please check the file path.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

    return vital_signs

def read_diagnoses_from_file():
    try:
        with open('dx_list.txt', 'r') as file:
            diagnoses = [line.strip() for line in file.readlines() if line.strip()]
        return diagnoses
    except Exception as e:
        st.error(f"Error reading dx_list.txt: {e}")
        return []
