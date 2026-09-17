-- =============================================================================
-- EMPLOYEE & HR MANAGEMENT SYSTEM
-- Seed Dataset (Realistic enterprise sample data across all 12 entities)
-- =============================================================================

USE hr_management;

-- -----------------------------------------------------------------------------
-- 1. Insert HR Managers
-- -----------------------------------------------------------------------------
INSERT INTO hr_manager (hr_id, hr_name, email, phone_number, designation, experience_years) VALUES
(1, 'Sarah Jenkins', 'sarah.jenkins@company.com', '+1-555-0101', 'Chief People Officer', 14),
(2, 'Michael Chang', 'michael.chang@company.com', '+1-555-0102', 'Senior HR Business Partner', 9),
(3, 'Priya Patel', 'priya.patel@company.com', '+1-555-0103', 'Talent Acquisition Director', 11),
(4, 'Carlos Rodriguez', 'carlos.rodriguez@company.com', '+1-555-0104', 'Employee Relations Lead', 7),
(5, 'Amanda Wright', 'amanda.wright@company.com', '+1-555-0105', 'Compensation & Benefits Specialist', 6);

-- -----------------------------------------------------------------------------
-- 2. Insert Departments
-- -----------------------------------------------------------------------------
INSERT INTO department (department_id, department_name, location, budget, manager_name) VALUES
(1, 'Engineering', 'Building A, Floor 4', 850000.00, 'Dr. Robert Vance'),
(2, 'Data Science & AI', 'Building A, Floor 5', 650000.00, 'Dr. Elena Rostova'),
(3, 'Product & Design', 'Building B, Floor 2', 450000.00, 'Marcus Sterling'),
(4, 'Human Resources', 'Building C, Floor 1', 320000.00, 'Sarah Jenkins'),
(5, 'Marketing & Sales', 'Building B, Floor 3', 520000.00, 'David Kim');

-- -----------------------------------------------------------------------------
-- 3. Insert Employees
-- -----------------------------------------------------------------------------
INSERT INTO employee (employee_id, first_name, last_name, gender, date_of_birth, email, phone_number, address, hire_date, salary, job_title, department_id, hr_id) VALUES
(101, 'Alex', 'Turner', 'Male', '1988-04-12', 'alex.turner@company.com', '+1-555-1001', '742 Evergreen Terrace, Springfield', '2019-03-15', 135000.00, 'Principal Software Architect', 1, 1),
(102, 'Emily', 'Chen', 'Female', '1992-09-24', 'emily.chen@company.com', '+1-555-1002', '124 Conch Street, Pacific Bay', '2020-07-01', 115000.00, 'Senior Backend Engineer', 1, 2),
(103, 'James', 'Wilson', 'Male', '1995-11-03', 'james.wilson@company.com', '+1-555-1003', '456 Elm Street, Metropolis', '2022-01-10', 88000.00, 'Full Stack Developer', 1, 2),
(104, 'Ananya', 'Sharma', 'Female', '1994-06-18', 'ananya.sharma@company.com', '+1-555-1004', '89 Victoria Gardens, Boston', '2021-04-15', 128000.00, 'Lead AI Research Scientist', 2, 3),
(105, 'David', 'O''Connor', 'Male', '1991-01-30', 'david.oconnor@company.com', '+1-555-1005', '321 Maple Avenue, Seattle', '2020-11-15', 105000.00, 'Machine Learning Engineer', 2, 3),
(106, 'Sophia', 'Martinez', 'Female', '1996-08-14', 'sophia.martinez@company.com', '+1-555-1006', '654 Pine Crescent, San Jose', '2022-06-01', 82000.00, 'Data Analyst', 2, 3),
(107, 'Liam', 'Taylor', 'Male', '1990-12-05', 'liam.taylor@company.com', '+1-555-1007', '987 Cedar Road, Austin', '2018-09-01', 120000.00, 'Lead Product Manager', 3, 1),
(108, 'Olivia', 'Brown', 'Female', '1993-03-22', 'olivia.brown@company.com', '+1-555-1008', '210 Oak Boulevard, Denver', '2021-08-15', 95000.00, 'Senior UI/UX Designer', 3, 4),
(109, 'Noah', 'Davis', 'Male', '1997-05-19', 'noah.davis@company.com', '+1-555-1009', '345 Birch Way, Chicago', '2023-02-01', 72000.00, 'Product Analyst', 3, 4),
(110, 'Grace', 'Hopper', 'Female', '1989-10-10', 'grace.hopper@company.com', '+1-555-1010', '101 Cyber Lane, New York', '2017-05-20', 142000.00, 'DevOps & Cloud Director', 1, 1),
(111, 'Ethan', 'Hunt', 'Male', '1994-07-04', 'ethan.hunt@company.com', '+1-555-1011', '789 Mission Street, San Francisco', '2021-10-01', 98000.00, 'Cybersecurity Engineer', 1, 2),
(112, 'Chloe', 'Bennett', 'Female', '1995-02-28', 'chloe.bennett@company.com', '+1-555-1012', '432 Sunset Blvd, Los Angeles', '2022-03-15', 78000.00, 'Talent Acquisition Associate', 4, 3),
(113, 'Lucas', 'Muller', 'Male', '1992-12-14', 'lucas.muller@company.com', '+1-555-1013', '567 River Road, Portland', '2020-04-10', 85000.00, 'HR Operations Specialist', 4, 4),
(114, 'Mia', 'Kawasaki', 'Female', '1993-05-08', 'mia.kawasaki@company.com', '+1-555-1014', '876 Blossom Court, Seattle', '2021-09-01', 110000.00, 'Enterprise Account Executive', 5, 5),
(115, 'Daniel', 'Evans', 'Male', '1996-01-25', 'daniel.evans@company.com', '+1-555-1015', '234 Market Square, Atlanta', '2022-11-01', 75000.00, 'Digital Marketing Strategist', 5, 5);

