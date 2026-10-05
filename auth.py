import bcrypt

from database import get_connection


# ============================================================
# CORE FUNCTIONS
# Used by BOTH terminal and web
# ============================================================

def register_employee_account(username, password, email):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # ----------------------------------------------------
        # Find employee using email
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT employee_id, user_id
            FROM employees
            WHERE email = %s
            """,
            (email,)
        )

        employee = cursor.fetchone()

        if not employee:

            return {
                "success": False,
                "message": "No employee found with this email."
            }

        # ----------------------------------------------------
        # Check whether employee already has an account
        # ----------------------------------------------------

        if employee["user_id"] is not None:

            return {
                "success": False,
                "message": "An account already exists for this employee."
            }

        # ----------------------------------------------------
        # Check username
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE username = %s
            """,
            (username,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            return {
                "success": False,
                "message": "Username already exists."
            }

        # ----------------------------------------------------
        # Hash password using bcrypt
        # ----------------------------------------------------

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # ----------------------------------------------------
        # Create user account
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO users
            (username, password_hash, role)
            VALUES (%s, %s, %s)
            """,
            (
                username,
                password_hash,
                "employee"
            )
        )

        user_id = cursor.lastrowid

        # ----------------------------------------------------
        # Link account to employee
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE employees
            SET user_id = %s
            WHERE employee_id = %s
            """,
            (
                user_id,
                employee["employee_id"]
            )
        )

        conn.commit()

        return {
            "success": True,
            "message": "Registration successful.",
            "user_id": user_id,
            "role": "employee"
        }

    except Exception:

        conn.rollback()
        raise

    finally:

        cursor.close()
        conn.close()


def authenticate_user(username, password):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # ----------------------------------------------------
        # Find user
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                user_id,
                username,
                password_hash,
                role
            FROM users
            WHERE username = %s
            """,
            (username,)
        )

        user = cursor.fetchone()

        if not user:

            return {
                "success": False,
                "message": "Invalid username or password."
            }

        # ----------------------------------------------------
        # Verify bcrypt password
        # ----------------------------------------------------

        password_valid = bcrypt.checkpw(
            password.encode("utf-8"),
            user["password_hash"].encode("utf-8")
        )

        if not password_valid:

            return {
                "success": False,
                "message": "Invalid username or password."
            }

        return {
            "success": True,
            "message": "Login successful.",
            "user_id": user["user_id"],
            "username": user["username"],
            "role": user["role"]
        }

    finally:

        cursor.close()
        conn.close()


# ============================================================
# TERMINAL FUNCTIONS
# Keeps main.py working
# ============================================================

def register_employee():

    print("\n===== EMPLOYEE REGISTRATION =====")

    username = input(
        "Enter username: "
    )

    password = input(
        "Enter password: "
    )

    email = input(
        "Enter employee email: "
    )

    try:

        result = register_employee_account(
            username,
            password,
            email
        )

        print(
            "\n" + result["message"]
        )

        if result["success"]:

            print(
                "User ID:",
                result["user_id"]
            )

    except Exception as e:

        print(
            "Error:",
            e
        )


def login():

    print("\n===== LOGIN =====")

    username = input(
        "Enter username: "
    )

    password = input(
        "Enter password: "
    )

    try:

        result = authenticate_user(
            username,
            password
        )

        if result["success"]:

            print(
                "\nLogin successful."
            )

            return (
                result["user_id"],
                result["role"]
            )

        print(
            "\n" + result["message"]
        )

        return None

    except Exception as e:

        print(
            "Error:",
            e
        )

        return None