import streamlit as st
from helperfunctions import *


def employee_dashboard(username):

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_type = None
        st.experimental_rerun()

    st.title("Employee Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["Vacation Leave Request","Absence Leave Request", "View Leave Status"])
    
    with tab1:
        main_type = "VacationLeave"
        st.header("Vacation Leave Request")
        name = st.text_input("Name")
        employee_id = st.text_input("Employee ID")
        job_title = st.text_input("Job title")
        leave_days = st.number_input("Leave request Days", min_value=1, value=1)
        from_date = st.date_input("Dates of absence: From")
        to_date = st.date_input("To")
        leave_type = st.selectbox("Type of leave", ["Paid Leave", "Unpaid Leave", "Other"])
        reason = st.text_area("Reason for the Leave")

        if st.button("Submit request"):
            insert_employee_request(username, name, employee_id, job_title, str(leave_days), str(from_date), str(to_date), leave_type, reason, main_type)
            st.success("Request submitted successfully")
    with tab2:
        main_type = "AbsenceLeave"
        st.header("Absence Leave Request")
        name = st.text_input("Name ")
        employee_id = st.text_input("Employee ID ")
        job_title = st.text_input("Job title ")
        type_of_absence = st.selectbox("Type of Absence", ["Paid Leave", "Unpaid Leave", "Sick", "Appointment", "Other"])

        if(type_of_absence == "Appointment"):
            st.write("Please provide the following Appointment information:")
            from_date = st.date_input("Appointment from")
            to_date = st.date_input("Appointment till")
        elif (type_of_absence == "Other"):
            st.write("Please provide the following Other information:")
            st.text_area("Reason for the Absence")
        from_date = st.date_input("From ")
        to_date = st.date_input("To ")
        reason = st.text_area("Reason for the Absence ")

        if st.button("Submit request "):
            insert_employee_request(username, name, employee_id, job_title, "0", str(from_date), str(to_date), type_of_absence, reason, main_type)    
            st.success("Request submitted successfully")
    with tab3:
        st.header("My Leave Requests")
        requests = fetch_all_employee_requests()
        my_requests = [req for req in requests if req[0] == username]
        
        if my_requests:
            for req in my_requests:
                status = get_leave_status(req[2], req[5], req[6], req[7])
                st.write(f"**Request for {req[1]}**")
                st.write(f"Main Type: {req[10]}")
                st.write(f"From: {req[5]} To: {req[6]}")
                st.write(f"Type: {req[7]}")
                st.write(f"**Status: {status if status else 'Pending'}**")
                st.write("---")
        else:
            st.info("You haven't submitted any leave requests yet.")