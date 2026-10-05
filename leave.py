from database import get_connection


# ============================================================
# CORE FUNCTIONS
# Used by BOTH terminal and web
# ============================================================

def create_leave(user_id, leave_type, start_date, end_date, reason):

    conn = get_connection()
    cursor = conn.cursor()

    # Find employee linked to this user
    cursor.execute(
        """
        SELECT employee_id
        FROM employees
        WHERE user_id = %s
        """,
        (user_id,)
    )

    employee = cursor.fetchone()

    if not employee:

        cursor.close()
        conn.close()

        return None

    employee_id = employee[0]

    query = """
        INSERT INTO leave_records
        (employee_id, leave_type, start_date, end_date, reason)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            employee_id,
            leave_type,
            start_date,
            end_date,
            reason
        )
    )

    leave_id = cursor.lastrowid

    conn.commit()

    cursor.close()
    conn.close()

    return leave_id


def get_leaves():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            l.leave_id,
            l.employee_id,
            e.first_name,
            e.last_name,
            l.leave_type,
            l.start_date,
            l.end_date,
            l.reason,
            l.status
        FROM leave_records l
        JOIN employees e
            ON l.employee_id = e.employee_id
        ORDER BY l.start_date DESC
    """

    cursor.execute(query)

    leaves = cursor.fetchall()

    cursor.close()
    conn.close()

    return leaves


def get_my_leave(user_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            l.leave_id,
            l.leave_type,
            l.start_date,
            l.end_date,
            l.reason,
            l.status
        FROM leave_records l
        JOIN employees e
            ON l.employee_id = e.employee_id
        WHERE e.user_id = %s
        ORDER BY l.start_date DESC
    """

    cursor.execute(
        query,
        (user_id,)
    )

    leaves = cursor.fetchall()

    cursor.close()
    conn.close()

    return leaves


def change_leave_status(leave_id, status):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE leave_records
        SET status = %s
        WHERE leave_id = %s
    """

    cursor.execute(
        query,
        (
            status,
            leave_id
        )
    )

    affected_rows = cursor.rowcount

    conn.commit()

    cursor.close()
    conn.close()

    return affected_rows


# ============================================================
# TERMINAL FUNCTIONS
# Keeps main.py working
# ============================================================

def apply_leave(user_id):

    print("\n===== APPLY LEAVE =====")

    leave_type = input(
        "Enter leave type: "
    )

    start_date = input(
        "Enter start date (YYYY-MM-DD): "
    )

    end_date = input(
        "Enter end date (YYYY-MM-DD): "
    )

    reason = input(
        "Enter reason: "
    )

    try:

        leave_id = create_leave(
            user_id,
            leave_type,
            start_date,
            end_date,
            reason
        )

        if leave_id is None:

            print(
                "No employee is linked to this account."
            )

            return

        print(
            "\nLeave application submitted successfully!"
        )

        print(
            "Leave ID:",
            leave_id
        )

    except Exception as e:

        print("Error:", e)


def view_leaves():

    print("\n===== ALL LEAVE RECORDS =====")

    try:

        leaves = get_leaves()

        if not leaves:

            print("No leave records found.")
            return

        for leave in leaves:

            print("-" * 55)

            print(
                "Leave ID:",
                leave["leave_id"]
            )

            print(
                "Employee ID:",
                leave["employee_id"]
            )

            print(
                "Employee:",
                leave["first_name"],
                leave["last_name"]
            )

            print(
                "Leave Type:",
                leave["leave_type"]
            )

            print(
                "Start Date:",
                leave["start_date"]
            )

            print(
                "End Date:",
                leave["end_date"]
            )

            print(
                "Reason:",
                leave["reason"]
            )

            print(
                "Status:",
                leave["status"]
            )

    except Exception as e:

        print("Error:", e)


def my_leave(user_id):

    print("\n===== MY LEAVE =====")

    try:

        leaves = get_my_leave(user_id)

        if not leaves:

            print("No leave records found.")
            return

        for leave in leaves:

            print("-" * 50)

            print(
                "Leave ID:",
                leave["leave_id"]
            )

            print(
                "Leave Type:",
                leave["leave_type"]
            )

            print(
                "Start Date:",
                leave["start_date"]
            )

            print(
                "End Date:",
                leave["end_date"]
            )

            print(
                "Reason:",
                leave["reason"]
            )

            print(
                "Status:",
                leave["status"]
            )

    except Exception as e:

        print("Error:", e)


def update_leave_status():

    print("\n===== UPDATE LEAVE STATUS =====")

    leave_id = input(
        "Enter leave ID: "
    )

    status = input(
        "Enter new status (Approved/Rejected/Pending): "
    )

    try:

        affected_rows = change_leave_status(
            leave_id,
            status
        )

        if affected_rows == 0:

            print("Leave record not found.")

        else:

            print(
                "Leave status updated successfully."
            )

    except Exception as e:

        print("Error:", e)