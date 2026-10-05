import bcrypt
from database import get_connection

def create_admin():
    username = input("Admin username: ").strip()
    password = input("Admin password: ").strip()

    if not username or not password:
        print("Username and password are required.")
        return

    hashed = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
            (username, hashed, "admin")
        )
        conn.commit()
        print("Admin account created.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_admin()
