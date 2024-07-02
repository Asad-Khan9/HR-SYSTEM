import sqlite3

def init_db():
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Companies
                 (company_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  company_name TEXT NOT NULL UNIQUE)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS HR_Managers
                 (manager_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL UNIQUE,
                  password TEXT NOT NULL,
                  company_id INTEGER,
                  FOREIGN KEY (company_id) REFERENCES Companies(company_id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Users
                 (user_id INTEGER PRIMARY KEY AUTOINCREMENT,   
                  username TEXT NOT NULL UNIQUE,
                  password TEXT NOT NULL,
                  company_id INTEGER,
                  FOREIGN KEY (company_id) REFERENCES Companies(company_id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Employees_Requests (
                 Username TEXT NOT NULL,
                 Name TEXT NOT NULL,
                 Employee_id TEXT NOT NULL,
                 Job_title TEXT NOT NULL,
                 Leave_request_days TEXT NOT NULL,
                 from_date TEXT NOT NULL,
                 to_date TEXT NOT NULL,
                 Type_of_leave TEXT NOT NULL,
                 Reason TEXT NOT NULL,
                 main_type TEXT)''')
    
    # c.execute('''CREATE TABLE IF NOT EXISTS Leave_Status
    #              (Username TEXT NOT NULL,
    #               Name TEXT NOT NULL,
    #               Employee_id TEXT NOT NULL,
    #               Leave_status TEXT NOT NULL)''')
    # conn.commit()
    c.execute('''CREATE TABLE IF NOT EXISTS Leave_Status
             (Username TEXT NOT NULL,
              Name TEXT NOT NULL,
              Employee_id TEXT NOT NULL,
              Leave_status TEXT NOT NULL,
              from_date TEXT NOT NULL,
              to_date TEXT NOT NULL,
              leave_type TEXT NOT NULL)''')
    conn.close()