-- -----------------------------------------------------------------------------
-- 4. Insert Projects
-- -----------------------------------------------------------------------------
INSERT INTO project (project_id, project_name, start_date, end_date, budget, client_name, status, department_id) VALUES
(201, 'NextGen Cloud ERP Migration', '2024-01-15', '2024-11-30', 250000.00, 'Apex Global Logistics', 'Ongoing', 1),
(202, 'AI Customer Insights Engine', '2024-03-01', '2024-10-15', 180000.00, 'FinTech International', 'Ongoing', 2),
(203, 'Global Mobile Banking App 3.0', '2023-06-01', '2024-02-28', 210000.00, 'Metro Trust Bank', 'Completed', 3),
(204, 'Zero-Trust Infrastructure Hardening', '2024-02-01', '2024-08-31', 140000.00, 'Internal Security Ops', 'Ongoing', 1),
(205, 'Omni-Channel Lead Conversion Portal', '2024-04-10', '2024-12-20', 125000.00, 'Horizon Retailers', 'Planning', 5),
(206, 'Automated People Operations Platform', '2023-09-01', '2024-03-31', 95000.00, 'Internal HR Operations', 'Completed', 4);

-- -----------------------------------------------------------------------------
-- 5. Insert Employee-Project Assignments (M:N Bridge)
-- Satisfies Functional Dependencies: AF -> I (Role), AF -> J (Hours_Worked)
-- -----------------------------------------------------------------------------
INSERT INTO employee_project (employee_id, project_id, assigned_date, employee_role, hours_worked) VALUES
(101, 201, '2024-01-15', 'Lead Cloud Architect', 320.50),
(102, 201, '2024-01-20', 'Backend Integration Specialist', 280.00),
(103, 201, '2024-02-01', 'Frontend Developer', 210.00),
(110, 201, '2024-01-15', 'DevOps Infrastructure Lead', 150.00),
(104, 202, '2024-03-01', 'Chief AI Researcher', 290.00),
(105, 202, '2024-03-05', 'ML Pipeline Architect', 260.50),
(106, 202, '2024-03-10', 'Model Evaluation & ETL Lead', 220.00),
(107, 203, '2023-06-01', 'Principal Product Owner', 450.00),
(108, 203, '2023-06-15', 'Lead UX Researcher', 410.00),
(103, 203, '2023-07-01', 'Mobile UI Developer', 380.00),
(110, 204, '2024-02-01', 'Security Architect', 240.00),
(111, 204, '2024-02-01', 'Penetration Tester & Compliance Lead', 275.50),
(101, 204, '2024-02-15', 'Network Security Consultant', 95.00),
(107, 205, '2024-04-10', 'Product Strategy Lead', 80.00),
(109, 205, '2024-04-15', 'Product Analyst', 110.00),
(114, 205, '2024-04-10', 'Commercial Engagement Lead', 130.00),
(115, 205, '2024-04-20', 'Growth Campaign Specialist', 90.00),
(112, 206, '2023-09-01', 'HR Workflows Coordinator', 200.00),
(113, 206, '2023-09-01', 'Process Automation Analyst', 225.00),
(102, 206, '2023-10-01', 'Internal Tool Developer', 140.00);

