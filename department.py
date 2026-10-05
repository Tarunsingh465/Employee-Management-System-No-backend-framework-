from database import get_connection


# ============================================================
# CORE FUNCTIONS
# Used by BOTH terminal and web
# ============================================================

def create_department(department_name, location):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO departments
        (department_name, location)
        VALUES (%s, %s)
    """

    cursor.execute(
        query,
        (department_name, location)
    )

    department_id = cursor.lastrowid

    conn.commit()

    cursor.close()
    conn.close()

    return department_id


def get_departments():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            department_id,
            department_name,
            location
        FROM departments
        ORDER BY department_id
    """

    cursor.execute(query)

    departments = cursor.fetchall()

    cursor.close()
    conn.close()

    return departments


# ============================================================
# TERMINAL FUNCTIONS
# Keeps main.py working
# ============================================================

def add_department():

    print("\n===== ADD DEPARTMENT =====")

    department_name = input(
        "Enter department name: "
    )

    location = input(
        "Enter location: "
    )

    try:

        department_id = create_department(
            department_name,
            location
        )

        print("\nDepartment added successfully!")
        print("Department ID:", department_id)

    except Exception as e:

        print("\nError:", e)


def view_departments():

    print("\n===== DEPARTMENTS =====")

    try:

        departments = get_departments()

        if not departments:

            print("No departments found.")
            return

        for department in departments:

            print("-" * 40)

            print(
                "ID:",
                department["department_id"]
            )

            print(
                "Department:",
                department["department_name"]
            )

            print(
                "Location:",
                department["location"]
            )

    except Exception as e:

        print("Error:", e)