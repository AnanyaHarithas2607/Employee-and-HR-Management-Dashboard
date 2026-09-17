# Enhanced Entity-Relationship (EER) Model Documentation

This document describes the conceptual and logical architecture of the **Employee & HR Management System**, translating the EER diagram directly into relational database specifications.

---

## 1. System EER Architecture Diagram (Mermaid)

```mermaid
erDiagram
    HR_MANAGER ||--o{ EMPLOYEE : "oversees (1:M)"
    HR_MANAGER ||--o{ RECRUITMENT : "coordinates (1:M)"
    DEPARTMENT ||--o{ EMPLOYEE : "employs (1:M)"
    DEPARTMENT ||--o{ PROJECT : "initiates (1:M)"

    EMPLOYEE ||--o{ ATTENDANCE : "logs (1:M)"
    EMPLOYEE ||--o{ LEAVE : "requests (1:M)"
    EMPLOYEE ||--o{ PAYROLL : "receives (1:M)"
    EMPLOYEE ||--o{ PERFORMANCE_REVIEW : "evaluated_by (1:M)"

    EMPLOYEE ||--o{ EMPLOYEE_PROJECT : "assigned_to (M:N)"
    PROJECT ||--o{ EMPLOYEE_PROJECT : "staffed_by (M:N)"

    EMPLOYEE ||--o{ EMPLOYEE_TRAINING : "attends (M:N)"
    TRAINING ||--o{ EMPLOYEE_TRAINING : "trains (M:N)"

    HR_MANAGER {
        int hr_id PK
        string hr_name
        string email UK
        string phone_number
        string designation
        int experience_years
    }

    DEPARTMENT {
        int department_id PK
        string department_name UK
        string location
        decimal budget
        string manager_name
    }

    EMPLOYEE {
        int employee_id PK
        string first_name
        string last_name
        string gender
        date date_of_birth
        string email UK
        string phone_number
        string address
        date hire_date
        decimal salary
        string job_title
        int department_id FK
        int hr_id FK
    }

    PROJECT {
        int project_id PK
        string project_name
        date start_date
        date end_date
        decimal budget
        string client_name
        string status
        int department_id FK
    }

    EMPLOYEE_PROJECT {
        int employee_id PK, FK
        int project_id PK, FK
        date assigned_date
        string employee_role
        decimal hours_worked
    }

    ATTENDANCE {
        int attendance_id PK
        int employee_id FK
        date date
        time check_in_time
        time check_out_time
        decimal work_hours
        string attendance_status
    }

    LEAVE {
        int leave_id PK
        int employee_id FK
        string leave_type
        date start_date
        date end_date
        text reason
        string approval_status
    }

    PAYROLL {
        int payroll_id PK
        int employee_id FK
        decimal basic_salary
        decimal allowances
        decimal deductions
        decimal net_salary
        date payment_date
    }

    PERFORMANCE_REVIEW {
        int review_id PK
        int employee_id FK
        string reviewer_name
        date review_date
        int rating
        text comments
    }

    TRAINING {
        int training_id PK
        string training_name
        string trainer_name
        date start_date
        date end_date
        string training_type
        decimal cost
    }

    EMPLOYEE_TRAINING {
        int employee_id PK, FK
        int training_id PK, FK
        string completion_status
        decimal score
    }

    RECRUITMENT {
        int recruitment_id PK
        string candidate_name
        string position_applied
        date interview_date
        string interview_status
        string offer_status
        int hr_id FK
    }
```

---

## 2. Generalization / Specialization Hierarchy

In the EER conceptual model:
- **Superclass**: `HR_PERSON`
  - Attributes: `HR_ID`, `Name`, `Email`, `Phone`, `Designation`
- **Subclasses**:
  - `HR_MANAGER`: Focuses on organizational governance, experience level, department alignment.
  - `RECRUITMENT_OFFICER`: Focuses on applicant sourcing, interview tracking, and hiring quotas.

### Relational Mapping Choice:
To maximize performance and eliminate unnecessary outer joins for transactional HR queries, this hierarchy is represented via the **`HR_MANAGER`** entity acting as the core HR authority, coupled with foreign key associations into the `RECRUITMENT` entity (`HR_ID` FK).

---

## 3. Cardinalities and Referential Integrity Rules

| Parent Entity | Child Entity | Cardinality | FK Constraint | Delete Rule | Update Rule |
|---|---|---|---|---|---|
| `DEPARTMENT` | `EMPLOYEE` | 1 : M | `department_id` | `RESTRICT` | `CASCADE` |
| `HR_MANAGER` | `EMPLOYEE` | 1 : M | `hr_id` | `RESTRICT` | `CASCADE` |
| `DEPARTMENT` | `PROJECT` | 1 : M | `department_id` | `RESTRICT` | `CASCADE` |
| `EMPLOYEE` | `ATTENDANCE` | 1 : M | `employee_id` | `CASCADE` | `CASCADE` |
| `EMPLOYEE` | `LEAVE` | 1 : M | `employee_id` | `CASCADE` | `CASCADE` |
| `EMPLOYEE` | `PAYROLL` | 1 : M | `employee_id` | `CASCADE` | `CASCADE` |
| `EMPLOYEE` | `PERFORMANCE_REVIEW` | 1 : M | `employee_id` | `CASCADE` | `CASCADE` |
| `HR_MANAGER` | `RECRUITMENT` | 1 : M | `hr_id` | `RESTRICT` | `CASCADE` |
| `EMPLOYEE` & `PROJECT` | `EMPLOYEE_PROJECT` | M : N | `(employee_id, project_id)` | `CASCADE` | `CASCADE` |
| `EMPLOYEE` & `TRAINING` | `EMPLOYEE_TRAINING` | M : N | `(employee_id, training_id)` | `CASCADE` | `CASCADE` |

- **Delete Rule Justification**:
  - Operational logs (`attendance`, `leave`, `payroll`, `reviews`) are tied directly to an employee's lifecycle and cascade when an employee record is expunged.
  - Organizational units (`department`, `hr_manager`) use `RESTRICT` so that departments cannot be accidentally purged while employees or projects remain assigned to them.
