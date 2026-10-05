from database import get_connection


# ============================================================
# CORE FUNCTIONS
# These functions can be used by BOTH terminal and web
# ============================================================

def create_employee(first_name, last_name, email, phone,
                    job_title, salary, hire_date, department_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO employees
        (first_name, last_name, email, phone, job_title,
         salary, hire_date, department_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        first_name,
        last_name,
        email,
        phone,
        job_title,
        salary,
        hire_date,
        department_id
    )

    cursor.execute(query, values)

    employee_id = cursor.lastrowid

    conn.commit()

    cursor.close()
    conn.close()

    return employee_id


def get_employees(search=""):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if search:

        query = """
            SELECT
                e.employee_id,
                e.first_name,
                e.last_name,
                e.email,
                e.phone,
                e.job_title,
                e.salary,
                e.hire_date,
                e.status,
                d.department_name
            FROM employees e
            LEFT JOIN departments d
                ON e.department_id = d.department_id
            WHERE e.first_name LIKE %s
               OR e.last_name LIKE %s
               OR e.email LIKE %s
        """

        search_value = "%" + search + "%"

        cursor.execute(
            query,
            (search_value, search_value, search_value)
        )

    else:

        query = """
            SELECT
                e.employee_id,
                e.first_name,
                e.last_name,
                e.email,
                e.phone,
                e.job_title,
                e.salary,
                e.hire_date,
                e.status,
                d.department_name
            FROM employees e
            LEFT JOIN departments d
                ON e.department_id = d.department_id
        """

        cursor.execute(query)

    employees = cursor.fetchall()

    cursor.close()
    conn.close()

    return employees


def update_employee_data(employee_id, salary, status):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE employees
        SET salary = %s,
            status = %s
        WHERE employee_id = %s
    """

    cursor.execute(
        query,
        (salary, status, employee_id)
    )

    affected_rows = cursor.rowcount

    conn.commit()

    cursor.close()
    conn.close()

    return affected_rows


def delete_employee_data(employee_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        DELETE FROM employees
        WHERE employee_id = %s
    """

    cursor.execute(query, (employee_id,))

    affected_rows = cursor.rowcount

    conn.commit()

    cursor.close()
    conn.close()

    return affected_rows


def get_my_profile(user_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            e.employee_id,
            e.first_name,
            e.last_name,
            e.email,
            e.phone,
            e.job_title,
            e.salary,
            e.hire_date,
            e.status,
            d.department_name
        FROM employees e
        LEFT JOIN departments d
            ON e.department_id = d.department_id
        WHERE e.user_id = %s
    """

    cursor.execute(query, (user_id,))

    employee = cursor.fetchone()

    cursor.close()
    conn.close()

    return employee


def get_my_attendance(user_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            a.attendance_id,
            a.attendance_date,
            a.status
        FROM attendance a
        JOIN employees e
            ON a.employee_id = e.employee_id
        WHERE e.user_id = %s
        ORDER BY a.attendance_date DESC
    """

    cursor.execute(query, (user_id,))

    attendance = cursor.fetchall()

    cursor.close()
    conn.close()

    return attendance


# ============================================================
# TERMINAL FUNCTIONS
# These keep your existing main.py working
# ============================================================

def add_employee():

    print("\n===== ADD EMPLOYEE =====")

    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    phone = input("Enter phone: ")
    job_title = input("Enter job title: ")
    salary = input("Enter salary: ")
    hire_date = input("Enter hire date (YYYY-MM-DD): ")
    department_id = input("Enter department ID: ")

    try:

        employee_id = create_employee(
            first_name,
            last_name,
            email,
            phone,
            job_title,
            salary,
            hire_date,
            department_id
        )

        print("\nEmployee added successfully!")
        print("Employee ID:", employee_id)

    except Exception as e:

        print("\nError:", e)


def view_employees():

    print("\n===== EMPLOYEES =====")

    try:

        employees = get_employees()

        if not employees:
            print("No employees found.")
            return

        for employee in employees:

            print("-" * 50)

            print(
                "ID:",
                employee["employee_id"]
            )

            print(
                "Name:",
                employee["first_name"],
                employee["last_name"]
            )

            print(
                "Email:",
                employee["email"]
            )

            print(
                "Phone:",
                employee["phone"]
            )

            print(
                "Job Title:",
                employee["job_title"]
            )

            print(
                "Salary:",
                employee["salary"]
            )

            print(
                "Hire Date:",
                employee["hire_date"]
            )

            print(
                "Department:",
                employee["department_name"]
            )

            print(
                "Status:",
                employee["status"]
            )

    except Exception as e:

        print("Error:", e)


def search_employee():

    print("\n===== SEARCH EMPLOYEE =====")

    search = input(
        "Enter first name, last name or email: "
    )

    try:

        employees = get_employees(search)

        if not employees:
            print("No employees found.")
            return

        for employee in employees:

            print("-" * 50)

            print(
                "ID:",
                employee["employee_id"]
            )

            print(
                "Name:",
                employee["first_name"],
                employee["last_name"]
            )

            print(
                "Email:",
                employee["email"]
            )

            print(
                "Job Title:",
                employee["job_title"]
            )

            print(
                "Department:",
                employee["department_name"]
            )

            print(
                "Status:",
                employee["status"]
            )

    except Exception as e:

        print("Error:", e)


def update_employee():

    print("\n===== UPDATE EMPLOYEE =====")

    employee_id = input("Enter employee ID: ")
    salary = input("Enter new salary: ")
    status = input("Enter new status: ")

    try:

        affected_rows = update_employee_data(
            employee_id,
            salary,
            status
        )

        if affected_rows == 0:

            print("Employee not found.")

        else:

            print("Employee updated successfully.")

    except Exception as e:

        print("Error:", e)


def delete_employee():

    print("\n===== DELETE EMPLOYEE =====")

    employee_id = input("Enter employee ID: ")

    confirmation = input(
        "Are you sure you want to delete this employee? (y/n): "
    )

    if confirmation.lower() != "y":

        print("Deletion cancelled.")
        return

    try:

        affected_rows = delete_employee_data(
            employee_id
        )

        if affected_rows == 0:

            print("Employee not found.")

        else:

            print("Employee deleted successfully.")

    except Exception as e:

        print("Error:", e)


def my_profile(user_id):

    try:

        employee = get_my_profile(user_id)

        if not employee:

            print("Employee profile not found.")
            return

        print("\n===== MY PROFILE =====")

        print("Employee ID:", employee["employee_id"])

        print(
            "Name:",
            employee["first_name"],
            employee["last_name"]
        )

        print("Email:", employee["email"])
        print("Phone:", employee["phone"])
        print("Job Title:", employee["job_title"])
        print("Salary:", employee["salary"])
        print("Hire Date:", employee["hire_date"])
        print("Department:", employee["department_name"])
        print("Status:", employee["status"])

    except Exception as e:

        print("Error:", e)


def my_attendance(user_id):

    try:

        attendance = get_my_attendance(user_id)

        print("\n===== MY ATTENDANCE =====")

        if not attendance:

            print("No attendance records found.")
            return

        for record in attendance:

            print("-" * 40)

            print(
                "Date:",
                record["attendance_date"]
            )

            print(
                "Status:",
                record["status"]
            )

    except Exception as e:

        print("Error:", e)