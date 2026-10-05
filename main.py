from auth import login, register_employee
from employee import (
    add_employee, view_employees, search_employee,
    update_employee, delete_employee, my_profile, my_attendance
)
from department import add_department, view_departments
from attendance import mark_attendance, view_attendance
from leave import apply_leave, view_leaves, my_leave, update_leave_status


def admin_menu():
    while True:
        print("\n===== ADMIN DASHBOARD =====")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Add Department")
        print("7. View Departments")
        print("8. Mark Attendance")
        print("9. View Attendance")
        print("10. View Leaves")
        print("11. Update Leave Status")
        print("0. Logout")

        choice = input("Enter choice: ")

        try:
            if choice == "1": add_employee()
            elif choice == "2": view_employees()
            elif choice == "3": search_employee()
            elif choice == "4": update_employee()
            elif choice == "5": delete_employee()
            elif choice == "6": add_department()
            elif choice == "7": view_departments()
            elif choice == "8": mark_attendance()
            elif choice == "9": view_attendance()
            elif choice == "10": view_leaves()
            elif choice == "11": update_leave_status()
            elif choice == "0":
                print("Logged out.")
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print("Error:", e)


def employee_menu(user_id):
    while True:
        print("\n===== EMPLOYEE PORTAL =====")
        print("1. My Profile")
        print("2. My Attendance")
        print("3. Apply Leave")
        print("4. My Leave")
        print("0. Logout")

        choice = input("Enter choice: ")

        try:
            if choice == "1": my_profile(user_id)
            elif choice == "2": my_attendance(user_id)
            elif choice == "3": apply_leave(user_id)
            elif choice == "4": my_leave(user_id)
            elif choice == "0":
                print("Logged out.")
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print("Error:", e)


def main():
    while True:
        print("\n===== EMPLOYEE MANAGEMENT SYSTEM =====")
        print("1. Login")
        print("2. Employee Registration")
        print("0. Exit")

        choice = input("Enter choice: ")

        try:
            if choice == "1":
                user = login()
                if user:
                    user_id, role = user
                    if role == "admin":
                        admin_menu()
                    else:
                        employee_menu(user_id)

            elif choice == "2":
                register_employee()

            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print("Invalid choice.")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()