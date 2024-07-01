import streamlit as st
import sqlite3
import hashlib
import pandas as pd
from datetime import date
import streamlit_authenticator as stauth
from helperfunctions import *
#----importing from local files-----
from employee import employee_dashboard
from manager import manager_dashboard
from database import init_db
#------------------------------
st.set_page_config(page_title="HR Management System", page_icon=":shark:")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

# Main Streamlit app
def main():
    st.title("HR Management System")

    init_db()

    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_type = None

    if not check_company_exists():
        st.header("Register Company")
        company_name = st.text_input("Company Name")
        username = st.text_input("HR Manager Username")
        password = st.text_input("Password", type="password")
        if st.button("Register Company"):
            if register_company(company_name, username, password):
                st.success("Company registered successfully!")
            else:
                st.error("Registration failed. Company or username may already exist.")

            if st.button("Go to HR Login"):
                st.experimental_rerun()



    elif not st.session_state.logged_in:
        st.markdown("""
            <style>
            .stRadio > label {
                background-color: #F9F3EA;
                padding: 10px;
                border-radius: 5px;
                width: 100%;
                margin-bottom: 10px;
            }
            .stRadio > label:hover {
                background-color: #CED8D0;
            }
            </style>
        """, unsafe_allow_html=True)
        with st.sidebar:
            st.image('login_image3.jpg')
        choice = st.sidebar.radio("**Menu**", ["HR Login", "User Login", "User Signup"])
        
        if choice == "HR Login":
            st.header("HR Manager Login")
            username = st.text_input("HR Username")
            password = st.text_input("HR Password", type="password")

            if st.button("HR Login"):
                result = login_hr(username, password)
                if result:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_type = "HR"
                    st.success(f"Logged in as HR: {username}")
                    st.experimental_rerun()
                else:
                    st.error("Incorrect username or password")


        elif choice == "User Signup":
            st.header("User Signup")
            username = st.text_input("New Username")
            password = st.text_input("New Password", type="password")
            companies = get_companies()
            company_names = [company[1] for company in companies]
            selected_company = st.selectbox("Select Company", company_names)
            company_id = next(company[0] for company in companies if company[1] == selected_company)
            if st.button("Sign Up"):
                if register_user(username, password, company_id):
                    st.success("User registered successfully!")
                else:
                    st.error("Registration failed. Username may already exist.")
        elif choice == "User Login":
            st.header("User Login")
            username = st.text_input("User Username")
            password = st.text_input("User Password", type="password")

            if st.button("User Login"):
                # Implement user login logic here
                result = login_user(username, password)
                if result:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_type = "User"
                    st.success(f"Logged in as User: {username}")
                    st.experimental_rerun()
                else:
                    st.error("Incorrect username or password")
            
    else:
        # User is logged in, show appropriate dashboard
        if st.session_state.user_type == "HR":
            manager_dashboard(st.session_state.username)
        else:
            employee_dashboard(st.session_state.username)

# Run the app

if __name__ == "__main__":
    main()