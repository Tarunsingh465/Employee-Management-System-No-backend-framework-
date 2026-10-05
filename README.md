# Employee Management System

Core Python + MySQL + bcrypt. No Flask, Django, FastAPI, HTML, CSS or JavaScript.

## Fresh setup

1. Run database.sql in MySQL Workbench.
2. Edit config.py and set your MySQL password.
3. Install:
   pip install -r requirements.txt
4. Create the first admin:
   python create_admin.py
5. Run:
   python main.py

## Existing database

If employee_management_db already exists, do NOT run database.sql blindly.

First run:
DESCRIBE employees;

If user_id is missing, run migrate_existing.sql.

Then connect the correct existing employee login:
SELECT user_id, username, role FROM users;
SELECT employee_id, first_name, last_name, email FROM employees;

Example:
UPDATE employees SET user_id = 2 WHERE employee_id = 3;

## Registration

The admin must first add an employee with an email.

The employee then chooses Employee Registration and enters that same email.
The account is automatically created with role = employee and linked to that employee.

Passwords are hashed with bcrypt before storage.

## Access

Admin:
- Full employee CRUD
- Departments
- Attendance
- View all leaves
- Approve/reject leaves

Employee:
- Own profile
- Own attendance
- Apply for own leave
- View own leave
