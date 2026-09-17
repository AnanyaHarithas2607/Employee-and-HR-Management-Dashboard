-- =============================================================================
-- EMPLOYEE & HR MANAGEMENT SYSTEM
-- Graded Assignment Complex Analytical SQL Queries
-- Demonstrating: Multi-table JOINs, Aggregates, Window Functions, CTEs & Subqueries
-- =============================================================================

USE hr_management;

-- -----------------------------------------------------------------------------
-- Query 1: Department Budget Utilization vs Total Salary Expenditure
-- Demonstrates: LEFT JOIN, GROUP BY, Aggregations, Percentage Calculation
-- -----------------------------------------------------------------------------
SELECT 
    d.department_id,
    d.department_name,
    d.manager_name,
    d.budget AS total_allocated_budget,
    COUNT(e.employee_id) AS employee_count,
    COALESCE(SUM(e.salary), 0) AS total_annual_payroll,
    ROUND((COALESCE(SUM(e.salary), 0) / d.budget) * 100, 2) AS payroll_budget_consumption_pct
FROM department d
LEFT JOIN employee e ON d.department_id = e.department_id
GROUP BY d.department_id, d.department_name, d.manager_name, d.budget
ORDER BY payroll_budget_consumption_pct DESC;

-- -----------------------------------------------------------------------------
-- Query 2: Cross-Department Project Workload & Hours Logged (FD AF -> I, AF -> J)
-- Demonstrates: Multi-table JOIN, Aggregations, Filtered Grouping
-- -----------------------------------------------------------------------------
SELECT 
    p.project_id,
    p.project_name,
    p.status AS project_status,
    p.budget AS project_budget,
    COUNT(DISTINCT ep.employee_id) AS total_team_members,
    COALESCE(SUM(ep.hours_worked), 0) AS total_hours_logged,
    ROUND(COALESCE(AVG(ep.hours_worked), 0), 2) AS avg_hours_per_member
FROM project p
LEFT JOIN employee_project ep ON p.project_id = ep.project_id
GROUP BY p.project_id, p.project_name, p.status, p.budget
ORDER BY total_hours_logged DESC;

-- -----------------------------------------------------------------------------
-- Query 3: Top Performing Employees Ranked Within Each Department
-- Demonstrates: Window Function DENSE_RANK() OVER (PARTITION BY), CTE
-- -----------------------------------------------------------------------------
WITH RankedPerformers AS (
    SELECT 
        e.employee_id,
        CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
        d.department_name,
        e.job_title,
        pr.rating,
        pr.comments,
        DENSE_RANK() OVER (PARTITION BY e.department_id ORDER BY pr.rating DESC, e.salary DESC) AS dept_performance_rank
    FROM employee e
    JOIN department d ON e.department_id = d.department_id
    JOIN performance_review pr ON e.employee_id = pr.employee_id
)
SELECT * FROM RankedPerformers
WHERE dept_performance_rank <= 2
ORDER BY department_name, dept_performance_rank;

-- -----------------------------------------------------------------------------
-- Query 4: Training Program ROI & Average Assessment Score per Course
-- Demonstrates: Inner JOIN, Aggregate functions, HAVING clause
-- -----------------------------------------------------------------------------
SELECT 
    t.training_id,
    t.training_name,
    t.training_type,
    t.trainer_name,
    t.cost AS program_cost,
    COUNT(et.employee_id) AS total_enrolled,
    SUM(CASE WHEN et.completion_status = 'Completed' THEN 1 ELSE 0 END) AS completed_count,
    ROUND(AVG(et.score), 2) AS average_score,
    ROUND(t.cost / NULLIF(COUNT(et.employee_id), 0), 2) AS cost_per_trainee
FROM training t
JOIN employee_training et ON t.training_id = et.training_id
GROUP BY t.training_id, t.training_name, t.training_type, t.trainer_name, t.cost
ORDER BY average_score DESC;

-- -----------------------------------------------------------------------------
-- Query 5: Monthly Payroll Reconciliation & Net Remittance Audit
-- Demonstrates: Aggregations, Financial calculations, Verification check
-- -----------------------------------------------------------------------------
SELECT 
    p.payment_date,
    COUNT(p.payroll_id) AS total_disbursements,
    SUM(p.basic_salary) AS total_basic_salary,
    SUM(p.allowances) AS total_allowances_paid,
    SUM(p.deductions) AS total_deductions_withheld,
    SUM(p.net_salary) AS total_net_remitted,
    ROUND(AVG(p.net_salary), 2) AS avg_net_payout
FROM payroll p
GROUP BY p.payment_date
ORDER BY p.payment_date DESC;

