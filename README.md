# Employee & HR Management System

A full-stack academic **Employee & Human Resources Management System** built with **Python, Streamlit, Plotly, MySQL, and SQLite**.

The system provides an interactive dashboard for managing and analysing employee information, departments, projects, attendance, leave, payroll, performance, training, and recruitment. The database is designed using **EER modelling, functional dependencies, and normalization up to Third Normal Form (3NF)**.

---

## Overview

The Employee & HR Management System is designed to provide a centralized platform for HR-related operations and analytics.

The application combines:

- A normalized relational database
- MySQL database connectivity
- Portable SQLite database support
- Interactive Streamlit dashboard
- Plotly-based data visualization
- Employee search and filtering
- CRUD operations
- Payroll and attendance analytics
- Project and training management
- Recruitment analysis
- Interactive SQL execution
- Academic database documentation

The application supports both **MySQL** and a **portable SQLite fallback**, allowing the project to run even when a MySQL server is not available.

---

## Key Features

### Employee Management

- View employee records
- Search employees using multiple criteria
- Filter employees by department, job title, and salary
- Register new employees
- View employee-related information

### Department Management

- View department information
- Analyse department-wise employee distribution
- Compare department budgets with payroll expenditure
- Monitor budget utilization

### Project Management

- View active projects
- Track employee-project assignments
- View employee roles within projects
- Track hours contributed by employees
- Analyse project staffing

### Attendance Management

- View attendance records
- Analyse attendance status
- Monitor attendance compliance
- Analyse work patterns

### Leave Management

- View leave requests
- Analyse leave categories and statuses
- Approve or manage leave requests
- View leave-related statistics

### Payroll Management

- View payroll information
- Analyse salary distributions
- Compare salaries across departments
- Analyse allowances and deductions
- Perform net salary reconciliation

### Performance Management

- View employee performance reviews
- Analyse performance ratings
- Identify high-performing employees
- Visualize rating distributions

### Training Management

- View training programs
- Track employee participation
- Analyse assessment scores
- Analyse training performance and ROI

### Recruitment Management

- Track candidates through recruitment stages
- Analyse recruitment conversion
- Visualize the recruitment funnel
- Analyse candidate progression

### Interactive SQL Studio

The dashboard includes an SQL interface that allows users to:

- Execute SQL queries
- View query results interactively
- Run predefined academic queries
- Analyse data directly from the database

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Interactive web dashboard |
| Plotly | Data visualization |
| MySQL | Primary relational database |
| SQLite | Portable database fallback |
| Pandas | Data processing |
| SQL | Database design and queries |
| Git & GitHub | Version control |

---

## System Architecture

```text
                         ┌──────────────────────┐
                         │      User / HR       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Streamlit Dashboard │
                         │       app.py         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Database Connection  │
                         │   connection.py      │
                         └──────────┬───────────┘
                                    │
                       ┌────────────┴────────────┐
                       │                         │
                       ▼                         ▼
              ┌─────────────────┐      ┌─────────────────┐
              │      MySQL      │      │     SQLite      │
              │  Primary Engine │      │ Portable Fallback│
              └─────────────────┘      └─────────────────┘
                       │                         │
                       └────────────┬────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │   Queries & Analytics│
                         │      queries.py      │
                         └──────────────────────┘
````

---

## Database Design

The database contains **12 relational entities**:

```text
HR_MANAGER
DEPARTMENT
EMPLOYEE
PROJECT
EMPLOYEE_PROJECT
ATTENDANCE
LEAVE
PAYROLL
PERFORMANCE_REVIEW
TRAINING
EMPLOYEE_TRAINING
RECRUITMENT
```

### Entity Relationships

```text
                         HR_MANAGER
                              │
                              │ 1:M
                              ▼
                         DEPARTMENT
                              │
                              │ 1:M
                              ▼
                          EMPLOYEE
                         /   │   \
                        /    │    \
                       ▼     ▼     ▼
                ATTENDANCE  LEAVE  PAYROLL
                             
                          EMPLOYEE
                         /        \
                        /          \
                       ▼            ▼
              EMPLOYEE_PROJECT  EMPLOYEE_TRAINING
                    │                 │
                    ▼                 ▼
                 PROJECT           TRAINING

                    EMPLOYEE
                       │
                       ▼
              PERFORMANCE_REVIEW

                    RECRUITMENT
