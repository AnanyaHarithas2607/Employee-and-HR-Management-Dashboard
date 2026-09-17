# 🏢 Employee & HR Management System

[![Database](https://img.shields.io/badge/Database-MySQL%208.0%2B-blue.svg)](https://www.mysql.com/)
[![Normalization](https://img.shields.io/badge/Normalization-Strict%203NF-success.svg)](docs/NORMALIZATION.md)
[![Frontend](https://img.shields.io/badge/Frontend-Streamlit%201.35%2B-red.svg)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade, academic **Employee & Human Resources Management System** built with **MySQL** and **Python (Streamlit + Plotly)**. Designed from foundational database normalization principles (1NF, 2NF, 3NF) and the Enhanced Entity-Relationship (EER) model, this project satisfies all requirements for a university-level graded database assignment and portfolio showcase.

---

## 📸 System Overview

```
                               ┌────────────────────────┐
                               │       HR_MANAGER       │
                               └───────────┬────────────┘
                                           │ 1:M
                        ┌──────────────────┴──────────────────┐
                        │                                     │
                        ▼                                     ▼
             ┌─────────────────────┐               ┌─────────────────────┐
             │     RECRUITMENT     │               │      EMPLOYEE       │
             └─────────────────────┘               └──────────┬──────────┘
                                                              │
         ┌──────────────┬──────────────┬──────────────┬───────┴───────┬──────────────┐
         ▼              ▼              ▼              ▼               ▼              ▼
   ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐   ┌───────────┐  ┌───────────┐
   │ATTENDANCE │  │   LEAVE   │  │  PAYROLL  │  │PERFORMANCE│   │ EMPLOYEE_ │  │ EMPLOYEE_ │
   │           │  │           │  │           │  │  REVIEW   │   │  PROJECT  │  │ TRAINING  │
   └───────────┘  └───────────┘  └───────────┘  └───────────┘   └─────┬─────┘  └─────┬─────┘
                                                                      │ M:N          │ M:N
                                                                ┌─────▼─────┐  ┌─────▼─────┐
                                                                │  PROJECT  │  │ TRAINING  │
                                                                └───────────┘  └───────────┘
```

---

## ✨ Features & Capabilities

- **12 Normalized Relational Entities**:
  - `HR_MANAGER`, `DEPARTMENT`, `EMPLOYEE`, `PROJECT`, `EMPLOYEE_PROJECT` (M:N), `ATTENDANCE`, `LEAVE`, `PAYROLL`, `PERFORMANCE_REVIEW`, `TRAINING`, `EMPLOYEE_TRAINING` (M:N), and `RECRUITMENT`.
- **Mathematical 3NF Rigor**:
  - Implements the complete set of 10 Functional Dependencies ($A \to B, B \to C, \dots, AF \to I, AF \to J$) with zero partial or transitive dependencies.
- **Interactive Web Dashboard**:
  - **Executive KPI Cards**: Real-time metrics on headcount, total monthly payroll, active client projects, company attendance compliance, and average performance rating.
  - **Employee Directory & CRUD**: Real-time multi-criteria search, salary filtering, and an intuitive form to register new employees.
  - **Department & Budget Insights**: Department budget consumption vs. actual payroll expenditure.
  - **Project Staffing & Hours**: Track team allocations, employee project roles, and contributed hours ($AF \to I, AF \to J$).
  - **Attendance & Leave Manager**: Check-in status breakdown and 1-click managerial leave request approvals.
  - **Payroll & Compensation**: Salary distribution histograms and net salary reconciliation.
  - **Performance & Training Hub**: Rating distributions, top performers, and training ROI metrics.
  - **Recruitment Funnel**: Visual candidate lifecycle from interview to offer acceptance.
  - **Interactive SQL Studio**: Run arbitrary custom SQL queries or test 10 pre-loaded graded assignment queries with instant data tables.
  - **Theory & Normalization Viewer**: Interactive breakdown of the 10 Functional Dependencies and 3NF formal proofs directly in the app.
- **Dual-Engine Architecture**:
  - Fully integrated with **MySQL 8.0+**.
  - Includes a built-in **zero-configuration portable engine (SQLite)** so evaluators can run and grade the project instantly even without an active MySQL server!

---

## 📐 Functional Dependencies & 3NF Normalization

### Attribute Symbols:
- **$A$**: `Employee_ID` | **$B$**: `Department_ID` | **$C$**: `Department_Name` | **$D$**: `Manager_ID` | **$E$**: `Manager_Name`
- **$F$**: `Project_ID` | **$G$**: `Project_Name` | **$H$**: `Project_Budget` | **$I$**: `Employee_Role` | **$J$**: `Hours_Worked`

### Functional Dependencies ($F$):
$$F = \{ A \to B,\; B \to C,\; B \to D,\; D \to E,\; F \to G,\; F \to H,\; AF \to I,\; AF \to J,\; A \to D,\; AF \to B \}$$

### Normalization Justification:
- **1NF**: Atomic values for all attributes; multi-valued assignments decomposed into `EMPLOYEE_PROJECT` and `EMPLOYEE_TRAINING`.
- **2NF**: No partial dependencies on composite keys. Non-key attributes `Employee_Role` ($I$) and `Hours_Worked` ($J$) depend fully on the complete composite key $\{A, F\}$.
- **3NF**: Elimination of transitive dependencies. The dependencies $A \to B$ and $B \to C, D \to E$ are decoupled into the dedicated `DEPARTMENT` and `HR_MANAGER` tables.

> 📖 *For the complete mathematical proof and canonical cover analysis, see [docs/NORMALIZATION.md](docs/NORMALIZATION.md).*

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.10+**
- *(Optional)* **MySQL Server 8.0+** / XAMPP / MariaDB (If offline, the portable database will run automatically).

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/employee-hr-management-system.git
cd employee-hr-management-system
```

### 2. Set Up Virtual Environment & Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# On Windows Command Prompt:
.\.venv\Scripts\activate.bat
# On macOS/Linux:
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. (Optional) Configure MySQL Server
1. Start your local MySQL service (e.g. via MySQL Workbench, Command Line, or XAMPP).
2. Copy `.env.example` to `.env` and configure your credentials:
   ```ini
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=hr_management
   ```
3. Run the SQL initialization scripts:
   ```bash
   mysql -u root -p < sql/01_schema.sql
   mysql -u root -p < sql/02_seed_data.sql
   ```
   *(Note: If you run the app without executing this manual step, the dashboard will automatically initialize the database schema and seed data for you!)*

### 4. Launch the Dashboard
- **Windows (1-Click)**: Double-click `run.bat` or execute `./run.ps1` in PowerShell.
- **Terminal**:
  ```bash
  streamlit run app.py
  ```
The dashboard will open automatically in your browser at `http://localhost:8501`.

---

## 🗄️ Project Directory Structure

```
employee-hr-management-system/
├── .env.example                     # MySQL credentials template
├── .gitignore                       # Standard Git exclusions
├── LICENSE                          # MIT Open-Source License
├── README.md                        # Project documentation (this file)
├── requirements.txt                 # Dependencies
├── run.bat                          # 1-click Windows launcher
├── run.ps1                          # PowerShell launcher
├── app.py                           # Main Streamlit web application
├── sql/
│   ├── 01_schema.sql                # 12-table MySQL DDL with 3NF constraints & indexes
│   ├── 02_seed_data.sql             # Comprehensive enterprise seed dataset
│   └── 03_complex_queries.sql       # 10 complex queries for academic grading
├── docs/
│   ├── NORMALIZATION.md             # Formal proof of 1NF, 2NF, 3NF & Armstrong's Axioms
│   ├── EER_DIAGRAM.md               # Mermaid EER diagram & cardinalities
│   └── ASSIGNMENT_REPORT.md         # Submission-ready academic project report
└── database/
    ├── __init__.py
    ├── connection.py                # MySQL connection manager with auto-fallback
    └── queries.py                   # Data queries, analytics, and pre-built queries catalog
```

---

## 📊 Graded Assignment SQL Queries

The repository includes 10 complex queries in `sql/03_complex_queries.sql` runnable directly via the **Interactive SQL Studio** tab in the dashboard:

1. **Department Budget vs Salary Expenditure**: `LEFT JOIN`, `GROUP BY`, budget consumption percentage calculation.
2. **Cross-Department Project Workload & Hours**: M:N bridge aggregation, hours logged per member ($AF \to I, AF \to J$).
3. **Top Performers Ranked by Department**: Window function `DENSE_RANK() OVER (PARTITION BY ...)` with Common Table Expression (CTE).
4. **Training Program ROI & Assessment Scores**: Multi-table aggregation with `HAVING` and average score computation.
5. **Monthly Payroll Reconciliation**: Financial summary auditing basic salary, allowances, deductions, and net pay.
6. **Employee 360-Degree Profile**: Multi-table join across Employee, Department, HR, Projects, and Training.
7. **Attendance Compliance & Remote Work Ratio**: Conditional aggregation (`CASE WHEN`) evaluating daily work patterns.
8. **Leave Request Approval Velocity**: Categorical breakdown of leave requests and approval rates.
9. **Recruitment Conversion Funnel**: Multi-entity analysis tracking candidate throughput from interview to offer acceptance.
10. **Salary Equity & Inter-Departmental Spread**: Minimum, Maximum, Average salary, and variance against company-wide mean.

---

## 📤 How to Upload to GitHub

Follow these steps to upload this project to your GitHub account:

1. **Create a new repository on GitHub**:
   - Go to [github.com/new](https://github.com/new).
   - Name your repository: `employee-hr-management-system`.
   - Set visibility to **Public**.
   - Do **NOT** check "Add a README file" (we already have a complete one).

2. **Push the project from your terminal**:
   ```bash
   cd "C:\Users\Ananya Harithas\.gemini\antigravity\scratch\employee-hr-management-system"
   git init
   git add .
   git commit -m "feat: complete Employee & HR Management System with MySQL and Streamlit dashboard"
   git branch -M main
   git remote add origin https://github.com/<your-username>/employee-hr-management-system.git
   git push -u origin main
   ```

---

## 🎓 Academic Submission Checklist

- [x] Functional Dependencies ($F$) clearly documented ($A \to B, \dots, AF \to J$).
- [x] Attribute domain table provided ($A$ through $J$).
- [x] Complete EER diagram with Generalization/Specialization and cardinalities.
- [x] Step-by-step mathematical proof for 1NF, 2NF, and 3NF.
- [x] Relational schema specified with Primary Keys, Foreign Keys, and cascade rules.
- [x] 12 Normalized tables implemented in MySQL DDL (`sql/01_schema.sql`).
- [x] Seed data provided with realistic records (`sql/02_seed_data.sql`).
- [x] 10 Complex SQL queries covering JOINs, Subqueries, and Window Functions (`sql/03_complex_queries.sql`).
- [x] Interactive web dashboard with real-time analytics and SQL execution console (`app.py`).
- [x] Clean GitHub repository setup with documentation and launcher scripts.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
