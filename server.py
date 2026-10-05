from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os
import secrets

from auth import (
    authenticate_user,
    register_employee_account
)

from employee import (
    create_employee,
    get_employees,
    update_employee_data,
    delete_employee_data,
    get_my_profile,
    get_my_attendance
)

from department import (
    create_department,
    get_departments
)

from attendance import (
    create_attendance,
    get_attendance
)

from leave import (
    create_leave,
    get_leaves,
    get_my_leave,
    change_leave_status
)


# ============================================================
# SERVER SETTINGS
# ============================================================

HOST = "localhost"
PORT = 8000

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

STATIC_DIR = os.path.join(
    BASE_DIR,
    "static"
)


# ============================================================
# SESSION STORAGE
# ============================================================

sessions = {}


# ============================================================
# RESPONSE HELPERS
# ============================================================

def send_json(handler, data, status=200):

    response = json.dumps(
        data,
        default=str
    ).encode("utf-8")

    handler.send_response(status)

    handler.send_header(
        "Content-Type",
        "application/json"
    )

    handler.send_header(
        "Content-Length",
        str(len(response))
    )

    handler.end_headers()

    handler.wfile.write(response)


def send_file(handler, filename, content_type):

    file_path = os.path.join(
        STATIC_DIR,
        filename
    )

    if not os.path.exists(file_path):

        send_json(
            handler,
            {
                "success": False,
                "message": "File not found."
            },
            404
        )

        return

    with open(
        file_path,
        "rb"
    ) as file:

        content = file.read()

    handler.send_response(200)

    handler.send_header(
        "Content-Type",
        content_type
    )

    handler.send_header(
        "Content-Length",
        str(len(content))
    )

    handler.end_headers()

    handler.wfile.write(content)


def get_request_body(handler):

    content_length = int(
        handler.headers.get(
            "Content-Length",
            0
        )
    )

    body = handler.rfile.read(
        content_length
    )

    if not body:

        return {}

    return json.loads(
        body.decode("utf-8")
    )


# ============================================================
# SESSION HELPERS
# ============================================================

def get_token(handler):

    # First check Authorization header

    authorization = handler.headers.get(
        "Authorization",
        ""
    )

    if authorization.startswith("Bearer "):

        return authorization.split(
            " ",
            1
        )[1]

    # Also support session cookie

    cookie = handler.headers.get(
        "Cookie",
        ""
    )

    for item in cookie.split(";"):

        item = item.strip()

        if item.startswith(
            "session_token="
        ):

            return item.split(
                "=",
                1
            )[1]

    return None


def get_session(handler):

    token = get_token(handler)

    if not token:

        return None

    return sessions.get(token)


def require_login(handler):

    session = get_session(handler)

    if not session:

        send_json(
            handler,
            {
                "success": False,
                "message": "Please login first."
            },
            401
        )

        return None

    return session


def require_admin(handler):

    session = require_login(handler)

    if not session:

        return None

    if session["role"] != "admin":

        send_json(
            handler,
            {
                "success": False,
                "message": "Admin access required."
            },
            403
        )

        return None

    return session


# ============================================================
# HTTP HANDLER
# ============================================================