```

The complete EER design and relationship cardinalities are documented in:

```text
docs/EER_DIAGRAM.md
```

---

## Normalization

The database follows normalization principles through **1NF, 2NF, and 3NF**.

### First Normal Form — 1NF

* Attributes contain atomic values.
* Repeating and multi-valued relationships are separated.
* Many-to-many relationships are represented using bridge tables.

Examples:

```text
EMPLOYEE_PROJECT
EMPLOYEE_TRAINING
```

### Second Normal Form — 2NF

The design eliminates partial dependencies on composite keys.

For example:

```text
(Employee_ID, Project_ID) → Employee_Role
(Employee_ID, Project_ID) → Hours_Worked
```

Both attributes depend on the complete composite key.

### Third Normal Form — 3NF

Transitive dependencies are separated into independent relations.

For example:

```text
Employee_ID → Department_ID
Department_ID → Department_Name
```

Department-specific information is therefore maintained in the `DEPARTMENT` table rather than being unnecessarily repeated in `EMPLOYEE`.

Detailed normalization analysis is available in:

```text
docs/NORMALIZATION.md
```

---

## Functional Dependencies

The project documents the following functional dependencies:

```text
A  → B
B  → C
B  → D
D  → E
F  → G
F  → H
AF → I
AF → J
A  → D
AF → B
```

### Attribute Mapping

```text
A = Employee_ID
B = Department_ID
C = Department_Name
D = Manager_ID
E = Manager_Name
F = Project_ID
G = Project_Name
H = Project_Budget
I = Employee_Role
J = Hours_Worked
```

The complete mathematical analysis and normalization proof are provided in:

```text
docs/NORMALIZATION.md
```

---

## Project Structure

```text
Employee-and-HR-Management-Dashboard/
│
└── employee-hr-management-system/
    │
    ├── app.py
    ├── README.md
    ├── requirements.txt
    ├── LICENSE
    ├── run.bat
    ├── run.ps1
    │
    ├── database/
    │   ├── __init__.py
    │   ├── connection.py
    │   ├── queries.py
    │   └── hr_management_portable.db
    │
    ├── sql/
    │   ├── 01_schema.sql
    │   ├── 02_seed_data.sql
    │   └── 03_complex_queries.sql
    │
    ├── docs/
    │   ├── NORMALIZATION.md
    │   ├── EER_DIAGRAM.md
    │   └── ASSIGNMENT_REPORT.md
    │
    └── tests/
        └── test_system.py
```

---

## Database Files

### `01_schema.sql`

Contains the database schema and table definitions, including:

* Tables
* Primary keys
* Foreign keys
* Constraints
* Relationships
* Indexes

### `02_seed_data.sql`

Contains sample data used to populate the database for demonstration and testing.

### `03_complex_queries.sql`

Contains the predefined complex SQL queries used for the academic database requirements.

---

## SQL Queries

The project includes 10 complex SQL queries covering different database concepts.

### Query 1 — Department Budget vs Salary Expenditure

Analyses department budgets against actual salary expenditure.

Concepts:

* `LEFT JOIN`
* `GROUP BY`
* Aggregate functions
* Calculated percentages

### Query 2 — Cross-Department Project Workload

Analyses project staffing and employee hours.

Concepts:

* Many-to-many relationships
* Bridge-table aggregation
* `JOIN`
* `GROUP BY`

### Query 3 — Top Performers by Department

Ranks employees according to their performance within departments.

Concepts:

* CTE
* Window functions
* `DENSE_RANK()`
* `PARTITION BY`

### Query 4 — Training Program ROI

Analyses training participation and assessment performance.

Concepts:

* Multiple joins
* Aggregation
* `HAVING`
* Average calculations

### Query 5 — Monthly Payroll Reconciliation

Analyses payroll components including:

* Basic salary
* Allowances
* Deductions
* Net salary

### Query 6 — Employee 360-Degree Profile

Combines information from multiple entities to provide a broader employee profile.

### Query 7 — Attendance Compliance

Analyses attendance and work patterns using conditional aggregation.

### Query 8 — Leave Request Analysis

Analyses leave categories, statuses, and approval information.

### Query 9 — Recruitment Conversion Funnel

Tracks candidate progression through recruitment stages.

### Query 10 — Salary Equity Analysis

Analyses:

* Minimum salary
* Maximum salary
* Average salary
* Salary variation
* Department-level salary differences

---

## Quick Start

### Prerequisites

Install the following:

* Python 3.10 or newer
* Git
* MySQL 8.0+ *(optional)*

MySQL is optional because the application includes a portable SQLite database.

---

## 1. Clone the Repository

```bash
git clone https://github.com/AnanyaHarithas2607/Employee-and-HR-Management-Dashboard.git
```

Move into the application directory:

```bash
cd Employee-and-HR-Management-Dashboard/employee-hr-management-system
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