-- -----------------------------------------------------------------------------
-- 6. Insert Attendance Records
-- -----------------------------------------------------------------------------
INSERT INTO attendance (attendance_id, employee_id, date, check_in_time, check_out_time, work_hours, attendance_status) VALUES
(1, 101, '2024-09-15', '08:55:00', '17:30:00', 8.58, 'Present'),
(2, 102, '2024-09-15', '09:02:00', '18:00:00', 8.96, 'Present'),
(3, 103, '2024-09-15', '09:15:00', '17:45:00', 8.50, 'Present'),
(4, 104, '2024-09-15', '08:45:00', '17:15:00', 8.50, 'Remote'),
(5, 105, '2024-09-15', '09:30:00', '18:30:00', 9.00, 'Present'),
(6, 106, '2024-09-15', '10:00:00', '14:00:00', 4.00, 'Half-Day'),
(7, 107, '2024-09-15', '09:00:00', '17:00:00', 8.00, 'Present'),
(8, 108, '2024-09-15', NULL, NULL, 0.00, 'On-Leave'),
(9, 109, '2024-09-15', '09:10:00', '17:40:00', 8.50, 'Present'),
(10, 110, '2024-09-15', '08:30:00', '17:00:00', 8.50, 'Remote'),
(11, 111, '2024-09-15', '09:00:00', '18:00:00', 9.00, 'Present'),
(12, 112, '2024-09-15', '09:05:00', '17:15:00', 8.16, 'Present'),
(13, 113, '2024-09-15', '08:50:00', '17:00:00', 8.16, 'Present'),
(14, 114, '2024-09-15', '09:15:00', '18:15:00', 9.00, 'Present'),
(15, 115, '2024-09-15', NULL, NULL, 0.00, 'Absent'),
-- Additional day for trend
(16, 101, '2024-09-16', '09:00:00', '17:30:00', 8.50, 'Present'),
(17, 102, '2024-09-16', '08:50:00', '17:50:00', 9.00, 'Present'),
(18, 104, '2024-09-16', '09:10:00', '18:00:00', 8.83, 'Remote'),
(19, 105, '2024-09-16', '09:15:00', '17:45:00', 8.50, 'Present'),
(20, 107, '2024-09-16', '09:00:00', '17:30:00', 8.50, 'Present');

-- -----------------------------------------------------------------------------
-- 7. Insert Leave Requests
-- -----------------------------------------------------------------------------
INSERT INTO `leave` (leave_id, employee_id, leave_type, start_date, end_date, reason, approval_status) VALUES
(1, 108, 'Annual', '2024-09-15', '2024-09-19', 'Scheduled family vacation', 'Approved'),
(2, 106, 'Sick', '2024-09-10', '2024-09-11', 'Severe seasonal flu', 'Approved'),
(3, 103, 'Casual', '2024-09-22', '2024-09-23', 'Personal house relocation', 'Pending'),
(4, 115, 'Casual', '2024-09-15', '2024-09-15', 'Emergency dentist visit', 'Pending'),
(5, 111, 'Annual', '2024-10-05', '2024-10-12', 'Autumn hiking trip', 'Pending'),
(6, 114, 'Sick', '2024-08-14', '2024-08-16', 'Recovery after outpatient surgery', 'Approved'),
(7, 102, 'Unpaid', '2024-07-01', '2024-07-05', 'Attending international conference', 'Rejected');

-- -----------------------------------------------------------------------------
-- 8. Insert Payroll Records
-- -----------------------------------------------------------------------------
INSERT INTO payroll (payroll_id, employee_id, basic_salary, allowances, deductions, net_salary, payment_date) VALUES
(1, 101, 11250.00, 1800.00, 2600.00, 10450.00, '2024-08-31'),
(2, 102, 9583.33, 1400.00, 2100.00, 8883.33, '2024-08-31'),
(3, 103, 7333.33, 1100.00, 1550.00, 6883.33, '2024-08-31'),
(4, 104, 10666.67, 1900.00, 2500.00, 10066.67, '2024-08-31'),
(5, 105, 8750.00, 1350.00, 1950.00, 8150.00, '2024-08-31'),
(6, 106, 6833.33, 950.00, 1400.00, 6383.33, '2024-08-31'),
(7, 107, 10000.00, 1600.00, 2300.00, 9300.00, '2024-08-31'),
(8, 108, 7916.67, 1200.00, 1750.00, 7366.67, '2024-08-31'),
(9, 109, 6000.00, 800.00, 1200.00, 5600.00, '2024-08-31'),
(10, 110, 11833.33, 2000.00, 2800.00, 11033.33, '2024-08-31'),
(11, 111, 8166.67, 1250.00, 1800.00, 7616.67, '2024-08-31'),
(12, 112, 6500.00, 850.00, 1300.00, 6050.00, '2024-08-31'),
(13, 113, 7083.33, 900.00, 1450.00, 6533.33, '2024-08-31'),
(14, 114, 9166.67, 2200.00, 2100.00, 9266.67, '2024-08-31'),
(15, 115, 6250.00, 1100.00, 1350.00, 6000.00, '2024-08-31');

