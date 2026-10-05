USE employee_management_db;

-- Run only if employees does not already have user_id.
ALTER TABLE employees ADD COLUMN user_id INT UNIQUE;

ALTER TABLE employees
ADD CONSTRAINT fk_employee_user
FOREIGN KEY (user_id) REFERENCES users(user_id)
ON DELETE SET NULL ON UPDATE CASCADE;

-- Then connect an existing login to its employee:
-- SELECT user_id, username, role FROM users;
-- SELECT employee_id, first_name, last_name, email FROM employees;
-- UPDATE employees SET user_id = 2 WHERE employee_id = 3;