-- -----------------------------------------------------------------------------
-- Query 6: Employee 360-Degree Comprehensive Profile
-- Demonstrates: Multiple 1:M and M:N JOINs combined with GROUP_CONCAT
-- -----------------------------------------------------------------------------
SELECT 
    e.employee_id,
    CONCAT(e.first_name, ' ', e.last_name) AS full_name,
    e.job_title,
    d.department_name,
    hr.hr_name AS assigned_hr_manager,
    COALESCE(pr.rating, 0) AS latest_performance_rating,
    COALESCE(COUNT(DISTINCT ep.project_id), 0) AS active_projects_count,
    COALESCE(SUM(ep.hours_worked), 0) AS total_project_hours,
    COALESCE(COUNT(DISTINCT et.training_id), 0) AS trainings_attended
FROM employee e
JOIN department d ON e.department_id = d.department_id
JOIN hr_manager hr ON e.hr_id = hr.hr_id
LEFT JOIN performance_review pr ON e.employee_id = pr.employee_id
LEFT JOIN employee_project ep ON e.employee_id = ep.employee_id
LEFT JOIN employee_training et ON e.employee_id = et.employee_id
GROUP BY e.employee_id, full_name, e.job_title, d.department_name, hr.hr_name, pr.rating
ORDER BY e.employee_id ASC;

-- -----------------------------------------------------------------------------
-- Query 7: Daily Attendance Compliance & Punctuality Breakdown
-- Demonstrates: Conditional COUNT (CASE WHEN), Percentage metrics
-- -----------------------------------------------------------------------------
SELECT 
    a.date,
    COUNT(a.attendance_id) AS total_logs,
    SUM(CASE WHEN a.attendance_status = 'Present' THEN 1 ELSE 0 END) AS physical_present,
    SUM(CASE WHEN a.attendance_status = 'Remote' THEN 1 ELSE 0 END) AS remote_present,
    SUM(CASE WHEN a.attendance_status = 'Half-Day' THEN 1 ELSE 0 END) AS half_day,
    SUM(CASE WHEN a.attendance_status = 'On-Leave' THEN 1 ELSE 0 END) AS on_leave,
    SUM(CASE WHEN a.attendance_status = 'Absent' THEN 1 ELSE 0 END) AS unexcused_absent,
    ROUND(AVG(a.work_hours), 2) AS avg_hours_logged
FROM attendance a
GROUP BY a.date
ORDER BY a.date DESC;

-- -----------------------------------------------------------------------------
-- Query 8: Leave Distribution by Type & Approval Velocity
-- Demonstrates: Status grouping, aggregation across leave requests
-- -----------------------------------------------------------------------------
SELECT 
    l.leave_type,
    COUNT(l.leave_id) AS total_requests,
    SUM(CASE WHEN l.approval_status = 'Approved' THEN 1 ELSE 0 END) AS approved_count,
    SUM(CASE WHEN l.approval_status = 'Pending' THEN 1 ELSE 0 END) AS pending_count,
    SUM(CASE WHEN l.approval_status = 'Rejected' THEN 1 ELSE 0 END) AS rejected_count,
    ROUND(SUM(CASE WHEN l.approval_status = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(l.leave_id), 1) AS approval_rate_pct
FROM `leave` l
GROUP BY l.leave_type
ORDER BY total_requests DESC;

-- -----------------------------------------------------------------------------
-- Query 9: Recruitment Conversion Funnel & HR Recruiter Performance
-- Demonstrates: Multi-entity JOIN, Status aggregation, Offer Conversion %
-- -----------------------------------------------------------------------------
SELECT 
    hr.hr_name AS recruiter,
    hr.designation,
    COUNT(r.recruitment_id) AS candidates_screened,
    SUM(CASE WHEN r.interview_status = 'Completed' THEN 1 ELSE 0 END) AS interviews_completed,
    SUM(CASE WHEN r.offer_status = 'Accepted' THEN 1 ELSE 0 END) AS offers_accepted,
    SUM(CASE WHEN r.offer_status = 'Pending' THEN 1 ELSE 0 END) AS offers_pending,
    ROUND(SUM(CASE WHEN r.offer_status = 'Accepted' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(r.recruitment_id), 0), 1) AS conversion_rate_pct
FROM hr_manager hr
LEFT JOIN recruitment r ON hr.hr_id = r.hr_id
GROUP BY hr.hr_id, hr.hr_name, hr.designation
ORDER BY candidates_screened DESC;

-- -----------------------------------------------------------------------------
-- Query 10: Salary Equity & Inter-Departmental Wage Comparison
-- Demonstrates: Statistical aggregates (MIN, MAX, AVG), Salary Variance
-- -----------------------------------------------------------------------------
SELECT 
    d.department_name,
    COUNT(e.employee_id) AS headcount,
    MIN(e.salary) AS min_salary,
    ROUND(AVG(e.salary), 2) AS avg_salary,
    MAX(e.salary) AS max_salary,
    ROUND(MAX(e.salary) - MIN(e.salary), 2) AS salary_spread,
    ROUND(AVG(e.salary) - (SELECT AVG(salary) FROM employee), 2) AS variance_from_company_avg
FROM department d
JOIN employee e ON d.department_id = e.department_id
GROUP BY d.department_id, d.department_name
ORDER BY avg_salary DESC;
