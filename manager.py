# import streamlit as st
# from helperfunctions import *

# def manager_dashboard(username):

#     if st.sidebar.button("Logout"):
#         st.session_state.logged_in = False
#         st.session_state.username = None
#         st.session_state.user_type = None
#         st.experimental_rerun()


#     st.title("Manager Dashboard")
    
#     # Fetch all requests
#     requests = fetch_all_employee_requests()
    
#     if requests:
#         st.write("### Pending Leave Requests")
        
#         # Create a table to display requests
#         request_data = []
#         for req in requests:
#             status = get_leave_status(req[2])
#             if status is None:
#                 request_data.append({
#                     "Name": req[1],
#                     "Employee ID": req[2],
#                     "Leave Type": req[7],
#                     "Main Type": req[10],
#                     "From": req[5],
#                     "To": req[6],
#                     "Status": "Pending"
#                 })
        
#         if request_data:
#             df = pd.DataFrame(request_data)
#             st.table(df)
            
#             # Process requests
#             selected_request = st.selectbox("Select a request to process:", df["Employee ID"].tolist())
#             action = st.radio("Choose an action:", ("Approve", "Reject"))
            
#             if st.button("Process Request"):
#                 selected_row = df[df["Employee ID"] == selected_request].iloc[0]
#                 insert_leave_status(username, selected_row["Name"], selected_request, action)
#                 st.success(f"Request for {selected_row['Name']} has been {action.lower()}ed.")
#                 st.experimental_rerun()

        
#         else:
#             st.info("No pending requests to process.")
#     else:
        # st.info("No leave requests found.")

#--------------------------------
import streamlit as st
import pandas as pd
from helperfunctions import *

def manager_dashboard(username):
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_type = None
        st.experimental_rerun()

    st.title("Manager Dashboard")
    
    # Fetch all requests
    requests = fetch_all_employee_requests()
    
    if requests:
        st.write("### Pending Leave Requests")
        
        # Create a table to display requests
        request_data = []
        for req in requests:
            status = get_leave_status(req[2], req[5], req[6], req[7])
            if status is None:
                request_data.append({
                    "Name": req[1],
                    "Employee ID": req[2],
                    "Job Title": req[3],
                    "Leave Days": req[4],
                    "From": req[5],
                    "To": req[6],
                    "Leave Type": req[7],
                    "Reason": req[8],
                    "Main Type": req[10],
                    "Status": "Pending",
                    "Request ID": f"{req[2]}_{req[5]}_{req[6]}_{req[7]}"  # Unique identifier
                })
        
        if request_data:
            df = pd.DataFrame(request_data)
            st.table(df[["Name", "Employee ID", "From", "To", "Leave Type", "Main Type", "Reason"]])
            
            # Process requests
            request_options = [f"{row['Request ID']} - {row['Name']} - {row['Main Type']} - {row['From']} to {row['To']} - {row['Reason'][:30]}..." for _, row in df.iterrows()]
            selected_request = st.selectbox("Select a request to process:", request_options)
            
            selected_request_id = selected_request.split(' - ')[0]
            selected_row = df[df["Request ID"] == selected_request_id].iloc[0]
            
            action = st.radio("Choose an action:", ("Approve", "Reject"))
            
            if st.button("Process Request"):
                insert_leave_status(username, selected_row["Name"], selected_row["Employee ID"], action, selected_row["From"], selected_row["To"], selected_row["Leave Type"])
                st.success(f"Request for {selected_row['Name']} ({selected_row['Leave Type']} from {selected_row['From']} to {selected_row['To']}) has been {action.lower()}ed.")
                st.experimental_rerun()

        else:
            st.info("No pending requests to process.")
    else:
        st.info("No leave requests found.")