-- -----------------------------------------------------------------------------
-- 9. Insert Performance Reviews
-- -----------------------------------------------------------------------------
INSERT INTO performance_review (review_id, employee_id, reviewer_name, review_date, rating, comments) VALUES
(1, 101, 'Dr. Robert Vance', '2024-06-30', 5, 'Consistently delivers state-of-the-art architectures. Outstanding mentorship of junior engineers.'),
(2, 102, 'Dr. Robert Vance', '2024-06-30', 4, 'Exceptional code reliability and API optimization during the ERP cloud migration.'),
(3, 103, 'Alex Turner', '2024-06-30', 4, 'Fast learner who rapidly mastered modern frontend state management protocols.'),
(4, 104, 'Dr. Elena Rostova', '2024-06-30', 5, 'Authored two breakthrough NLP algorithm optimizations directly powering client solutions.'),
(5, 105, 'Dr. Elena Rostova', '2024-06-30', 4, 'Strong execution across automated model evaluation pipelines and feature stores.'),
(6, 106, 'Ananya Sharma', '2024-06-30', 3, 'Solid delivery on data sanitization; encouraged to take higher ownership of statistical analysis.'),
(7, 107, 'Marcus Sterling', '2024-06-30', 5, 'Flawless product leadership for Mobile Banking 3.0, hitting target delivery ahead of schedule.'),
(8, 108, 'Marcus Sterling', '2024-06-30', 4, 'Superb visual craftsmanship and user-centric prototypes that received client accolades.'),
(9, 110, 'Dr. Robert Vance', '2024-06-30', 5, 'Maintained 99.99% cloud infrastructure uptime while driving down container costs by 22%.'),
(10, 111, 'Grace Hopper', '2024-06-30', 4, 'Proactively detected and remediated three zero-day vulnerabilities in staging environments.');

-- -----------------------------------------------------------------------------
-- 10. Insert Training Programs
-- -----------------------------------------------------------------------------
INSERT INTO training (training_id, training_name, trainer_name, start_date, end_date, training_type, cost) VALUES
(301, 'High-Performance MySQL Optimization & Indexing', 'Prof. Kenneth Cole', '2024-02-10', '2024-02-14', 'Technical', 2500.00),
(302, 'Large Language Models in Enterprise Production', 'Dr. Aris Thorne', '2024-04-05', '2024-04-09', 'Technical', 3800.00),
(303, 'Agile Leadership & Cross-Functional Delivery', 'Miriam Webster', '2024-05-12', '2024-05-14', 'Leadership', 1800.00),
(304, 'Zero-Trust Security & DevSecOps Mastery', 'Nathaniel Drake', '2024-06-18', '2024-06-21', 'Security', 2900.00),
(305, 'Modern Inclusive Hiring & Interview Ethics', 'Sarah Jenkins', '2024-07-02', '2024-07-03', 'Compliance', 950.00);

-- -----------------------------------------------------------------------------
-- 11. Insert Employee Training Enrollments (M:N Bridge)
-- -----------------------------------------------------------------------------
INSERT INTO employee_training (employee_id, training_id, completion_status, score) VALUES
(101, 301, 'Completed', 98.50),
(102, 301, 'Completed', 94.00),
(103, 301, 'Completed', 88.00),
(104, 302, 'Completed', 99.00),
(105, 302, 'Completed', 92.50),
(106, 302, 'In Progress', 82.00),
(107, 303, 'Completed', 96.00),
(108, 303, 'Completed', 91.00),
(110, 304, 'Completed', 97.00),
(111, 304, 'Completed', 95.00),
(112, 305, 'Completed', 93.00),
(113, 305, 'Completed', 90.50),
(109, 303, 'Enrolled', NULL),
(105, 301, 'Completed', 89.00);

-- -----------------------------------------------------------------------------
-- 12. Insert Recruitment Candidates
-- -----------------------------------------------------------------------------
INSERT INTO recruitment (recruitment_id, candidate_name, position_applied, interview_date, interview_status, offer_status, hr_id) VALUES
(401, 'Kavita Menon', 'Senior Backend Engineer', '2024-09-12', 'Completed', 'Accepted', 2),
(402, 'Julian Becker', 'AI Research Scientist', '2024-09-14', 'Completed', 'Pending', 3),
(403, 'Maya Lin', 'Product Designer', '2024-09-18', 'Scheduled', 'Pending', 4),
(404, 'Tariq Al-Mansoor', 'DevOps Specialist', '2024-09-19', 'Scheduled', 'Pending', 2),
(405, 'Rebecca Stone', 'Sales Account Manager', '2024-09-08', 'Completed', 'Rejected', 5),
(406, 'Lucas Silva', 'Data Engineer', '2024-09-10', 'Completed', 'Declined', 3);
