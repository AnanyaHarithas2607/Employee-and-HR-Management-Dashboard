# 🏢 Employee & HR Management System

[![Database](https://img.shields.io/badge/Database-MySQL%208.0%2B-blue.svg)](https://www.mysql.com/)
[![Frontend](https://img.shields.io/badge/Frontend-Streamlit-red.svg)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-yellow.svg)](https://www.python.org/)
[![Normalization](https://img.shields.io/badge/Normalization-3NF-success.svg)](docs/NORMALIZATION.md)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An interactive **Employee & Human Resources Management System** built using
**Python, Streamlit, Plotly, MySQL, and SQLite**.

The project combines a normalized relational database design with an
interactive web dashboard for employee management, attendance, leave,
payroll, performance, training, recruitment, project allocation, and
analytics.

It was developed as a university-level database project with emphasis on
**EER modelling, functional dependencies, normalization up to 3NF,
relational integrity, SQL queries, and interactive data visualization**.

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
- Primary keys and foreign keys
- Referential integrity and cascade rules
- Many-to-many relationships through bridge tables
- MySQL 8.0+ support
- Built-in SQLite portable database fallback

### 📊 Interactive Dashboard

The Streamlit dashboard provides:

- Executive KPI dashboard
- Employee directory
- Employee search and filtering
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
- Interactive charts using Plotly

### 🔎 Employee Search

The employee directory supports multi-criteria filtering including:

- Employee ID
- Employee name
- Department
- Job title
- Salary range
- Other employee attributes

### 💾 Dual Database Architecture

The application supports two database engines:

**MySQL**
- Primary relational database
- Suitable for full database deployment
- Supports the complete SQL schema and seed data

**SQLite**
- Portable local database
- Requires no MySQL server
- Allows the dashboard to run without additional database configuration

The application can fall back to the portable SQLite database when MySQL is unavailable.

---

## 📐 Database Design

The system follows relational database normalization principles.

### Functional Dependencies

The project uses the following functional dependencies:

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
