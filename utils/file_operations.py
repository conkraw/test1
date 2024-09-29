# utils/file_operations.py

import pandas as pd

def load_users():
    return pd.read_csv('users.csv')
    
def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return None

def load_vital_signs(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read().splitlines()
            vital_signs = {}
            for line in data:
                key, value = line.split(':')
                vital_signs[key.strip()] = value.strip()
            return vital_signs
    except FileNotFoundError:
        return None

def read_diagnoses_from_file():
    try:
        with open('dx_list.txt', 'r') as file:
            diagnoses = [line.strip() for line in file.readlines() if line.strip()]
        return diagnoses
    except Exception as e:
        st.error(f"Error reading dx_list.txt: {e}")
        return []
