import streamlit as st

def display_simple_success1():
    print("Displaying Simple Success page.")  # Debugging statement
    st.title("Success!")
    st.write("Your operation was successful1111.")
    
    if st.button("Final Submit"):
    session_data = collect_session_data()
    upload_message = upload_to_firebase(db, session_data)
    st.success(upload_message) 
