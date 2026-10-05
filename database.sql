CREATE DATABASE IF NOT EXISTS employee_management_db;
USE employee_management_db;

CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'employee',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    department_name VARCHAR(100) UNIQUE NOT NULL,
    location VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS employees (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    job_title VARCHAR(100),
    salary DECIMAL(10,2),
    hire_date DATE,
    department_id INT,
    user_id INT UNIQUE,
    status VARCHAR(20) DEFAULT 'Active',
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS leave_records (
    leave_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    leave_type VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason VARCHAR(255),
    status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        ON DELETE CASCADE
);

INSERT IGNORE INTO departments (department_name, location) VALUES
('IT', 'Indore'),
('HR', 'Indore'),
('Finance', 'Bhopal'),
('Marketing', 'Indore');
