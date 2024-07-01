import streamlit as st
import sqlite3
import hashlib
import pandas as pd
from datetime import date
import streamlit_authenticator as stauth



def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_company_exists():
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Companies")
    result = c.fetchone()
    conn.close()
    return result is not None

def register_company(company_name, username, password):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO Companies (company_name) VALUES (?)", (company_name,))
        company_id = c.lastrowid
        c.execute("INSERT INTO HR_Managers (username, password, company_id) VALUES (?, ?, ?)",
                  (username, hash_password(password), company_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_hr(username, password):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM HR_Managers WHERE username = ? AND password = ?",
              (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result
def login_user(username, password):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Users WHERE username = ? AND password = ?",
              (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result

def register_user(username, password, company_id):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO Users (username, password, company_id) VALUES (?, ?, ?)",
                  (username, hash_password(password), company_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_companies():
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("SELECT company_id, company_name FROM Companies")
    companies = c.fetchall()
    conn.close()
    return companies

def get_users_by_company(company_id):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("SELECT username FROM Users WHERE company_id = ?", (company_id,))
    users = c.fetchall()
    conn.close()
    return [user[0] for user in users]

def insert_employee_request(username, name, employee_id, job_title, leave_days, from_date, to_date, leave_type, reason, main_type):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("INSERT INTO Employees_Requests (Username, Name, Employee_id, Job_title, Leave_request_days, from_date, to_date, Type_of_leave, Reason, main_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (username, name, employee_id, job_title, leave_days, from_date, to_date, leave_type, reason, main_type))
    conn.commit()
    conn.close()

def fetch_all_employee_requests():
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("SELECT *, main_type FROM Employees_Requests")
    rows = c.fetchall()
    conn.close()
    return rows

# def insert_leave_status(username, name, employee_id, leave_status):
#     conn = sqlite3.connect('hr_system.db')
#     c = conn.cursor()
#     c.execute("INSERT INTO Leave_Status VALUES (?, ?, ?, ?)",
#               (username, name, employee_id, leave_status))
#     conn.commit()
#     conn.close()

# def get_leave_status(employee_id):
#     conn = sqlite3.connect('hr_system.db')
#     c = conn.cursor()
#     c.execute("SELECT Leave_status FROM Leave_Status WHERE Employee_id = ?", (employee_id,))
#     result = c.fetchone()
#     conn.close()
#     return result[0] if result else None

def get_leave_status(employee_id, from_date, to_date, leave_type):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("SELECT Leave_status FROM Leave_Status WHERE Employee_id = ? AND from_date = ? AND to_date = ? AND leave_type = ?", (employee_id, from_date, to_date, leave_type))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None



def insert_leave_status(username, name, employee_id, leave_status, from_date, to_date, leave_type):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("INSERT INTO Leave_Status (Username, Name, Employee_id, Leave_status, from_date, to_date, leave_type) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (username, name, employee_id, leave_status, from_date, to_date, leave_type))
    conn.commit()
    conn.close()