On Windows, if `python` is mapped to another Python installation, use:

```powershell
py -m pip install -r requirements.txt
```

---

## 4. Run the Application

### Recommended

```bash
python -m streamlit run app.py
```

On Windows, you can also use the included launcher:

```text
run.bat
```

or:

```powershell
.\run.ps1
```

The Streamlit dashboard will be available at:

```text
http://localhost:8501
```

---

# MySQL Configuration

The application can connect to a local MySQL database.

Typical configuration:

```text
Host: localhost
Port: 3306
User: root
Database: hr_management
Password: <your MySQL password>
```

After starting MySQL:

1. Launch the Streamlit application.
2. Enter the MySQL connection details.
3. Connect to the database.
4. Initialize the database if required.

The database schema and seed files are available under:

```text
sql/
```

### Manual MySQL Initialization

If required, initialize the schema:

```bash
mysql -u root -p < sql/01_schema.sql
```

Then load the sample data:

```bash
mysql -u root -p < sql/02_seed_data.sql
```

---

# SQLite Portable Mode

The project includes a portable SQLite database:

```text
database/hr_management_portable.db
```

SQLite mode allows the project to run without a separate MySQL server.

This is useful for:

* Demonstrations
* Academic evaluation
* Offline execution
* Testing
* Quick setup

The application can use the SQLite database when MySQL is unavailable.

---

# Testing

System tests are provided in:

```text
tests/test_system.py
```

Run the test file using:

```bash
python tests/test_system.py
```

On Windows:

```powershell
py tests/test_system.py
```

---

# Documentation

Additional project documentation is available in the `docs` directory.

### Normalization Documentation

```text
docs/NORMALIZATION.md
```

Contains:

* Functional dependencies
* Attribute mapping
* 1NF analysis
* 2NF analysis
* 3NF analysis
* Normalization proof
* Armstrong's axioms

### EER Diagram

```text
docs/EER_DIAGRAM.md
```

Contains:

* Entity relationships
* Cardinalities
* EER representation
* Database structure

### Assignment Report

```text
docs/ASSIGNMENT_REPORT.md
```

Contains the detailed academic documentation for the project.

---

# Dashboard Preview

Add screenshots of the application here after uploading them to the repository.

Example:

```text
docs/images/dashboard.png
docs/images/employee-directory.png
docs/images/payroll.png
docs/images/sql-studio.png
```

Recommended screenshots:

1. Executive Dashboard
2. Employee Directory
3. Department & Budget Analysis
4. Payroll Dashboard
5. Recruitment Funnel
6. SQL Studio

---

# Security

Do not commit actual database passwords or private credentials to GitHub.

If environment variables are used, keep actual credentials in a local `.env` file.

Example configuration:

```text
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=hr_management
```

Do not upload a `.env` file containing real credentials.

---

# Academic Requirements Covered

This project demonstrates:

* [x] EER modelling
* [x] Relational database design
* [x] Functional dependencies
* [x] First Normal Form
* [x] Second Normal Form
* [x] Third Normal Form
* [x] Primary keys
* [x] Foreign keys
* [x] Referential integrity
* [x] One-to-many relationships
* [x] Many-to-many relationships
* [x] Bridge tables
* [x] CRUD operations
* [x] SQL joins
* [x] Aggregation
* [x] Subqueries
* [x] Common Table Expressions
* [x] Window functions
* [x] Conditional aggregation
* [x] Database connectivity
* [x] Data visualization
* [x] Interactive dashboard
* [x] Automated testing
* [x] Academic documentation

---

# Future Enhancements

Possible future improvements include:

* Role-based authentication
* HR administrator login
* Advanced employee analytics
* Exporting reports to PDF/Excel
* Email notifications
* Advanced recruitment analytics
* Additional dashboard filters
* Cloud database deployment
* Deployment to a cloud hosting platform

---

# Repository

GitHub:

[https://github.com/AnanyaHarithas2607/Employee-and-HR-Management-Dashboard](https://github.com/AnanyaHarithas2607/Employee-and-HR-Management-Dashboard)

---

