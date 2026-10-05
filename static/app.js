const app = document.getElementById("app");


// =========================
// SESSION HELPERS
// =========================

function getToken() {
    return sessionStorage.getItem("token");
}

function getUserId() {
    return sessionStorage.getItem("user_id");
}

function getRole() {
    return sessionStorage.getItem("role");
}

function clearSession() {
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("user_id");
    sessionStorage.removeItem("role");
}


// =========================
// API HELPER
// =========================

async function apiRequest(url, options = {}) {

    const token = getToken();

    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
        ...options,
        headers
    });

    let data;

    try {
        data = await response.json();
    } catch {
        data = {};
    }

    if (response.status === 401) {
        clearSession();
        showLogin();
        return null;
    }

    if (!response.ok) {
        throw new Error(data.message || "Something went wrong");
    }

    return data;
}


// =========================
// HTML SAFETY
// =========================

function escapeHtml(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// =========================
// LOGIN PAGE
// =========================

function showLogin() {

    app.innerHTML = `
        <div class="login-container">

            <div class="logo">
                <h1>Employee Management System</h1>
                <p>Login to continue</p>
            </div>

            <form id="loginForm">

                <div class="form-group">
                    <label>Username</label>
                    <input
                        type="text"
                        id="username"
                        placeholder="Enter username"
                        required
                    >
                </div>

                <div class="form-group">
                    <label>Password</label>
                    <input
                        type="password"
                        id="password"
                        placeholder="Enter password"
                        required
                    >
                </div>

                <button type="submit" class="login-btn">
                    Login
                </button>

            </form>

            <p id="message"></p>

            <div class="register-link">
                <button onclick="showRegister()">
                    Create Employee Account
                </button>
            </div>

        </div>
    `;

    document
        .getElementById("loginForm")
        .addEventListener("submit", handleLogin);
}


// =========================
// LOGIN
// =========================

async function handleLogin(event) {

    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    const message = document.getElementById("message");

    try {

        const data = await apiRequest("/api/login", {
            method: "POST",
            body: JSON.stringify({
                username,
                password
            })
        });

        if (!data) return;

        sessionStorage.setItem("token", data.token);
        sessionStorage.setItem("user_id", data.user_id);
        sessionStorage.setItem("role", data.role);

        showDashboard(data.role);

    } catch (error) {

        message.textContent = error.message;
        message.className = "error-message";
    }
}


// =========================
// REGISTRATION PAGE
// =========================

function showRegister() {

    app.innerHTML = `
        <div class="login-container">

            <div class="logo">
                <h1>Create Employee Account</h1>
                <p>Register using your employee email</p>
            </div>

            <form id="registerForm">

                <div class="form-group">
                    <label>Employee Email</label>
                    <input
                        type="email"
                        id="registerEmail"
                        placeholder="Enter employee email"
                        required
                    >
                </div>

                <div class="form-group">
                    <label>Username</label>
                    <input
                        type="text"
                        id="registerUsername"
                        placeholder="Choose username"
                        required
                    >
                </div>

                <div class="form-group">
                    <label>Password</label>
                    <input
                        type="password"
                        id="registerPassword"
                        placeholder="Choose password"
                        required
                    >
                </div>

                <button type="submit" class="login-btn">
                    Register
                </button>

            </form>

            <p id="message"></p>

            <div class="register-link">
                <button onclick="showLogin()">
                    Back to Login
                </button>
            </div>

        </div>
    `;

    document
        .getElementById("registerForm")
        .addEventListener("submit", handleRegister);
}


// =========================
// REGISTER
// =========================

async function handleRegister(event) {

    event.preventDefault();

    const email = document.getElementById("registerEmail").value.trim();
    const username = document.getElementById("registerUsername").value.trim();
    const password = document.getElementById("registerPassword").value;

    const message = document.getElementById("message");

    try {

        const data = await apiRequest("/api/register", {
            method: "POST",
            body: JSON.stringify({
                email,
                username,
                password
            })
        });

        if (!data) return;

        message.textContent = data.message;
        message.className = "success-message";

        setTimeout(showLogin, 1200);

    } catch (error) {

        message.textContent = error.message;
        message.className = "error-message";
    }
}


// =========================
// DASHBOARD
// =========================

function showDashboard(role) {

    if (role === "admin") {
        showAdminDashboard();
    } else {
        showEmployeeDashboard();
    }
}


// =========================
// ADMIN DASHBOARD
// =========================

function showAdminDashboard() {

    app.innerHTML = `
        <div class="dashboard-container">

            <div class="page-header">
                <div>
                    <h1>Admin Dashboard</h1>
                    <p>Employee Management System</p>
                </div>
            </div>

            <div class="dashboard-menu">

                <button onclick="showEmployees()">
                    👥 Employees
                </button>

                <button onclick="showDepartments()">
                    🏢 Departments
                </button>

                <button onclick="showAttendance()">
                    📅 Attendance
                </button>

                <button onclick="showLeaves()">
                    📝 Leave Management
                </button>

                <button class="logout-btn" onclick="logout()">
                    Logout
                </button>

            </div>

        </div>
    `;
}


// =========================
// EMPLOYEE DASHBOARD
// =========================

function showEmployeeDashboard() {

    app.innerHTML = `
        <div class="dashboard-container">

            <div class="page-header">
                <div>
                    <h1>Employee Dashboard</h1>
                    <p>Employee Management System</p>
                </div>
            </div>

            <div class="dashboard-menu">

                <button onclick="showMyProfile()">
                    👤 My Profile
                </button>

                <button onclick="showMyAttendance()">
                    📅 My Attendance
                </button>

                <button onclick="showMyLeave()">
                    📝 My Leave
                </button>

                <button onclick="showApplyLeave()">
                    ➕ Apply Leave
                </button>

                <button class="logout-btn" onclick="logout()">
                    Logout
                </button>

            </div>

        </div>
    `;
}


// =========================
// EMPLOYEES
// =========================

async function showEmployees() {

    try {

        const data = await apiRequest("/api/employees");

        if (!data) return;

        let rows = "";

        data.employees.forEach(employee => {

            rows += `
                <tr>

                    <td>${escapeHtml(employee.employee_id)}</td>

                    <td>
                        ${escapeHtml(employee.first_name)}
                        ${escapeHtml(employee.last_name)}
                    </td>

                    <td>${escapeHtml(employee.email)}</td>

                    <td>${escapeHtml(employee.phone)}</td>

                    <td>${escapeHtml(employee.job_title)}</td>

                    <td>${escapeHtml(employee.salary)}</td>

                    <td>${escapeHtml(employee.department_name || "Not Assigned")}</td>

                    <td>${escapeHtml(employee.status)}</td>

                    <td>
                        <button
                            class="small-btn"
                            onclick="showUpdateEmployee(${employee.employee_id})">
                            Update
                        </button>

                        <button
                            class="small-btn delete-btn"
                            onclick="deleteEmployee(${employee.employee_id})">
                            Delete
                        </button>
                    </td>

                </tr>
            `;
        });

        app.innerHTML = `
            <div class="employees-page">

                <div class="page-header">

                    <div>
                        <h1>Employees</h1>
                        <p>Manage employee records</p>
                    </div>

                    <div>
                        <button
                            class="back-btn"
                            onclick="showAdminDashboard()">
                            Back
                        </button>

                        <button
                            class="primary-btn"
                            onclick="showAddEmployee()">
                            Add Employee
                        </button>
                    </div>

                </div>

                <div class="search-box">

                    <input
                        type="text"
                        id="employeeSearch"
                        placeholder="Search by name or email">

                    <button onclick="searchEmployees()">
                        Search
                    </button>

                    <button onclick="showEmployees()">
                        Reset
                    </button>

                </div>

                <div class="table-container">

                    <table>

                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Phone</th>
                                <th>Job Title</th>
                                <th>Salary</th>
                                <th>Department</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>

                        <tbody>
                            ${rows}
                        </tbody>

                    </table>

                </div>

            </div>
        `;

    } catch (error) {

        alert(error.message);
    }
}


// =========================
// SEARCH EMPLOYEES
// =========================

async function searchEmployees() {

    const search = document
        .getElementById("employeeSearch")
        .value
        .trim()
        .toLowerCase();

    if (!search) {
        showEmployees();
        return;
    }

    try {

        const data = await apiRequest("/api/employees");

        if (!data) return;

        const filtered = data.employees.filter(employee => {

            const name =
                `${employee.first_name} ${employee.last_name}`
                .toLowerCase();

            const email =
                (employee.email || "").toLowerCase();

            return name.includes(search) || email.includes(search);
        });

        let rows = "";

        filtered.forEach(employee => {

            rows += `
                <tr>

                    <td>${escapeHtml(employee.employee_id)}</td>

                    <td>
                        ${escapeHtml(employee.first_name)}
                        ${escapeHtml(employee.last_name)}
                    </td>

                    <td>${escapeHtml(employee.email)}</td>

                    <td>${escapeHtml(employee.phone)}</td>

                    <td>${escapeHtml(employee.job_title)}</td>

                    <td>${escapeHtml(employee.salary)}</td>

                    <td>${escapeHtml(employee.department_name || "Not Assigned")}</td>

                    <td>${escapeHtml(employee.status)}</td>

                    <td>
                        <button
                            class="small-btn"
                            onclick="showUpdateEmployee(${employee.employee_id})">
                            Update
                        </button>

                        <button
                            class="small-btn delete-btn"
                            onclick="deleteEmployee(${employee.employee_id})">
                            Delete
                        </button>
                    </td>

                </tr>
            `;
        });

        const tbody = document.querySelector("tbody");

        if (tbody) {
            tbody.innerHTML = rows;
        }

    } catch (error) {

        alert(error.message);
    }
}


// =========================
// ADD EMPLOYEE
// =========================

async function showAddEmployee() {

    const departmentData =
        await apiRequest("/api/departments");

    if (!departmentData) return;

    const departments = departmentData.departments || [];

    let departmentOptions = `
        <option value="">Select Department</option>
    `;

    departments.forEach(department => {

        departmentOptions += `
            <option value="${department.department_id}">
                ${escapeHtml(department.department_name)}
            </option>
        `;
    });

    app.innerHTML = `
        <div class="form-page">

            <div class="page-header">

                <div>
                    <h1>Add Employee</h1>
                    <p>Create a new employee record</p>
                </div>

                <button
                    class="back-btn"
                    onclick="showEmployees()">
                    Back
                </button>

            </div>

            <form id="employeeForm">

                <div class="form-grid">

                    <div class="form-group">
                        <label>First Name</label>
                        <input id="firstName" required>
                    </div>

                    <div class="form-group">
                        <label>Last Name</label>
                        <input id="lastName" required>
                    </div>

                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" id="email" required>
                    </div>

                    <div class="form-group">
                        <label>Phone</label>
                        <input id="phone">
                    </div>

                    <div class="form-group">
                        <label>Job Title</label>
                        <input id="jobTitle">
                    </div>

                    <div class="form-group">
                        <label>Salary</label>
                        <input type="number" id="salary" step="0.01">
                    </div>

                    <div class="form-group">
                        <label>Hire Date</label>
                        <input type="date" id="hireDate">
                    </div>

                    <div class="form-group">
                        <label>Department</label>
                        <select id="departmentId">
                            ${departmentOptions}
                        </select>
                    </div>

                </div>

                <button type="submit" class="primary-btn">
                    Add Employee
                </button>

            </form>

            <p id="formMessage"></p>

        </div>
    `;

    document
        .getElementById("employeeForm")
        .addEventListener("submit", createEmployee);
}


// =========================
// CREATE EMPLOYEE
// =========================

async function createEmployee(event) {

    event.preventDefault();

    const employee = {

        first_name:
            document.getElementById("firstName").value.trim(),

        last_name:
            document.getElementById("lastName").value.trim(),

        email:
            document.getElementById("email").value.trim(),

        phone:
            document.getElementById("phone").value.trim(),

        job_title:
            document.getElementById("jobTitle").value.trim(),

        salary:
            document.getElementById("salary").value || null,

        hire_date:
            document.getElementById("hireDate").value || null,

        department_id:
            document.getElementById("departmentId").value || null
    };

    try {

        const data = await apiRequest("/api/employees", {
            method: "POST",
            body: JSON.stringify(employee)
        });

        if (!data) return;

        alert(data.message);

        showEmployees();

    } catch (error) {

        document.getElementById("formMessage").textContent =
            error.message;

        document.getElementById("formMessage").className =
            "error-message";
    }
}


// =========================
// UPDATE EMPLOYEE
// =========================

async function showUpdateEmployee(employeeId) {

    try {

        const data = await apiRequest("/api/employees");

        if (!data) return;

        const employee = data.employees.find(
            item => item.employee_id === employeeId
        );

        if (!employee) {
            alert("Employee not found");
            return;
        }

        app.innerHTML = `
            <div class="form-page">

                <div class="page-header">

                    <div>
                        <h1>Update Employee</h1>
                        <p>Employee ID: ${employeeId}</p>
                    </div>

                    <button
                        class="back-btn"
                        onclick="showEmployees()">
                        Back
                    </button>

                </div>

                <form id="updateEmployeeForm">

                    <div class="form-grid">

                        <div class="form-group">
                            <label>Salary</label>
                            <input
                                type="number"
                                id="updateSalary"
                                step="0.01"
                                value="${escapeHtml(employee.salary || "")}">
                        </div>

                        <div class="form-group">

                            <label>Status</label>

                            <select id="updateStatus">

                                <option value="Active"
                                    ${employee.status === "Active" ? "selected" : ""}>
                                    Active
                                </option>

                                <option value="Inactive"
                                    ${employee.status === "Inactive" ? "selected" : ""}>
                                    Inactive
                                </option>

                            </select>

                        </div>

                    </div>

                    <button
                        type="submit"
                        class="primary-btn">
                        Update Employee
                    </button>

                </form>

                <p id="formMessage"></p>

            </div>
        `;

        document
            .getElementById("updateEmployeeForm")
            .addEventListener(
                "submit",
                event => updateEmployee(event, employeeId)
            );

    } catch (error) {

        alert(error.message);
    }
}


async function updateEmployee(event, employeeId) {

    event.preventDefault();

    const salary =
        document.getElementById("updateSalary").value;

    const status =
        document.getElementById("updateStatus").value;

    try {

        const data = await apiRequest(
            "/api/employees/update",
            {
                method: "POST",
                body: JSON.stringify({
                    employee_id: employeeId,
                    salary: salary || null,
                    status
                })
            }
        );

        if (!data) return;

        alert(data.message);

        showEmployees();

    } catch (error) {

        document.getElementById("formMessage").textContent =
            error.message;

        document.getElementById("formMessage").className =
            "error-message";
    }
}


// =========================
// DELETE EMPLOYEE
// =========================

async function deleteEmployee(employeeId) {

    const confirmed =
        confirm(
            `Are you sure you want to delete employee ${employeeId}?`
        );

    if (!confirmed) return;

    try {

        const data = await apiRequest(
            "/api/employees/delete",
            {
                method: "POST",
                body: JSON.stringify({
                    employee_id: employeeId
                })
            }
        );

        if (!data) return;

        alert(data.message);

        showEmployees();

    } catch (error) {

        alert(error.message);
    }
}


// =========================
// DEPARTMENTS
// =========================

async function showDepartments() {

    try {

        const data =
            await apiRequest("/api/departments");

        if (!data) return;

        let rows = "";

        data.departments.forEach(department => {

            rows += `
                <tr>

                    <td>
                        ${escapeHtml(department.department_id)}
                    </td>

                    <td>
                        ${escapeHtml(department.department_name)}
                    </td>

                    <td>
                        ${escapeHtml(department.location)}
                    </td>

                </tr>
            `;
        });

        app.innerHTML = `
            <div class="employees-page">

                <div class="page-header">

                    <div>
                        <h1>Departments</h1>
                        <p>Manage company departments</p>
                    </div>

                    <div>

                        <button
                            class="back-btn"
                            onclick="showAdminDashboard()">
                            Back
                        </button>

                        <button
                            class="primary-btn"
                            onclick="showAddDepartment()">
                            Add Department
                        </button>

                    </div>

                </div>

                <div class="table-container">

                    <table>

                        <thead>

                            <tr>
                                <th>ID</th>
                                <th>Department</th>
                                <th>Location</th>
                            </tr>

                        </thead>

                        <tbody>
                            ${rows}
                        </tbody>

                    </table>

                </div>

            </div>
        `;

    } catch (error) {

        alert(error.message);
    }
}


// =========================
// ADD DEPARTMENT
// =========================

function showAddDepartment() {

    app.innerHTML = `
        <div class="form-page">

            <div class="page-header">

                <div>
                    <h1>Add Department</h1>
                    <p>Create a new department</p>
                </div>

                <button
                    class="back-btn"
                    onclick="showDepartments()">
                    Back
                </button>

            </div>

            <form id="departmentForm">

                <div class="form-grid">

                    <div class="form-group">

                        <label>Department Name</label>

                        <input
                            id="departmentName"
                            required>

                    </div>

                    <div class="form-group">

                        <label>Location</label>

                        <input
                            id="departmentLocation">

                    </div>

                </div>

                <button
                    type="submit"
                    class="primary-btn">
                    Add Department
                </button>

            </form>

            <p id="formMessage"></p>

        </div>
    `;

    document
        .getElementById("departmentForm")
        .addEventListener(
            "submit",
            createDepartment
        );
}


async function createDepartment(event) {

    event.preventDefault();

    const departmentName =
        document.getElementById("departmentName")
            .value.trim();

    const location =
        document.getElementById("departmentLocation")
            .value.trim();

    try {

        const data = await apiRequest(
            "/api/departments",
            {
                method: "POST",
                body: JSON.stringify({
                    department_name: departmentName,
                    location
                })
            }
        );

        if (!data) return;

        alert(data.message);

        showDepartments();

    } catch (error) {

        document.getElementById("formMessage").textContent =
            error.message;

        document.getElementById("formMessage").className =
            "error-message";
    }
}


// =========================
// ATTENDANCE
// =========================

async function showAttendance() {

    try {

        const data =
            await apiRequest("/api/attendance");

        if (!data) return;

        let rows = "";

        data.attendance.forEach(record => {

            rows += `
                <tr>

                    <td>${escapeHtml(record.attendance_id)}</td>

                    <td>${escapeHtml(record.employee_id)}</td>

                    <td>${escapeHtml(record.first_name || "")}
                        ${escapeHtml(record.last_name || "")}
                    </td>

                    <td>${escapeHtml(record.attendance_date)}</td>

                    <td>${escapeHtml(record.status)}</td>

                </tr>
            `;
        });

        app.innerHTML = `
            <div class="employees-page">

                <div class="page-header">

                    <div>
                        <h1>Attendance</h1>
                        <p>View employee attendance</p>
                    </div>

                    <div>

                        <button
                            class="back-btn"
                            onclick="showAdminDashboard()">
                            Back
                        </button>

                        <button
                            class="primary-btn"
                            onclick="showMarkAttendance()">
                            Mark Attendance
                        </button>

                    </div>

                </div>

                <div class="table-container">

                    <table>

                        <thead>

                            <tr>
                                <th>ID</th>
                                <th>Employee ID</th>
                                <th>Employee</th>
                                <th>Date</th>
                                <th>Status</th>
                            </tr>

                        </thead>

                        <tbody>
                            ${rows}
                        </tbody>

                    </table>

                </div>

            </div>
        `;

    } catch (error) {

        alert(error.message);
    }
}


// =========================
// MARK ATTENDANCE
// =========================

function showMarkAttendance() {

    app.innerHTML = `
        <div class="form-page">

            <div class="page-header">

                <div>
                    <h1>Mark Attendance</h1>
                    <p>Record employee attendance</p>
                </div>

                <button
                    class="back-btn"
                    onclick="showAttendance()">
                    Back
                </button>

            </div>

            <form id="attendanceForm">

                <div class="form-grid">

                    <div class="form-group">

                        <label>Employee ID</label>

                        <input
                            type="number"
                            id="attendanceEmployeeId"
                            required>

                    </div>

                    <div class="form-group">

                        <label>Date</label>

                        <input
                            type="date"
                            id="attendanceDate"
                            required>

                    </div>

                    <div class="form-group">

                        <label>Status</label>

                        <select id="attendanceStatus">

                            <option value="Present">
                                Present
                            </option>

                            <option value="Absent">
                                Absent
                            </option>

                            <option value="Late">
                                Late
                            </option>

                        </select>

                    </div>

                </div>

                <button
                    type="submit"
                    class="primary-btn">
                    Mark Attendance
                </button>

            </form>

            <p id="formMessage"></p>

        </div>
    `;

    document
        .getElementById("attendanceForm")
        .addEventListener(
            "submit",
            createAttendance
        );
}


async function createAttendance(event) {

    event.preventDefault();

    const employeeId =
        document.getElementById("attendanceEmployeeId")
            .value;

    const attendanceDate =
        document.getElementById("attendanceDate")
            .value;

    const status =
        document.getElementById("attendanceStatus")
            .value;

    try {

        const data = await apiRequest(
            "/api/attendance",
            {
                method: "POST",
                body: JSON.stringify({
                    employee_id: employeeId,
                    attendance_date: attendanceDate,
                    status
                })
            }
        );

        if (!data) return;

        alert(data.message);

        showAttendance();

    } catch (error) {

        document.getElementById("formMessage").textContent =
            error.message;

        document.getElementById("formMessage").className =
            "error-message";
    }
}


// =========================
// LEAVES - ADMIN
// =========================

async function showLeaves() {

    try {

        const data =
            await apiRequest("/api/leaves");

        if (!data) return;

        let rows = "";

        data.leaves.forEach(leave => {

            rows += `
                <tr>

                    <td>${escapeHtml(leave.leave_id)}</td>

                    <td>${escapeHtml(leave.employee_id)}</td>

                    <td>${escapeHtml(leave.first_name || "")}
                        ${escapeHtml(leave.last_name || "")}
                    </td>

                    <td>${escapeHtml(leave.leave_type)}</td>

                    <td>${escapeHtml(leave.start_date)}</td>

                    <td>${escapeHtml(leave.end_date)}</td>

                    <td>${escapeHtml(leave.reason)}</td>

                    <td>${escapeHtml(leave.status)}</td>

                    <td>

                        <button
                            class="small-btn"
                            onclick="updateLeaveStatus(${leave.leave_id}, 'Approved')">
                            Approve
                        </button>

                        <button
                            class="small-btn delete-btn"
                            onclick="updateLeaveStatus(${leave.leave_id}, 'Rejected')">
                            Reject
                        </button>

                    </td>

                </tr>
            `;
        });

        app.innerHTML = `
            <div class="employees-page">

                <div class="page-header">

                    <div>
                        <h1>Leave Management</h1>
                        <p>View and manage employee leaves</p>
                    </div>

                    <button
                        class="back-btn"
                        onclick="showAdminDashboard()">
                        Back
                    </button>

                </div>

                <div class="table-container">

                    <table>

                        <thead>

                            <tr>
                                <th>ID</th>
                                <th>Employee ID</th>
                                <th>Employee</th>
                                <th>Type</th>
                                <th>Start</th>
                                <th>End</th>
                                <th>Reason</th>
                                <th>Status</th>
                                <th>Action</th>
                            </tr>

                        </thead>

                        <tbody>
                            ${rows}
                        </tbody>

                    </table>

                </div>

            </div>
        `;

    } catch (error) {

        alert(error.message);
    }
}


// =========================
// UPDATE LEAVE STATUS
// =========================

async function updateLeaveStatus(leaveId, status) {

    try {

        const data = await apiRequest(
            "/api/leaves/status",
            {
                method: "POST",
                body: JSON.stringify({
                    leave_id: leaveId,
                    status
                })
            }
        );

        if (!data) return;

        alert(data.message);

        showLeaves();

    } catch (error) {

        alert(error.message);
    }
}


// =========================
// MY PROFILE
// =========================

async function showMyProfile() {

    try {

        const data =
            await apiRequest("/api/my-profile");

        if (!data) return;

        // The server returns the employee object directly
        const employee = data.employee || data;

        if (!employee || !employee.employee_id) {
            alert("Employee profile not found.");
            return;
        }

        app.innerHTML = `
            <div class="form-page">

                <div class="page-header">

                    <div>
                        <h1>My Profile</h1>
                        <p>Employee information</p>
                    </div>

                    <button
                        class="back-btn"
                        onclick="showEmployeeDashboard()">
                        Back
                    </button>

                </div>

                <div class="profile-card">

                    <p>
                        <strong>Employee ID:</strong>
                        ${escapeHtml(employee.employee_id)}
                    </p>

                    <p>
                        <strong>Name:</strong>
                        ${escapeHtml(employee.first_name)}
                        ${escapeHtml(employee.last_name)}
                    </p>

                    <p>
                        <strong>Email:</strong>
                        ${escapeHtml(employee.email)}
                    </p>

                    <p>
                        <strong>Phone:</strong>
                        ${escapeHtml(employee.phone)}
                    </p>

                    <p>
                        <strong>Job Title:</strong>
                        ${escapeHtml(employee.job_title)}
                    </p>

                    <p>
                        <strong>Salary:</strong>
                        ${escapeHtml(employee.salary)}
                    </p>

                    <p>
                        <strong>Hire Date:</strong>
                        ${escapeHtml(employee.hire_date)}
                    </p>

                    <p>
                        <strong>Department:</strong>
                        ${escapeHtml(
                            employee.department_name || "Not Assigned"
                        )}
                    </p>

                    <p>
                        <strong>Status:</strong>
                        ${escapeHtml(employee.status)}
                    </p>

                </div>

            </div>
        `;

    } catch (error) {

        alert(error.message);
    }
}


// =========================
// MY ATTENDANCE
// =========================

async function showMyAttendance() {

    try {

        const data =
            await apiRequest("/api/my-attendance");

        if (!data) return;

        let rows = "";

        data.attendance.forEach(record => {

            rows += `
                <tr>

                    <td>${escapeHtml(record.attendance_date)}</td>

                    <td>${escapeHtml(record.status)}</td>

                </tr>
            `;
        });

        app.innerHTML = `
            <div class="employees-page">

                <div class="page-header">

                    <div>
                        <h1>My Attendance</h1>
                        <p>Your attendance records</p>
                    </div>

                    <button
                        class="back-btn"
                        onclick="showEmployeeDashboard()">
                        Back
                    </button>

                </div>

                <div class="table-container">

                    <table>

                        <thead>

                            <tr>
                                <th>Date</th>
                                <th>Status</th>
                            </tr>

                        </thead>

                        <tbody>
                            ${rows}
                        </tbody>

                    </table>

                </div>

            </div>
        `;

    } catch (error) {

        alert(error.message);
    }
}


// =========================
// MY LEAVE
// =========================

async function showMyLeave() {

    try {

        const data =
            await apiRequest("/api/my-leave");

        if (!data) return;

        let rows = "";

        data.leaves.forEach(leave => {

            rows += `
                <tr>

                    <td>${escapeHtml(leave.leave_id)}</td>

                    <td>${escapeHtml(leave.leave_type)}</td>

                    <td>${escapeHtml(leave.start_date)}</td>

                    <td>${escapeHtml(leave.end_date)}</td>

                    <td>${escapeHtml(leave.reason)}</td>

                    <td>${escapeHtml(leave.status)}</td>

                </tr>
            `;
        });

        app.innerHTML = `
            <div class="employees-page">

                <div class="page-header">

                    <div>
                        <h1>My Leave</h1>
                        <p>Your leave applications</p>
                    </div>

                    <button
                        class="back-btn"
                        onclick="showEmployeeDashboard()">
                        Back
                    </button>

                </div>

                <div class="table-container">

                    <table>

                        <thead>

                            <tr>
                                <th>ID</th>
                                <th>Type</th>
                                <th>Start</th>
                                <th>End</th>
                                <th>Reason</th>
                                <th>Status</th>
                            </tr>

                        </thead>

                        <tbody>
                            ${rows}
                        </tbody>

                    </table>

                </div>

            </div>
        `;

    } catch (error) {

        alert(error.message);
    }
}


// =========================
// APPLY LEAVE
// =========================

function showApplyLeave() {

    app.innerHTML = `
        <div class="form-page">

            <div class="page-header">

                <div>
                    <h1>Apply Leave</h1>
                    <p>Submit a new leave application</p>
                </div>

                <button
                    class="back-btn"
                    onclick="showEmployeeDashboard()">
                    Back
                </button>

            </div>

            <form id="leaveForm">

                <div class="form-grid">

                    <div class="form-group">

                        <label>Leave Type</label>

                        <select id="leaveType">

                            <option value="Casual">
                                Casual
                            </option>

                            <option value="Sick">
                                Sick
                            </option>

                            <option value="Annual">
                                Annual
                            </option>

                            <option value="Emergency">
                                Emergency
                            </option>

                        </select>

                    </div>

                    <div class="form-group">

                        <label>Start Date</label>

                        <input
                            type="date"
                            id="leaveStart"
                            required>

                    </div>

                    <div class="form-group">

                        <label>End Date</label>

                        <input
                            type="date"
                            id="leaveEnd"
                            required>

                    </div>

                    <div class="form-group">

                        <label>Reason</label>

                        <textarea
                            id="leaveReason"
                            rows="4"
                            placeholder="Enter reason">
                        </textarea>

                    </div>

                </div>

                <button
                    type="submit"
                    class="primary-btn">
                    Apply Leave
                </button>

            </form>

            <p id="formMessage"></p>

        </div>
    `;

    document
        .getElementById("leaveForm")
        .addEventListener(
            "submit",
            createLeave
        );
}


async function createLeave(event) {

    event.preventDefault();

    const leaveType =
        document.getElementById("leaveType").value;

    const startDate =
        document.getElementById("leaveStart").value;

    const endDate =
        document.getElementById("leaveEnd").value;

    const reason =
        document.getElementById("leaveReason").value.trim();

    try {

        const data = await apiRequest(
            "/api/my-leave",
            {
                method: "POST",
                body: JSON.stringify({
                    leave_type: leaveType,
                    start_date: startDate,
                    end_date: endDate,
                    reason
                })
            }
        );

        if (!data) return;

        alert(data.message);

        showMyLeave();

    } catch (error) {

        document.getElementById("formMessage").textContent =
            error.message;

        document.getElementById("formMessage").className =
            "error-message";
    }
}


// =========================
// LOGOUT
// =========================

async function logout() {

    try {

        await apiRequest(
            "/api/logout",
            {
                method: "POST"
            }
        );

    } catch (error) {

        console.log(error.message);

    } finally {

        clearSession();
        showLogin();
    }
}


// =========================
// INITIAL PAGE
// =========================

function initializeApp() {

    const token = getToken();
    const role = getRole();

    if (token && role) {
        showDashboard(role);
    } else {
        showLogin();
    }
}


initializeApp();