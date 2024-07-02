import streamlit as st
import pandas as pd
from helperfunctions import *
import os
import pdfkit
from datetime import datetime
from datetime import date 
from io import BytesIO
import base64
def manager_dashboard(username):
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_type = None
        st.experimental_rerun()

    st.title("Manager Dashboard")
    
    # Fetch all requests
    requests = fetch_all_employee_requests()
    # requests.reverse()
    tab1, tab2 = st.tabs(["Pending Leave Requests", "Employee Contract"])

    with tab1:
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
                
                st.table(df[["Name", "Employee ID","Job Title", "Leave Days", "From", "To", "Leave Type", "Main Type", "Reason", "Status", "Request ID"]])
                
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

    with tab2:
        def get_binary_file_downloader_html(bin_data, file_label='File', btn_label='Download', file_name='file.pdf'):
            bin_str = base64.b64encode(bin_data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_name}">{btn_label}</a>'
            return href
        st.header("Employment Contract Form")
        
        contract_date = st.date_input("Contract Date")
        employee_name = st.text_input("Employee Name")
        national_id = st.text_input("National ID Number")
        
        # Text area for agreed terms
        agreed_terms = st.text_area("Terms of Agreement", height=300, 
                                    value="""1. The second party is committed to working for the first party in the profession of [JOB TITLE].
                                    2. The duration of this contract is [DURATION] starting from [START DATE].
                                    3. The second party's salary is a monthly total of [TOTAL SALARY] Saudi riyals.
                                    4. [ADD MORE TERMS AS NEEDED]

                                    The parties agree to abide by these terms and conditions.""")
    
        if st.button("Generate Contract PDF"):
            # Create the HTML content (use the html_content string from above)
            html_content = f"""
                <html>
                <head>
                    <style>
                        body {{ font-family: 'Arial', sans-serif; margin: 0; padding: 20px; font-size: 12pt; color: #333; }}
                        .form-container {{ max-width: 100%; margin: auto; padding: 0; }}
                        .header {{ background-color: #f0f0f0; padding: 20px; margin: -30px -30px 20px -30px; border-bottom: 2px solid #ddd; }}
                        h2 {{ font-size: 24pt; margin: 0; color: #2c3e50; }}
                        .section {{ max-width: 100%; margin-bottom: 5px; padding-bottom: 5px; border-bottom: 1px solid #eee; }}
                        .section {{max-width: 100%; background-color: #f0f0f0;padding: 10px;border: 1px solid #ccc;border-radius: 5px;margin-bottom: 10px;}}
                        .field {{ margin-bottom: 12px; display: flex; align-items: center; }}
                        .label {{ font-weight: bold; width: 200px; color: #34495e; }}
                        .value {{ flex: 1; }}
                        .signature-line {{ border-top: 1px solid #999; width: 300px; display: inline-block; margin-left: 10px; }}
                        h3 {{ font-size: 16pt; color: #2980b9; margin-bottom: 15px; }}
                        .note {{ font-style: italic; font-size: 10pt; color: #7f8c8d; }}
                        .terms {{ white-space: pre-wrap; }}
                    </style>
                </head>
                <body>
                    <div class="form-container">
                        <div class="header">
                            <h2>Employment Contract</h2>
                        </div>

                        <div class="section">
                            <p>On {contract_date}, an agreement has been made between:</p>
                            <div class="field"><span class="label">First party:</span> <span class="value">Real Energy Sources Contracting Establishment</span></div>
                            <div class="field"><span class="label">Second party:</span> <span class="value">{employee_name}</span></div>
                            <div class="field"><span class="label">National ID No.:</span> <span class="value">{national_id}</span></div>
                        </div>

                        <div class="section">
                            <h3>Terms of Agreement</h3>
                            <div class="terms">{agreed_terms}</div>
                        </div>

                        <div class="section">
                            <div class="field">
                                <span class="label">First party name:</span> 
                                <span class="value">Real Energy Sources Contracting Establishment</span>
                            </div>
                            <div class="field">
                                <span class="label">First party signature:</span> 
                                <span class="signature-line"></span>
                            </div>
                        </div>

                        <div class="section">
                            <div class="field">
                                <span class="label">Second party name:</span> 
                                <span class="value">{employee_name}</span>
                            </div>
                            <div class="field">
                                <span class="label">Second party signature:</span> 
                                <span class="signature-line"></span>
                            </div>
                        </div>
                    </div>
                </body>
                </html>
            """
            # pdf_filename = f"Employment_Contract_{employee_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            # pdf_path = os.path.join(save_directory, pdf_filename)
            # # Save the HTML content as a PDF
            # # pdfkit.from_string(html_content, pdf_path, configuration=config)
            # pdfkit.from_string(html_content, pdf_path)
    
            # st.success(f"Employment Contract saved as PDF: {pdf_path}")
            options = {
                'page-size': 'A4',
                'margin-top': '0.5in',
                'margin-right': '0.5in',
                'margin-bottom': '0.5in',
                'margin-left': '0.5in',
                'encoding': "UTF-8",
                'no-outline': None
            }
            
            # Generate PDF in memory
            pdf_data = pdfkit.from_string(html_content, False, options=options)
            
            # Offer the PDF as a download
            st.markdown(get_binary_file_downloader_html(pdf_data, 'Contract.pdf', 'Download PDF'), unsafe_allow_html=True)

