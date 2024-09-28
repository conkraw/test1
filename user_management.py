import pandas as pd
import streamlit as st

@st.cache_data
def load_users():
    return pd.read_csv('users.csv')

def welcome_page():
    st.markdown("<h3>Welcome to the Pediatric Clerkship Assessment!</h3>", unsafe_allow_html=True)
    st.markdown("<p>This assessment is designed to evaluate your clinical reasoning skills.</p>", unsafe_allow_html=True)
    st.markdown("<h4>Instructions:</h4>", unsafe_allow_html=True)
    st.markdown("<p>Please enter your unique code on the next page.</p>", unsafe_allow_html=True)

    if st.button("Next"):
        st.session_state.page = "login"
        st.rerun()

def login_page(users):
    st.markdown("<p>Please enter your unique code to access the assessment.</p>", unsafe_allow_html=True)
    unique_code = st.text_input("Unique Code:")

    if st.button("Submit"):
        if unique_code:
            try:
                unique_code = int(unique_code.strip())
                if unique_code in users['code'].values:
                    st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                    st.session_state.unique_code = unique_code
                    st.session_state.page = "assessment"
                    st.rerun()
                else:
                    st.error("Invalid code. Please try again.")
            except ValueError:
                st.error("Please enter a valid code.")
        else:
            st.error("Please enter a code.")
