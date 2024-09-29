# utils/file_operations.py

import pandas as pd

def load_users():
    # Your code to load users
    pass

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
