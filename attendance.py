from database import get_connection


# ============================================================
# CORE FUNCTIONS
# Used by BOTH terminal and web
# ============================================================

def create_attendance(employee_id, attendance_date, status):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO attendance
        (employee_id, attendance_date, status)
        VALUES (%s, %s, %s)
    """

    cursor.execute(
        query,
        (
            employee_id,
            attendance_date,
            status
        )
    )

    attendance_id = cursor.lastrowid

    conn.commit()

    cursor.close()
    conn.close()

    return attendance_id


def get_attendance():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            a.attendance_id,
            a.employee_id,
            e.first_name,
            e.last_name,
            a.attendance_date,
            a.status
        FROM attendance a
        JOIN employees e
            ON a.employee_id = e.employee_id
        ORDER BY a.attendance_date DESC
    """

    cursor.execute(query)

    attendance = cursor.fetchall()

    cursor.close()
    conn.close()

    return attendance


# ============================================================
# TERMINAL FUNCTIONS
# Keeps main.py working
# ============================================================

def mark_attendance():

    print("\n===== MARK ATTENDANCE =====")

    employee_id = input(
        "Enter employee ID: "
    )

    attendance_date = input(
        "Enter attendance date (YYYY-MM-DD): "
    )

    status = input(
        "Enter status (Present/Absent): "
    )

    try:

        attendance_id = create_attendance(
            employee_id,
            attendance_date,
            status
        )

        print("\nAttendance marked successfully!")
        print("Attendance ID:", attendance_id)

    except Exception as e:

        print("\nError:", e)


def view_attendance():

    print("\n===== ATTENDANCE =====")

    try:

        attendance = get_attendance()

        if not attendance:

            print("No attendance records found.")
            return

        for record in attendance:

            print("-" * 50)

            print(
                "Attendance ID:",
                record["attendance_id"]
            )

            print(
                "Employee ID:",
                record["employee_id"]
            )

            print(
                "Employee:",
                record["first_name"],
                record["last_name"]
            )

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