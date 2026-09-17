-- =============================================================================
-- EMPLOYEE & HR MANAGEMENT SYSTEM
-- Relational Database Schema (Normalized to 3NF)
-- Target RDBMS: MySQL 8.0+ / MariaDB / SQLite compatible
-- =============================================================================

DROP DATABASE IF EXISTS hr_management;
CREATE DATABASE IF NOT EXISTS hr_management;
USE hr_management;

-- -----------------------------------------------------------------------------
-- 1. Table: HR_MANAGER
-- Represents HR leadership and personnel managing employees and recruitment
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS hr_manager (
    hr_id INT AUTO_INCREMENT PRIMARY KEY,
    hr_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone_number VARCHAR(20) NOT NULL,
    designation VARCHAR(50) NOT NULL,
    experience_years INT NOT NULL CHECK (experience_years >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 2. Table: DEPARTMENT
-- Represents organizational units with budgets and designated managerial oversight
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS department (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    location VARCHAR(100) NOT NULL,
    budget DECIMAL(15, 2) NOT NULL CHECK (budget >= 0),
    manager_name VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 3. Table: EMPLOYEE
-- Core entity storing primary employee demographic, job, and compensation info
-- FDs: A -> B (Dept), A -> D (Manager via Dept), A -> all Employee attributes
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS employee (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender ENUM('Male', 'Female', 'Non-binary', 'Other') NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone_number VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL,
    hire_date DATE NOT NULL,
    salary DECIMAL(12, 2) NOT NULL CHECK (salary > 0),
    job_title VARCHAR(100) NOT NULL,
    department_id INT NOT NULL,
    hr_id INT NOT NULL,
    CONSTRAINT fk_emp_department FOREIGN KEY (department_id) 
        REFERENCES department(department_id) 
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_emp_hr FOREIGN KEY (hr_id) 
        REFERENCES hr_manager(hr_id) 
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 4. Table: PROJECT
-- Strategic client and internal projects owned by departments
-- FDs: F -> G (Project_Name), F -> H (Project_Budget)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS project (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(150) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    budget DECIMAL(15, 2) NOT NULL CHECK (budget >= 0),
    client_name VARCHAR(100) NOT NULL,
    status ENUM('Planning', 'Ongoing', 'On-Hold', 'Completed', 'Cancelled') NOT NULL DEFAULT 'Planning',
    department_id INT NOT NULL,
    CONSTRAINT fk_project_department FOREIGN KEY (department_id) 
        REFERENCES department(department_id) 
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 5. Table: EMPLOYEE_PROJECT (Bridge Table: M:N)
-- Resolves M:N relationship between Employee and Project
-- FDs: AF -> I (Employee_Role), AF -> J (Hours_Worked)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS employee_project (
    employee_id INT NOT NULL,
    project_id INT NOT NULL,
    assigned_date DATE NOT NULL,
    employee_role VARCHAR(100) NOT NULL,
    hours_worked DECIMAL(6, 2) NOT NULL DEFAULT 0.00 CHECK (hours_worked >= 0),
    PRIMARY KEY (employee_id, project_id),
    CONSTRAINT fk_ep_employee FOREIGN KEY (employee_id) 
        REFERENCES employee(employee_id) 
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_ep_project FOREIGN KEY (project_id) 
        REFERENCES project(project_id) 
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 6. Table: ATTENDANCE
-- Logs daily check-ins, check-outs, work hours, and statuses
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    date DATE NOT NULL,
    check_in_time TIME,
    check_out_time TIME,
    work_hours DECIMAL(4, 2) DEFAULT 0.00,
    attendance_status ENUM('Present', 'Absent', 'Half-Day', 'On-Leave', 'Remote') NOT NULL DEFAULT 'Present',
    CONSTRAINT fk_att_employee FOREIGN KEY (employee_id) 
        REFERENCES employee(employee_id) 
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT uq_emp_date UNIQUE (employee_id, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 7. Table: LEAVE
-- Tracks employee time-off requests, reasons, and management approval status
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `leave` (
    leave_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    leave_type ENUM('Casual', 'Sick', 'Annual', 'Maternity', 'Paternity', 'Unpaid') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT,
    approval_status ENUM('Pending', 'Approved', 'Rejected') NOT NULL DEFAULT 'Pending',
    CONSTRAINT fk_leave_employee FOREIGN KEY (employee_id) 
        REFERENCES employee(employee_id) 
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 8. Table: PAYROLL
-- Monthly salary disbursements, tax/pension deductions, allowances, and net pay
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS payroll (
    payroll_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    basic_salary DECIMAL(12, 2) NOT NULL,
    allowances DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    deductions DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    net_salary DECIMAL(12, 2) NOT NULL,
    payment_date DATE NOT NULL,
    CONSTRAINT fk_payroll_employee FOREIGN KEY (employee_id) 
        REFERENCES employee(employee_id) 
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 9. Table: PERFORMANCE_REVIEW
-- Annual/quarterly managerial evaluations, ratings (1-5), and feedback comments
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS performance_review (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    reviewer_name VARCHAR(100) NOT NULL,
    review_date DATE NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comments TEXT,
    CONSTRAINT fk_review_employee FOREIGN KEY (employee_id) 
        REFERENCES employee(employee_id) 
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 10. Table: TRAINING
-- Professional corporate training and skill development programs
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS training (
    training_id INT AUTO_INCREMENT PRIMARY KEY,
    training_name VARCHAR(150) NOT NULL,
    trainer_name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    training_type VARCHAR(50) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (cost >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 11. Table: EMPLOYEE_TRAINING (Bridge Table: M:N)
-- Resolves M:N relationship between Employee and Training sessions
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS employee_training (
    employee_id INT NOT NULL,
    training_id INT NOT NULL,
    completion_status ENUM('Enrolled', 'In Progress', 'Completed', 'Dropped') NOT NULL DEFAULT 'Enrolled',
    score DECIMAL(5, 2) CHECK (score BETWEEN 0.00 AND 100.00),
    PRIMARY KEY (employee_id, training_id),
    CONSTRAINT fk_et_employee FOREIGN KEY (employee_id) 
        REFERENCES employee(employee_id) 
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_et_training FOREIGN KEY (training_id) 
        REFERENCES training(training_id) 
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 12. Table: RECRUITMENT
-- Recruitment pipeline tracking applicants from interview to offer letter
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS recruitment (
    recruitment_id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_name VARCHAR(100) NOT NULL,
    position_applied VARCHAR(100) NOT NULL,
    interview_date DATE NOT NULL,
    interview_status ENUM('Scheduled', 'Completed', 'Cancelled', 'In Review') NOT NULL DEFAULT 'Scheduled',
    offer_status ENUM('Pending', 'Accepted', 'Declined', 'Rejected') NOT NULL DEFAULT 'Pending',
    hr_id INT NOT NULL,
    CONSTRAINT fk_recruitment_hr FOREIGN KEY (hr_id) 
        REFERENCES hr_manager(hr_id) 
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================================================
-- Performance Indexes for High-Traffic Analytical Queries
-- =============================================================================
CREATE INDEX idx_emp_dept ON employee(department_id);
CREATE INDEX idx_emp_hire ON employee(hire_date);
CREATE INDEX idx_att_date ON attendance(date);
CREATE INDEX idx_att_status ON attendance(attendance_status);
CREATE INDEX idx_payroll_emp ON payroll(employee_id, payment_date);
CREATE INDEX idx_proj_status ON project(status);
CREATE INDEX idx_leave_status ON `leave`(approval_status);
CREATE INDEX idx_review_rating ON performance_review(rating);
