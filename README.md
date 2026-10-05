# Employee Management System

A simple Employee Management System built with **Core Python + MySQL + HTML/CSS/JavaScript**.

This project does **not** use Flask, Django, FastAPI, or any other backend framework. The web application uses Python's built-in `http.server`.

## Features

- Admin and Employee login
- Bcrypt password hashing
- Role-based access
- Employee CRUD operations
- Department management
- Attendance management
- Leave application and approval
- Employee profile and personal attendance/leave view
- Terminal/CLI application
- Browser-based web application

## Tech Stack

- Python 3
- MySQL
- `mysql-connector-python`
- `bcrypt`
- HTML, CSS, JavaScript
- Python `http.server`

## Project Structure

```text
employee-management-system/
│
├── main.py              # Terminal application
├── server.py            # Core Python web server
├── config.py            # Database configuration
├── database.py          # MySQL connection
├── auth.py              # Login and registration
├── employee.py          # Employee operations
├── department.py        # Department operations
├── attendance.py        # Attendance operations
├── leave.py             # Leave operations
├── create_admin.py      # Create admin account
│
├── database.sql         # Database setup
├── migrate_existing.sql # Migration for existing databases
├── requirements.txt     # Python dependencies
│
└── static/
    ├── index.html
    ├── style.css
    └── app.js
```

## Requirements

Install:

- Python 3
- MySQL Server
- MySQL Workbench

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Tarunsingh465/Employee-Management-System-No-backend-framework-.git
cd Employee-Management-System-No-backend-framework-
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv mse
.\mse\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Create the database

Open **MySQL Workbench** and run:

```text
database.sql
```

This creates the `employee_management_db` database and required tables.

## Database Configuration

The MySQL password is read from the `DB_PASSWORD` environment variable.

In PowerShell:

```powershell
$env:DB_PASSWORD="YOUR_MYSQL_PASSWORD"
```

The `config.py` should use:

```python
import os

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = "employee_management_db"
```

**Do not put your actual MySQL password in `config.py` or commit it to GitHub.**

## Create Admin Account

Run:

```powershell
python create_admin.py
```

Enter the admin username and password when prompted.

Passwords are stored using bcrypt hashing.

## Run the Terminal Application

```powershell
python main.py
```

You can then log in as an admin or register an employee.

## Run the Web Application

Set the database password first if needed:

```powershell
$env:DB_PASSWORD="YOUR_MYSQL_PASSWORD"
```

Start the server:

```powershell
python server.py
```

Open your browser and go to:

```text
http://localhost:8000
```

## User Roles

### Admin

- Add, view, search, update and delete employees
- Add/view departments
- Mark/view attendance
- View leaves
- Approve/reject leaves

### Employee

- View own profile
- View own attendance
- Apply for leave
- View own leave

## Employee Registration

The admin must first create an employee record with an email.

The employee can then use **Employee Registration** with the same email to create their login account.

The account is automatically linked to that employee.

## Existing Database

If you already have an `employee_management_db` database, do **not** blindly run `database.sql`.

Check your existing structure first:

```sql
DESCRIBE employees;
```

If the existing database needs the newer employee/user relationship, check:

```text
migrate_existing.sql
```

## Security

- Passwords are hashed with bcrypt.
- SQL queries use parameterized values.
- Database passwords are kept outside the source code.
- `.gitignore` excludes virtual environments, Python cache files, `.env`, and other unnecessary files.

## Important

This project is designed for **local development and learning**. The web server uses Python's built-in `http.server` and is not intended as a production web server.

## Author

**Tarun Singh**

GitHub:  
https://github.com/Tarunsingh465