class EmployeeManagementHandler(
    BaseHTTPRequestHandler
):

    def log_message(self, format, *args):

        return

    # ========================================================
    # GET
    # ========================================================

    def do_GET(self):

        parsed = urlparse(
            self.path
        )

        path = parsed.path

        query = parse_qs(
            parsed.query
        )

        # ----------------------------------------------------
        # STATIC FILES
        # ----------------------------------------------------

        if path == "/":

            send_file(
                self,
                "index.html",
                "text/html"
            )

            return

        if path == "/static/index.html":

            send_file(
                self,
                "index.html",
                "text/html"
            )

            return

        if path == "/static/style.css":

            send_file(
                self,
                "style.css",
                "text/css"
            )

            return

        if path == "/static/app.js":

            send_file(
                self,
                "app.js",
                "application/javascript"
            )

            return

        # ----------------------------------------------------
        # EMPLOYEES
        # ----------------------------------------------------

        if path == "/api/employees":

            session = require_admin(self)

            if not session:

                return

            search = query.get(
                "search",
                [""]
            )[0]

            try:

                employees = get_employees(
                    search
                )

                send_json(
                    self,
                    {
                        "success": True,
                        "employees": employees
                    }
                )

            except Exception as e:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": str(e)
                    },
                    500
                )

            return

        # ----------------------------------------------------
        # DEPARTMENTS
        # ----------------------------------------------------

        if path == "/api/departments":

            session = require_admin(self)

            if not session:

                return

            try:

                departments = get_departments()

                send_json(
                    self,
                    {
                        "success": True,
                        "departments": departments
                    }
                )

            except Exception as e:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": str(e)
                    },
                    500
                )

            return

        # ----------------------------------------------------
        # ATTENDANCE
        # ----------------------------------------------------

        if path == "/api/attendance":

            session = require_admin(self)

            if not session:

                return

            try:

                attendance = get_attendance()

                send_json(
                    self,
                    {
                        "success": True,
                        "attendance": attendance
                    }
                )

            except Exception as e:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": str(e)
                    },
                    500
                )

            return

        # ----------------------------------------------------
        # ALL LEAVES
        # ----------------------------------------------------

        if path == "/api/leaves":

            session = require_admin(self)

            if not session:

                return

            try:

                leaves = get_leaves()

                send_json(
                    self,
                    {
                        "success": True,
                        "leaves": leaves
                    }
                )

            except Exception as e:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": str(e)
                    },
                    500
                )

            return

        # ----------------------------------------------------
        # MY PROFILE
        # ----------------------------------------------------

        if path == "/api/my-profile":

            session = require_login(self)

            if not session:

                return

            try:

                profile = get_my_profile(
                    session["user_id"]
                )

                send_json(
                    self,
                    {
                        "success": True,
                        "profile": profile,
                        "employee": profile
                    }
                )

            except Exception as e:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": str(e)
                    },
                    500
                )

            return

        # ----------------------------------------------------
        # MY ATTENDANCE
        # ----------------------------------------------------

        if path == "/api/my-attendance":

            session = require_login(self)

            if not session:

                return

            try:

                attendance = get_my_attendance(
                    session["user_id"]
                )

                send_json(
                    self,
                    {
                        "success": True,
                        "attendance": attendance
                    }
                )

            except Exception as e:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": str(e)
                    },
                    500
                )

            return

        # ----------------------------------------------------
        # MY LEAVE
        # ----------------------------------------------------

        if path == "/api/my-leave":

            session = require_login(self)

            if not session:

                return

            try:

                leaves = get_my_leave(
                    session["user_id"]
                )

                send_json(
                    self,
                    {
                        "success": True,
                        "leaves": leaves
                    }
                )

            except Exception as e:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": str(e)
                    },
                    500
                )

            return

        # ----------------------------------------------------
        # UNKNOWN GET
        # ----------------------------------------------------

        send_json(
            self,
            {
                "success": False,
                "message": "API endpoint not found."
            },
            404
        )

    # ========================================================
    # POST
    # ========================================================

    def do_POST(self):

        parsed = urlparse(
            self.path
        )

        path = parsed.path

        try:

            data = get_request_body(
                self
            )

        except Exception:

            send_json(
                self,
                {
                    "success": False,
                    "message": "Invalid JSON request."
                },
                400
            )

            return

        # ----------------------------------------------------
        # LOGIN
        # ----------------------------------------------------

        if path == "/api/login":

            username = data.get(
                "username",
                ""
            ).strip()

            password = data.get(
                "password",
                ""
            )

            if not username or not password:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": "Username and password are required."
                    },
                    400
                )

                return

            try:

                result = authenticate_user(username, password)

                if not result:
                    send_json(
                        self,
                        {
                            "success": False,
                            "message": "Invalid username or password."
                        },
                        401
                    )
                    return


                # Handle the authentication result
                if isinstance(result, dict):

                    if not result.get("success", True):
                        send_json(
                            self,
                            result,
                            401
                        )
                        return

                    user_id = result["user_id"]
                    username = result.get("username", username)
                    role = result["role"]

                else:

                    # Supports both:
                    # (user_id, role)
                    # (user_id, username, role)

                    user_id = result[0]

                    if len(result) == 2:
                        role = result[1]
                    else:
                        username = result[1]
                        role = result[2]


                token = secrets.token_urlsafe(32)

                sessions[token] = {
                    "user_id": user_id,
                    "username": username,
                    "role": role
                }

                send_json(
                    self,
                    {
                        "success": True,
                        "message": "Login successful.",
                        "token": token,
                        "user_id": user_id,
                        "username": username,
                        "role": role
                    }
                )

            except Exception as e:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": str(e)
                    },
                    500
                )

            return

        # ----------------------------------------------------
        # REGISTER
        # ----------------------------------------------------

        if path == "/api/register":

            username = data.get(
                "username",
                ""
            ).strip()

            password = data.get(
                "password",
                ""
            )

            email = data.get(
                "email",
                ""
            ).strip()

            if not username or not password or not email:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": "Username, password and email are required."
                    },
                    400
                )

                return

            try:

                result = register_employee_account(
                    username,
                    password,
                    email
                )

                send_json(
                    self,
                    result,
                    200 if result["success"] else 400
                )

            except Exception as e:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": str(e)
                    },
                    500
                )

            return

        # ----------------------------------------------------
        # LOGOUT
        # ----------------------------------------------------

        if path == "/api/logout":

            token = get_token(
                self
            )

            if token:

                sessions.pop(
                    token,
                    None
                )

            send_json(
                self,
                {
                    "success": True,
                    "message": "Logged out successfully."
                }
            )

            return

        # ----------------------------------------------------
        # ADD EMPLOYEE
        # ----------------------------------------------------

        if path == "/api/employees":

            session = require_admin(self)

            if not session:

                return

            try:

                employee_id = create_employee(
                    data["first_name"],
                    data["last_name"],
                    data["email"],
                    data.get("phone"),
                    data.get("job_title"),
                    data.get("salary"),
                    data.get("hire_date"),
                    data.get("department_id")
                )

                send_json(
                    self,
                    {
                        "success": True,
                        "message": "Employee added successfully.",
                        "employee_id": employee_id
                    }
                )

            except Exception as e:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": str(e)
                    },
                    400
                )

            return

        # ----------------------------------------------------
        # ADD DEPARTMENT
        # ----------------------------------------------------

        if path == "/api/departments":

            session = require_admin(self)

            if not session:

                return

            try:

                department_id = create_department(
                    data["department_name"],
                    data.get("location")
                )

                send_json(
                    self,
                    {
                        "success": True,
                        "message": "Department added successfully.",
                        "department_id": department_id
                    }
                )

            except Exception as e:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": str(e)
                    },
                    400
                )

            return

        # ----------------------------------------------------
        # MARK ATTENDANCE
        # ----------------------------------------------------

        if path == "/api/attendance":

            session = require_admin(self)

            if not session:

                return

            try:

                attendance_id = create_attendance(
                    data["employee_id"],
                    data["attendance_date"],
                    data["status"]
                )

                send_json(
                    self,
                    {
                        "success": True,
                        "message": "Attendance marked successfully.",
                        "attendance_id": attendance_id
                    }
                )

            except Exception as e:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": str(e)
                    },
                    400
                )

            return

        # ----------------------------------------------------
        # APPLY LEAVE
        # ----------------------------------------------------

        if path == "/api/my-leave":

            session = require_login(self)

            if not session:

                return

            try:

                leave_id = create_leave(
                    session["user_id"],
                    data["leave_type"],
                    data["start_date"],
                    data["end_date"],
                    data.get("reason")
                )

                if leave_id is None:

                    send_json(
                        self,
                        {
                            "success": False,
                            "message": "No employee is linked to this account."
                        },
                        400
                    )

                    return

                send_json(
                    self,
                    {
                        "success": True,
                        "message": "Leave application submitted successfully.",
                        "leave_id": leave_id
                    }
                )

            except Exception as e:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": str(e)
                    },
                    400
                )

            return

        # ----------------------------------------------------
        # UPDATE LEAVE STATUS
        # ----------------------------------------------------

        if path == "/api/leaves/status":

            session = require_admin(self)

            if not session:

                return

            try:

                affected_rows = change_leave_status(
                    data["leave_id"],
                    data["status"]
                )

                if affected_rows == 0:

                    send_json(
                        self,
                        {
                            "success": False,
                            "message": "Leave record not found."
                        },
                        404
                    )

                    return

                send_json(
                    self,
                    {
                        "success": True,
                        "message": "Leave status updated successfully."
                    }
                )

            except Exception as e:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": str(e)
                    },
                    400
                )

            return

        # ----------------------------------------------------
        # UPDATE EMPLOYEE
        # ----------------------------------------------------

        if path == "/api/employees/update":

            session = require_admin(self)

            if not session:

                return

            try:

                affected_rows = update_employee_data(
                    data["employee_id"],
                    data["salary"],
                    data["status"]
                )

                if affected_rows == 0:

                    send_json(
                        self,
                        {
                            "success": False,
                            "message": "Employee not found."
                        },
                        404
                    )

                    return

                send_json(
                    self,
                    {
                        "success": True,
                        "message": "Employee updated successfully."
                    }
                )

            except Exception as e:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": str(e)
                    },
                    400
                )

            return

        # ----------------------------------------------------
        # DELETE EMPLOYEE
        # ----------------------------------------------------

        if path == "/api/employees/delete":

            session = require_admin(self)

            if not session:

                return

            try:

                affected_rows = delete_employee_data(
                    data["employee_id"]
                )

                if affected_rows == 0:

                    send_json(
                        self,
                        {
                            "success": False,
                            "message": "Employee not found."
                        },
                        404
                    )

                    return

                send_json(
                    self,
                    {
                        "success": True,
                        "message": "Employee deleted successfully."
                    }
                )

            except Exception as e:

                send_json(
                    self,
                    {
                        "success": False,
                        "message": str(e)
                    },
                    400
                )

            return

        # ----------------------------------------------------
        # UNKNOWN POST
        # ----------------------------------------------------

        send_json(
            self,
            {
                "success": False,
                "message": "API endpoint not found."
            },
            404
        )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    server = HTTPServer(
        (HOST, PORT),
        EmployeeManagementHandler
    )

    print(
        f"Server running at http://{HOST}:{PORT}"
    )

    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print("\nServer stopped.")

    finally:

        server.server_close()