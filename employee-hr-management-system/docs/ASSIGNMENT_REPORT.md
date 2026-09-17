# Academic Project Report: Employee & HR Management System

**Course Module**: Relational Database Management Systems (RDBMS) / Database Design  
**Topic**: Enhanced Entity-Relationship (EER) Modeling, Functional Dependencies, Relational Decomposition (3NF), and Interactive Web Dashboard  
**Database Backend**: MySQL 8.0+  
**Application Tier**: Python, Streamlit, Plotly, SQLAlchemy / PyMySQL  

---

## Executive Summary
This project implements an end-to-end **Employee & Human Resources Management System** constructed from rigorous database theory principles. Starting from a specified set of real-world attributes and 10 Functional Dependencies ($F$), the system demonstrates:
1. Conceptual modeling via an Enhanced Entity-Relationship (EER) diagram.
2. Formal normalization through First (1NF), Second (2NF), and Third Normal Form (3NF).
3. Implementation of the physical relational schema in MySQL with Primary Keys, Foreign Keys, Referential Integrity constraints (`CASCADE` / `RESTRICT`), and performance indexes.
4. Development of an interactive executive and managerial dashboard providing real-time data visualisations, automated payroll and performance tracking, and an analytical SQL query console.

---

## 1. Problem Statement & Functional Dependencies

The organization requires a centralized database to record employee profiles, department allocations, managerial reporting, project assignments, daily attendance logs, leave processing, monthly payroll disbursements, annual performance evaluations, training programs, and recruitment candidate workflows.

Given attributes:
- $A$: `Employee_ID`
- $B$: `Department_ID`
- $C$: `Department_Name`
- $D$: `Manager_ID`
- $E$: `Manager_Name`
- $F$: `Project_ID`
- $G$: `Project_Name`
- $H$: `Project_Budget`
- $I$: `Employee_Role`
- $J$: `Hours_Worked`

The functional dependencies governing the relations are:
1. $A \to B$
2. $B \to C$
3. $B \to D$
4. $D \to E$
5. $F \to G$
6. $F \to H$
7. $AF \to I$
8. $AF \to J$
9. $A \to D$ (Transitive)
10. $AF \to B$ (Augmentation)

---

## 2. Normalization Steps Summary

- **1NF**: Decomposed repeating groups into independent bridge tables (`EMPLOYEE_PROJECT` and `EMPLOYEE_TRAINING`). All attributes are atomic.
- **2NF**: Eliminated partial dependencies on composite keys. In `EMPLOYEE_PROJECT(employee_id, project_id)`, both `employee_role` ($I$) and `hours_worked` ($J$) require the full candidate key $\{A, F\}$. Project attributes ($G, H$) are isolated in `PROJECT`.
- **3NF**: Eliminated transitive dependencies. In an unnormalized employee relation, $A \to B$ and $B \to C, D$ would create transitive dependencies on non-candidate keys. Decomposing into `DEPARTMENT` with primary key $B$ eliminates these transitive paths while preserving all dependencies.

---

## 3. Relational Schema Structure (12 Tables)

1. `HR_MANAGER`: Stores HR professionals and leadership credentials.
2. `DEPARTMENT`: Stores distinct organizational units, budgets, and managers.
3. `EMPLOYEE`: Core workforce profiles with demographics, department FK, and HR FK.
4. `PROJECT`: Strategic client and internal projects linked to owning departments.
5. `EMPLOYEE_PROJECT`: Resolves $M:N$ project staffing, capturing roles and hours logged.
6. `ATTENDANCE`: High-frequency daily clock-in/out and work hours logs.
7. `LEAVE`: Vacation, casual, and sick leave requests with approval status workflows.
8. `PAYROLL`: Detailed monthly basic salary, allowances, tax deductions, and net payouts.
9. `PERFORMANCE_REVIEW`: Managerial evaluations with 1-5 rating metrics and comments.
10. `TRAINING`: Upskilling and compliance courses with trainer details and budget costs.
11. `EMPLOYEE_TRAINING`: Resolves $M:N$ course attendance, tracking completion status and scores.
12. `RECRUITMENT`: Hiring funnel tracking candidate interviews and job offers.

---

## 4. Complex Analytical Queries Implemented
The project includes 10 complex queries demonstrating:
- Budget variance and consumption percentages.
- Employee utilization per project.
- Window functions (`DENSE_RANK()`) for intra-departmental performance ranking.
- Return on Investment (ROI) and average scores across training programs.
- Recruitment conversion funnel rates.
- Cross-table 360-degree employee profile consolidation.

---

## 5. Software Architecture & Dashboard Capabilities
The web dashboard provides:
- **Executive KPI Cards**: Real-time headcount, payroll totals, active projects, and attendance compliance.
- **Visual Analytics**: Interactive Plotly charts (budget distributions, salary histograms, project workload breakdowns).
- **CRUD Operations**: Interactive forms to register new employees, update details, assign project roles, log attendance, and approve leave requests.
- **Interactive SQL Studio**: Enables professors and evaluators to run arbitrary SQL statements or test pre-configured queries in real time.
- **Dual-Engine Resilience**: Seamlessly operates on native MySQL 8.0+ or zero-config fallback SQLite for offline portability.

---

## 6. Conclusion
The system satisfies all theoretical principles of database design, achieving 3NF compliance, lossless decomposition, and high query efficiency, accompanied by an enterprise-grade web interface.
