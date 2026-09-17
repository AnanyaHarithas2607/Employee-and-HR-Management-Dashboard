"""
Data access queries and business logic helpers for the 12 normalized tables.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
from database.connection import run_query, execute_action


def get_executive_kpis() -> Dict[str, Any]:
    """Calculates top-level KPI metrics across the organization."""
    try:
        emp_df = run_query("SELECT COUNT(*) AS total_employees, AVG(salary) AS avg_salary, SUM(salary) AS total_payroll FROM employee")
        proj_df = run_query("SELECT COUNT(*) AS total_projects, SUM(CASE WHEN status='Ongoing' THEN 1 ELSE 0 END) AS active_projects, SUM(budget) AS total_budget FROM project")
        dept_df = run_query("SELECT COUNT(*) AS total_depts, SUM(budget) AS total_dept_budget FROM department")
        review_df = run_query("SELECT AVG(rating) AS avg_rating FROM performance_review")
        att_df = run_query("""
            SELECT 
                ROUND(SUM(CASE WHEN attendance_status IN ('Present', 'Remote') THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 1) AS attendance_rate
            FROM attendance
        """)

        return {
            "total_employees": int(emp_df["total_employees"].iloc[0] if not emp_df.empty else 0),
            "avg_salary": float(emp_df["avg_salary"].iloc[0] if not emp_df.empty and pd.notna(emp_df["avg_salary"].iloc[0]) else 0),
            "total_payroll": float(emp_df["total_payroll"].iloc[0] if not emp_df.empty and pd.notna(emp_df["total_payroll"].iloc[0]) else 0),
            "active_projects": int(proj_df["active_projects"].iloc[0] if not proj_df.empty and pd.notna(proj_df["active_projects"].iloc[0]) else 0),
            "total_projects": int(proj_df["total_projects"].iloc[0] if not proj_df.empty else 0),
            "total_dept_budget": float(dept_df["total_dept_budget"].iloc[0] if not dept_df.empty and pd.notna(dept_df["total_dept_budget"].iloc[0]) else 0),
            "avg_rating": float(review_df["avg_rating"].iloc[0] if not review_df.empty and pd.notna(review_df["avg_rating"].iloc[0]) else 0),
            "attendance_rate": float(att_df["attendance_rate"].iloc[0] if not att_df.empty and pd.notna(att_df["attendance_rate"].iloc[0]) else 0)
        }
    except Exception as e:
        return {"error": str(e)}


def get_employees(department_id: Optional[int] = None, search_term: Optional[str] = None) -> pd.DataFrame:
    """Fetches employee directory with department and HR details."""
    query = """
        SELECT 
            e.employee_id,
            CONCAT(e.first_name, ' ', e.last_name) AS full_name,
            e.first_name,
            e.last_name,
            e.email,
            e.phone_number,
            e.gender,
            e.date_of_birth,
            e.hire_date,
            e.job_title,
            e.salary,
            d.department_name,
            d.department_id,
            hr.hr_name AS hr_manager,
            e.address
        FROM employee e
        JOIN department d ON e.department_id = d.department_id
        JOIN hr_manager hr ON e.hr_id = hr.hr_id
        WHERE 1=1
    """
    params = []
    if department_id:
        query += " AND e.department_id = %s"
        params.append(department_id)
    if search_term:
        query += " AND (e.first_name LIKE %s OR e.last_name LIKE %s OR e.job_title LIKE %s OR e.email LIKE %s)"
        pattern = f"%{search_term}%"
        params.extend([pattern, pattern, pattern, pattern])

    query += " ORDER BY e.employee_id ASC"
    return run_query(query)


def add_employee(first_name: str, last_name: str, gender: str, dob: str, email: str, 
                 phone: str, address: str, hire_date: str, salary: float, 
                 job_title: str, department_id: int, hr_id: int):
    """Inserts a new employee record."""
    query = """
        INSERT INTO employee (first_name, last_name, gender, date_of_birth, email, 
                             phone_number, address, hire_date, salary, job_title, department_id, hr_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    return execute_action(query, (first_name, last_name, gender, dob, email, phone, address, hire_date, salary, job_title, department_id, hr_id))


def get_departments() -> pd.DataFrame:
    """Retrieves all departments along with current headcounts and payroll spend."""
    query = """
        SELECT 
            d.department_id,
            d.department_name,
            d.location,
            d.budget,
            d.manager_name,
            COUNT(e.employee_id) AS employee_count,
            COALESCE(SUM(e.salary), 0) AS total_payroll,
            ROUND((COALESCE(SUM(e.salary), 0) / NULLIF(d.budget, 0)) * 100, 1) AS budget_utilized_pct
        FROM department d
        LEFT JOIN employee e ON d.department_id = e.department_id
        GROUP BY d.department_id, d.department_name, d.location, d.budget, d.manager_name
        ORDER BY d.department_id ASC
    """
    return run_query(query)


def get_projects() -> pd.DataFrame:
    """Fetches projects with owning departments and assigned member counts."""
    query = """
        SELECT 
            p.project_id,
            p.project_name,
            p.client_name,
            p.budget,
            p.status,
            p.start_date,
            p.end_date,
            d.department_name,
            COUNT(ep.employee_id) AS team_size,
            COALESCE(SUM(ep.hours_worked), 0) AS total_hours_worked
        FROM project p
        JOIN department d ON p.department_id = d.department_id
        LEFT JOIN employee_project ep ON p.project_id = ep.project_id
        GROUP BY p.project_id, p.project_name, p.client_name, p.budget, p.status, p.start_date, p.end_date, d.department_name
        ORDER BY p.project_id ASC
    """
    return run_query(query)


def get_project_assignments(project_id: Optional[int] = None) -> pd.DataFrame:
    """Fetches employee project assignments with role and hours (FD AF -> I, AF -> J)."""
    query = """
        SELECT 
            ep.project_id,
            p.project_name,
            ep.employee_id,
            CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
            e.job_title,
            ep.employee_role,
            ep.hours_worked,
            ep.assigned_date
        FROM employee_project ep
        JOIN project p ON ep.project_id = p.project_id
        JOIN employee e ON ep.employee_id = e.employee_id
    """
    if project_id:
        query += f" WHERE ep.project_id = {project_id}"
    query += " ORDER BY ep.project_id, ep.hours_worked DESC"
    return run_query(query)


def assign_employee_to_project(employee_id: int, project_id: int, assigned_date: str, role: str, hours: float):
    """Creates an assignment in employee_project bridge table."""
    query = """
        INSERT INTO employee_project (employee_id, project_id, assigned_date, employee_role, hours_worked)
        VALUES (%s, %s, %s, %s, %s)
    """
    return execute_action(query, (employee_id, project_id, assigned_date, role, hours))


def get_attendance_records(filter_date: Optional[str] = None) -> pd.DataFrame:
    """Retrieves attendance records with employee names."""
    query = """
        SELECT 
            a.attendance_id,
            a.date,
            a.employee_id,
            CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
            d.department_name,
            a.check_in_time,
            a.check_out_time,
            a.work_hours,
            a.attendance_status
        FROM attendance a
        JOIN employee e ON a.employee_id = e.employee_id
        JOIN department d ON e.department_id = d.department_id
    """
    if filter_date:
        query += f" WHERE a.date = '{filter_date}'"
    query += " ORDER BY a.date DESC, a.attendance_id DESC"
    return run_query(query)


def log_attendance(employee_id: int, date_val: str, check_in: str, check_out: str, hours: float, status: str):
    """Inserts a daily attendance log."""
    query = """
        INSERT INTO attendance (employee_id, date, check_in_time, check_out_time, work_hours, attendance_status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    return execute_action(query, (employee_id, date_val, check_in, check_out, hours, status))


def get_leave_requests(status_filter: Optional[str] = None) -> pd.DataFrame:
    """Retrieves leave requests."""
    query = """
        SELECT 
            l.leave_id,
            l.employee_id,
            CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
            d.department_name,
            l.leave_type,
            l.start_date,
            l.end_date,
            l.reason,
            l.approval_status
        FROM `leave` l
        JOIN employee e ON l.employee_id = e.employee_id
        JOIN department d ON e.department_id = d.department_id
    """
    if status_filter and status_filter != "All":
        query += f" WHERE l.approval_status = '{status_filter}'"
    query += " ORDER BY l.leave_id DESC"
    return run_query(query)


def update_leave_status(leave_id: int, new_status: str):
    """Updates approval status of a leave request."""
    query = "UPDATE `leave` SET approval_status = %s WHERE leave_id = %s"
    return execute_action(query, (new_status, leave_id))


def get_payroll_records() -> pd.DataFrame:
    """Retrieves payroll history with employee details."""
    query = """
        SELECT 
            p.payroll_id,
            p.payment_date,
            p.employee_id,
            CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
            d.department_name,
            p.basic_salary,
            p.allowances,
            p.deductions,
            p.net_salary
        FROM payroll p
        JOIN employee e ON p.employee_id = e.employee_id
        JOIN department d ON e.department_id = d.department_id
        ORDER BY p.payment_date DESC, p.payroll_id ASC
    """
    return run_query(query)


def get_performance_reviews() -> pd.DataFrame:
    """Retrieves all employee performance evaluations."""
    query = """
        SELECT 
            pr.review_id,
            pr.review_date,
            pr.employee_id,
            CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
            e.job_title,
            d.department_name,
            pr.reviewer_name,
            pr.rating,
            pr.comments
        FROM performance_review pr
        JOIN employee e ON pr.employee_id = e.employee_id
        JOIN department d ON e.department_id = d.department_id
        ORDER BY pr.rating DESC, pr.review_date DESC
    """
    return run_query(query)


def add_performance_review(employee_id: int, reviewer: str, date_val: str, rating: int, comments: str):
    """Inserts a performance review."""
    query = """
        INSERT INTO performance_review (employee_id, reviewer_name, review_date, rating, comments)
        VALUES (%s, %s, %s, %s, %s)
    """
    return execute_action(query, (employee_id, reviewer, date_val, rating, comments))


def get_trainings() -> pd.DataFrame:
    """Retrieves training catalog with enrollment metrics."""
    query = """
        SELECT 
            t.training_id,
            t.training_name,
            t.trainer_name,
            t.training_type,
            t.cost,
            t.start_date,
            t.end_date,
            COUNT(et.employee_id) AS enrolled_count,
            ROUND(AVG(et.score), 1) AS avg_assessment_score
        FROM training t
        LEFT JOIN employee_training et ON t.training_id = et.training_id
        GROUP BY t.training_id, t.training_name, t.trainer_name, t.training_type, t.cost, t.start_date, t.end_date
        ORDER BY t.training_id ASC
    """
    return run_query(query)


def get_training_enrollments(training_id: Optional[int] = None) -> pd.DataFrame:
    """Retrieves employee enrollments in training."""
    query = """
        SELECT 
            et.training_id,
            t.training_name,
            et.employee_id,
            CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
            et.completion_status,
            et.score
        FROM employee_training et
        JOIN training t ON et.training_id = t.training_id
        JOIN employee e ON et.employee_id = e.employee_id
    """
    if training_id:
        query += f" WHERE et.training_id = {training_id}"
    query += " ORDER BY et.score DESC"
    return run_query(query)


def get_recruitment_candidates() -> pd.DataFrame:
    """Retrieves candidates in recruitment pipeline."""
    query = """
        SELECT 
            r.recruitment_id,
            r.candidate_name,
            r.position_applied,
            r.interview_date,
            r.interview_status,
            r.offer_status,
            hr.hr_name AS coordinator
        FROM recruitment r
        JOIN hr_manager hr ON r.hr_id = hr.hr_id
        ORDER BY r.interview_date DESC
    """
    return run_query(query)


def get_hr_managers() -> pd.DataFrame:
    """Retrieves HR personnel."""
    query = """
        SELECT 
            hr.hr_id,
            hr.hr_name,
            hr.email,
            hr.phone_number,
            hr.designation,
            hr.experience_years,
            COUNT(e.employee_id) AS managed_employees
        FROM hr_manager hr
        LEFT JOIN employee e ON hr.hr_id = e.hr_id
        GROUP BY hr.hr_id, hr.hr_name, hr.email, hr.phone_number, hr.designation, hr.experience_years
        ORDER BY hr.hr_id ASC
    """
    return run_query(query)


COMPLEX_QUERIES_CATALOG = {
    "1. Department Budget vs Salary Spend": {
        "description": "Calculates total departmental budget, employee headcount, annual payroll cost, and budget utilization percentage.",
        "sql": """SELECT 
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
ORDER BY payroll_budget_consumption_pct DESC;"""
    },
    "2. Project Staffing & Hours Logged (FD AF -> I, AF -> J)": {
        "description": "Aggregates project team size, total logged hours, and average hours per contributor across all enterprise projects.",
        "sql": """SELECT 
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
ORDER BY total_hours_logged DESC;"""
    },
    "3. Top Performers Ranked by Department (Window Function)": {
        "description": "Utilizes DENSE_RANK() OVER (PARTITION BY department) to discover the highest-rated talent in every department.",
        "sql": """WITH RankedPerformers AS (
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
ORDER BY department_name, dept_performance_rank;"""
    },
    "4. Training Course ROI & Completion Analysis": {
        "description": "Computes completion statistics, average assessment score, and cost per trainee across professional development courses.",
        "sql": """SELECT 
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
ORDER BY average_score DESC;"""
    },
    "5. Monthly Payroll Disbursements & Deductions Audit": {
        "description": "Financial audit calculating aggregate basic salaries, company-paid allowances, withheld deductions, and net payouts.",
        "sql": """SELECT 
    p.payment_date,
    COUNT(p.payroll_id) AS total_disbursements,
    SUM(p.basic_salary) AS total_basic_salary,
    SUM(p.allowances) AS total_allowances_paid,
    SUM(p.deductions) AS total_deductions_withheld,
    SUM(p.net_salary) AS total_net_remitted,
    ROUND(AVG(p.net_salary), 2) AS avg_net_payout
FROM payroll p
GROUP BY p.payment_date
ORDER BY p.payment_date DESC;"""
    },
    "6. Employee 360-Degree Comprehensive View": {
        "description": "Comprehensive multi-entity join consolidating demographics, department, manager, rating, active projects, and training.",
        "sql": """SELECT 
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
ORDER BY e.employee_id ASC;"""
    },
    "7. Attendance Compliance & Work-from-Home Ratio": {
        "description": "Daily breakdown of physical on-site presence vs remote work, half-days, leaves, and unexcused absences.",
        "sql": """SELECT 
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
ORDER BY a.date DESC;"""
    },
    "8. Leave Application Approval Velocity": {
        "description": "Analyzes employee leave requests by category (Annual, Sick, Casual) and computes management approval rates.",
        "sql": """SELECT 
    l.leave_type,
    COUNT(l.leave_id) AS total_requests,
    SUM(CASE WHEN l.approval_status = 'Approved' THEN 1 ELSE 0 END) AS approved_count,
    SUM(CASE WHEN l.approval_status = 'Pending' THEN 1 ELSE 0 END) AS pending_count,
    SUM(CASE WHEN l.approval_status = 'Rejected' THEN 1 ELSE 0 END) AS rejected_count,
    ROUND(SUM(CASE WHEN l.approval_status = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(l.leave_id), 1) AS approval_rate_pct
FROM `leave` l
GROUP BY l.leave_type
ORDER BY total_requests DESC;"""
    },
    "9. Recruitment Conversion Funnel": {
        "description": "Measures candidate throughput from interview to offer acceptance per recruiter.",
        "sql": """SELECT 
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
ORDER BY candidates_screened DESC;"""
    },
    "10. Salary Spread & Departmental Variance": {
        "description": "Calculates salary minimum, maximum, and average per department, comparing each against the global organization average.",
        "sql": """SELECT 
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
ORDER BY avg_salary DESC;"""
    }
}
