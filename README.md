````markdown
# 🏢 Employee & HR Management System

[![Database](https://img.shields.io/badge/Database-MySQL%208.0%2B-blue.svg)](https://www.mysql.com/)
[![Frontend](https://img.shields.io/badge/Frontend-Streamlit-red.svg)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-yellow.svg)](https://www.python.org/)
[![Normalization](https://img.shields.io/badge/Normalization-3NF-success.svg)](docs/NORMALIZATION.md)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An interactive **Employee & Human Resources Management System** built using **Python, Streamlit, Plotly, MySQL, and SQLite**.

The system combines a normalized relational database with an interactive dashboard for employee management, attendance, leave, payroll, performance, training, recruitment, project allocation, and analytics.

---

## ✨ Features

### 🗄️ Database Management

- 12 normalized relational entities:
  - `HR_MANAGER`
  - `DEPARTMENT`
  - `EMPLOYEE`
  - `PROJECT`
  - `EMPLOYEE_PROJECT`
  - `ATTENDANCE`
  - `LEAVE`
  - `PAYROLL`
  - `PERFORMANCE_REVIEW`
  - `TRAINING`
  - `EMPLOYEE_TRAINING`
  - `RECRUITMENT`
- Primary and foreign keys
- Referential integrity and cascade rules
- Many-to-many relationships using bridge tables
- MySQL 8.0+ support
- Portable SQLite database fallback

### 📊 Interactive Dashboard

- Executive KPI dashboard
- Employee directory and search
- Multi-criteria employee filtering
- Employee registration
- Department budget analysis
- Project staffing and employee roles
- Project hours tracking
- Attendance analytics
- Leave management and approval
- Payroll and salary analysis
- Performance review analytics
- Training analytics
- Recruitment funnel
- Interactive Plotly visualizations
- Interactive SQL Studio

### 🔎 Employee Search

The employee directory supports filtering by:

- Employee ID
- Employee name
- Department
- Job title
- Salary range
- Other employee attributes

### 💾 Dual Database Architecture

The application supports:

**MySQL**
- Primary relational database
- Full database deployment
- Complete schema and seed data

**SQLite**
- Portable local database
- No MySQL server required
- Useful for demonstrations, testing, and offline execution

If MySQL is unavailable, the application can use the portable SQLite database.

---

## 📐 Database Design

The database follows **1NF, 2NF, and 3NF** normalization principles.

### Functional Dependencies

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
````

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

### Normalization

**1NF**

* All attributes contain atomic values.
* Many-to-many relationships are decomposed into bridge tables such as `EMPLOYEE_PROJECT` and `EMPLOYEE_TRAINING`.

**2NF**

* Non-key attributes depend on the complete composite key.
* For example:

```text
(Employee_ID, Project_ID) → Employee_Role
(Employee_ID, Project_ID) → Hours_Worked
```

**3NF**

* Transitive dependencies are separated into independent relations.

```text
Employee_ID → Department_ID
Department_ID → Department_Name
```

Detailed normalization documentation is available in:

```text
docs/NORMALIZATION.md
```

---

## 📊 Dashboard Modules

### 1. Executive Dashboard

Displays:

* Total employees
* Monthly payroll
* Active projects
* Attendance statistics
* Average performance rating

### 2. Employee Management

Provides:

* Employee directory
* Employee search
* Employee filtering
* Salary filtering
* Employee registration

### 3. Department & Budget

Provides:

* Department budgets
* Payroll expenditure
* Budget utilization
* Employee distribution

### 4. Project Management

Tracks:

* Employee-project assignments
* Employee roles
* Project staffing
* Hours worked
* Project budgets

### 5. Attendance & Leave

Provides:

* Attendance breakdown
* Check-in status
* Leave requests
* Leave approval workflow

### 6. Payroll

Provides:

* Salary distributions
* Basic salary analysis
* Allowances
* Deductions
* Net salary reconciliation

### 7. Performance & Training

Provides:

* Performance rating distributions
* Top-performing employees
* Training participation
* Training assessment analysis
* Training ROI metrics

### 8. Recruitment

Provides a recruitment funnel:

```text
Application
    ↓
Interview
    ↓
Offer
    ↓
Acceptance
```

### 9. SQL Studio

Allows users to:

* Execute SQL queries
* View query results
* Run predefined academic queries
* Analyze database tables interactively

---

## 📁 Project Structure

```text
Employee-and-HR-Management-Dashboard/
│
├── employee-hr-management-system/
│   ├── app.py
│   ├── README.md
│   ├── requirements.txt
│   ├── run.bat
│   ├── run.ps1
│   ├── LICENSE
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── queries.py
│   │   └── hr_management_portable.db
│   │
│   ├── sql/
│   │   ├── 01_schema.sql
│   │   ├── 02_seed_data.sql
│   │   └── 03_complex_queries.sql
│   │
│   ├── docs/
│   │   ├── NORMALIZATION.md
│   │   ├── EER_DIAGRAM.md
│   │   └── ASSIGNMENT_REPORT.md
│   │
│   └── tests/
│       └── test_system.py
│
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

* Python 3.10+
* Git
* MySQL 8.0+ *(optional when using SQLite fallback)*

### 1. Clone the Repository

```bash
git clone https://github.com/AnanyaHarithas2607/Employee-and-HR-Management-Dashboard.git
cd Employee-and-HR-Management-Dashboard/employee-hr-management-system
```

### 2. Install Dependencies

#### Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the Dashboard

```bash
python -m streamlit run app.py
```

Or on Windows:

```text
run.bat
```

or:

```powershell
.\run.ps1
```

The dashboard will open at:

```text
http://localhost:8501
```

---

## 🗄️ MySQL Configuration

MySQL is optional because the project includes a portable SQLite database.

To use MySQL:

1. Start your MySQL server.
2. Open the dashboard.
3. Enter the MySQL connection details.
4. Click **Connect & Initialize MySQL**.

Typical configuration:

```text
Host: localhost
Port: 3306
User: root
Database: hr_management
Password: <your MySQL password>
```

The SQL initialization scripts are:

```text
sql/01_schema.sql
sql/02_seed_data.sql
```

They can also be executed manually:

```bash
mysql -u root -p < sql/01_schema.sql
mysql -u root -p < sql/02_seed_data.sql
```

---

## 💾 SQLite Portable Mode

The project includes:

```text
database/hr_management_portable.db
```

SQLite mode allows the dashboard to run without a MySQL server.

It is useful for:

* Demonstrations
* Academic evaluation
* Offline execution
* Testing
* Quick setup

---

## 🧪 Testing

System tests are available in:

```text
tests/test_system.py
```

Run:

```bash
python tests/test_system.py
```

---

## 📚 SQL Assignment Queries

The project includes 10 complex SQL queries in:

```text
sql/03_complex_queries.sql
```

The queries cover:

1. Department budget vs salary expenditure
2. Cross-department project workload
3. Top performers ranked by department
4. Training program ROI
5. Monthly payroll reconciliation
6. Employee 360-degree profile
7. Attendance compliance
8. Leave approval analysis
9. Recruitment conversion funnel
10. Salary equity and departmental salary spread

SQL concepts demonstrated include:

* `JOIN`
* `LEFT JOIN`
* `GROUP BY`
* `HAVING`
* Subqueries
* Common Table Expressions
* Window functions
* Conditional aggregation
* Aggregate functions

---

## 📖 Documentation

### Normalization

```text
docs/NORMALIZATION.md
```

Contains:

* Functional dependencies
* Attribute definitions
* 1NF analysis
* 2NF analysis
* 3NF analysis
* Armstrong's axioms
* Canonical cover analysis

### EER Diagram

```text
docs/EER_DIAGRAM.md
```

Contains the Entity-Relationship design and relationship cardinalities.

### Assignment Report

```text
docs/ASSIGNMENT_REPORT.md
```

Contains the detailed academic project report.

---

## 🔐 Security

Do not commit real database credentials to GitHub.

Keep actual MySQL passwords in a local `.env` file when environment-based configuration is used.

Use `.env.example` as the configuration template.

---

## 🛠️ Technologies Used

| Technology | Purpose                      |
| ---------- | ---------------------------- |
| Python     | Application logic            |
| Streamlit  | Interactive web dashboard    |
| Plotly     | Data visualization           |
| MySQL      | Relational database          |
| SQLite     | Portable database fallback   |
| SQL        | Database design and querying |
| Pandas     | Data processing              |
| Git/GitHub | Version control              |

---

## 🎓 Academic Objectives

This project demonstrates:

* Relational database design
* EER modelling
* Functional dependencies
* Database normalization
* 1NF, 2NF, and 3NF
* Primary and foreign keys
* Referential integrity
* Many-to-many relationships
* SQL joins and aggregation
* Subqueries
* CTEs
* Window functions
* CRUD operations
* Database connectivity
* Data visualization
* Interactive dashboard development

---

## 📄 License

This project is licensed under the MIT License.

See [LICENSE](LICENSE) for details.

```
```
