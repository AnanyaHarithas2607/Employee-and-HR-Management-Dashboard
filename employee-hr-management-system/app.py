"""
=============================================================================
EMPLOYEE & HR MANAGEMENT SYSTEM — INTERACTIVE DASHBOARD
Powered by MySQL 8.0+ / Dual Engine Architecture, Streamlit & Plotly
=============================================================================
"""

import datetime
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Database interface imports
from database.connection import (
    get_connection_status,
    try_connect_mysql,
    run_query,
    execute_action,
    DB_CONFIG
)
from database.queries import (
    get_executive_kpis,
    get_employees,
    add_employee,
    get_departments,
    get_projects,
    get_project_assignments,
    assign_employee_to_project,
    get_attendance_records,
    log_attendance,
    get_leave_requests,
    update_leave_status,
    get_payroll_records,
    get_performance_reviews,
    add_performance_review,
    get_trainings,
    get_training_enrollments,
    get_recruitment_candidates,
    get_hr_managers,
    COMPLEX_QUERIES_CATALOG
)

# Set page configuration
st.set_page_config(
    page_title="Employee & HR Management System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    /* Metric card enhancements */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        color: #f8fafc;
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #38bdf8;
        margin-top: 5px;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 4px;
    }
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 20px;
        color: #e2e8f0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    /* Status pills */
    .badge-active { background-color: #065f46; color: #34d399; padding: 3px 8px; border-radius: 9999px; font-size: 0.75rem; }
    .badge-pending { background-color: #854d0e; color: #fde047; padding: 3px 8px; border-radius: 9999px; font-size: 0.75rem; }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# SIDEBAR: Engine Status & Navigation
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/database.png", width=60)
    st.title("HR & Database Hub")
    st.caption("Graded Assignment — 3NF Normalization")

    st.markdown("---")
    # Connection status widget
    status = get_connection_status()
    if status["is_mysql"]:
        st.success(f"🟢 **{status['engine']}**\n\n`{status['details']}`")
    else:
        st.warning(f"🟡 **{status['engine']}**\n\n`{status['details']}`")

    # MySQL Configuration Expander
    with st.expander("⚙️ Configure MySQL Connection"):
        st.caption("Connect directly to your local or remote MySQL Server instance:")
        mysql_host = st.text_input("Host", value=DB_CONFIG["host"])
        mysql_port = st.number_input("Port", value=DB_CONFIG["port"], step=1)
        mysql_user = st.text_input("User", value=DB_CONFIG["user"])
        mysql_pass = st.text_input("Password", value=DB_CONFIG["password"], type="password")
        mysql_db = st.text_input("Database Name", value=DB_CONFIG["database"])

        if st.button("Connect & Initialize MySQL", use_container_width=True):
            test_cfg = {
                "host": mysql_host,
                "port": int(mysql_port),
                "user": mysql_user,
                "password": mysql_pass,
                "database": mysql_db
            }
            ok, msg = try_connect_mysql(test_cfg)
            if ok:
                st.success("Connected to MySQL successfully!")
                st.rerun()
            else:
                st.error(msg)

    st.markdown("---")
    menu = st.radio(
        "Navigation",
        [
            "📊 Executive Overview",
            "👥 Employee Directory & CRUD",
            "🏛️ Departments & Managers",
            "💼 Projects & Staffing (AF → I, J)",
            "⏱️ Attendance & Leave Portal",
            "💰 Payroll & Compensation",
            "🌟 Performance & Training",
            "🎯 Recruitment Funnel",
            "⚡ Interactive SQL Studio",
            "📜 3NF Normalization Theory"
        ]
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem; color:#64748b; text-align:center;'>"
        "Designed for Academic Submission & GitHub Showcase<br>"
        "Normalized Relational Architecture (3NF)"
        "</div>",
        unsafe_allow_html=True
    )


# -----------------------------------------------------------------------------
# 1. EXECUTIVE OVERVIEW
# -----------------------------------------------------------------------------
if menu == "📊 Executive Overview":
    st.markdown("<div class='section-header'>📊 Executive HR Dashboard & KPI Analytics</div>", unsafe_allow_html=True)
    
    kpis = get_executive_kpis()
    if "error" in kpis:
        st.error(f"Error loading KPIs: {kpis['error']}")
    else:
        # 4 Metric Cards
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric(label="Total Employees", value=kpis["total_employees"], delta="Headcount")
        with col2:
            st.metric(label="Annualized Payroll", value=f"${kpis['total_payroll']:,.0f}", delta="Annualized")
        with col3:
            st.metric(label="Active Projects", value=f"{kpis['active_projects']} / {kpis['total_projects']}", delta="Execution")
        with col4:
            st.metric(label="Attendance Compliance", value=f"{kpis['attendance_rate']}%", delta="Present/Remote")
        with col5:
            st.metric(label="Avg Performance", value=f"{kpis['avg_rating']:.2f} / 5.0", delta="Rating")

    st.markdown("---")

    # High-level charts
    ch_col1, ch_col2 = st.columns([3, 2])
    
    dept_df = get_departments()
    with ch_col1:
        st.subheader("Department Budget Allocation vs. Total Salary Spend")
        if not dept_df.empty:
            fig_budget = go.Figure()
            fig_budget.add_trace(go.Bar(
                x=dept_df["department_name"],
                y=dept_df["budget"],
                name="Allocated Budget ($)",
                marker_color="#38bdf8"
            ))
            fig_budget.add_trace(go.Bar(
                x=dept_df["department_name"],
                y=dept_df["total_payroll"],
                name="Annual Payroll Spend ($)",
                marker_color="#f43f5e"
            ))
            fig_budget.update_layout(
                barmode="group",
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_budget, use_container_width=True)

    with ch_col2:
        st.subheader("Workforce Distribution by Department")
        if not dept_df.empty:
            fig_pie = px.pie(
                dept_df,
                names="department_name",
                values="employee_count",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pie.update_layout(margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    # Quick Summary Tables
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.subheader("Active Projects Status")
        proj_df = get_projects()
        if not proj_df.empty:
            st.dataframe(
                proj_df[["project_name", "client_name", "status", "budget", "team_size"]],
                use_container_width=True,
                hide_index=True
            )
    with t_col2:
        st.subheader("Recent Leave Requests")
        leave_df = get_leave_requests()
        if not leave_df.empty:
            st.dataframe(
                leave_df[["employee_name", "leave_type", "start_date", "end_date", "approval_status"]].head(6),
                use_container_width=True,
                hide_index=True
            )


# -----------------------------------------------------------------------------
# 2. EMPLOYEE DIRECTORY & CRUD
# -----------------------------------------------------------------------------
elif menu == "👥 Employee Directory & CRUD":
    st.markdown("<div class='section-header'>👥 Employee Directory & Workforce Records</div>", unsafe_allow_html=True)
    
    # Filter controls
    f_col1, f_col2, f_col3 = st.columns([2, 2, 2])
    dept_df = get_departments()
    dept_options = {"All Departments": None}
    for _, row in dept_df.iterrows():
        dept_options[row["department_name"]] = row["department_id"]

    with f_col1:
        selected_dept_label = st.selectbox("Filter by Department", list(dept_options.keys()))
        selected_dept_id = dept_options[selected_dept_label]

    with f_col2:
        search_query = st.text_input("🔍 Search by Name, Title, or Email")

    emp_df = get_employees(department_id=selected_dept_id, search_term=search_query)

    with f_col3:
        st.metric(label="Filtered Records", value=len(emp_df))

    # Display Employee Data Table
    display_cols = ["employee_id", "full_name", "job_title", "department_name", "salary", "hire_date", "email", "phone_number", "hr_manager"]
    st.dataframe(
        emp_df[display_cols].rename(columns={
            "employee_id": "ID",
            "full_name": "Employee Name",
            "job_title": "Job Title",
            "department_name": "Department",
            "salary": "Salary ($)",
            "hire_date": "Hire Date",
            "email": "Email",
            "phone_number": "Phone",
            "hr_manager": "HR Partner"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # Add Employee Form
    with st.expander("➕ Register New Employee (INSERT Transaction)", expanded=False):
        st.markdown("##### Fill Employee Details (Enforces Foreign Keys on `DEPARTMENT` and `HR_MANAGER`)")
        hr_df = get_hr_managers()
        hr_options = {row["hr_name"]: row["hr_id"] for _, row in hr_df.iterrows()}

        with st.form("add_employee_form"):
            form_c1, form_c2, form_c3 = st.columns(3)
            with form_c1:
                first_name = st.text_input("First Name", placeholder="e.g. John")
                last_name = st.text_input("Last Name", placeholder="e.g. Doe")
                gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Other"])
                dob = st.date_input("Date of Birth", value=datetime.date(1995, 1, 1))

            with form_c2:
                email = st.text_input("Corporate Email", placeholder="e.g. john.doe@company.com")
                phone = st.text_input("Phone Number", placeholder="e.g. +1-555-0199")
                address = st.text_input("Residential Address", placeholder="e.g. 123 University Ave")
                hire_date = st.date_input("Hire Date", value=datetime.date.today())

            with form_c3:
                salary = st.number_input("Annual Salary ($)", min_value=10000.0, max_value=500000.0, value=85000.0, step=1000.0)
                job_title = st.text_input("Job Title", placeholder="e.g. Data Systems Engineer")
                dept_keys = [k for k in dept_options.keys() if k != "All Departments"]
                sel_dept = st.selectbox("Assigned Department", dept_keys)
                sel_hr = st.selectbox("Assigned HR Manager", list(hr_options.keys()))

            submitted = st.form_submit_button("Submit & Commit Employee Record", use_container_width=True)
            if submitted:
                if not first_name or not last_name or not email or not job_title:
                    st.error("Please provide all required fields (First Name, Last Name, Email, Job Title).")
                else:
                    success, msg = add_employee(
                        first_name=first_name,
                        last_name=last_name,
                        gender=gender,
                        dob=str(dob),
                        email=email,
                        phone=phone,
                        address=address,
                        hire_date=str(hire_date),
                        salary=float(salary),
                        job_title=job_title,
                        department_id=int(dept_options[sel_dept]),
                        hr_id=int(hr_options[sel_hr])
                    )
                    if success:
                        st.success(f"Employee {first_name} {last_name} registered successfully!")
                        st.rerun()
                    else:
                        st.error(msg)


# -----------------------------------------------------------------------------
# 3. DEPARTMENTS & MANAGERS
# -----------------------------------------------------------------------------
elif menu == "🏛️ Departments & Managers":
    st.markdown("<div class='section-header'>🏛️ Departmental Hierarchy & Managerial Oversight</div>", unsafe_allow_html=True)
    
    dept_df = get_departments()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Operational Units", len(dept_df))
    with col2:
        st.metric("Combined Budget", f"${dept_df['budget'].sum():,.2f}")
    with col3:
        st.metric("Combined Payroll Commitments", f"${dept_df['total_payroll'].sum():,.2f}")

    st.markdown("---")

    # Card overview of departments
    d_cols = st.columns(len(dept_df) if len(dept_df) <= 5 else 3)
    for i, (_, dept) in enumerate(dept_df.iterrows()):
        col_idx = i % (len(d_cols))
        with d_cols[col_idx]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{dept['department_name']}</div>
                <div class="metric-value">{dept['employee_count']} <span style='font-size:1rem;color:#94a3b8;'>staff</span></div>
                <div style='margin-top:10px; font-size:0.85rem; color:#cbd5e1;'>
                    <b>Manager:</b> {dept['manager_name']}<br>
                    <b>Location:</b> {dept['location']}<br>
                    <b>Budget:</b> ${dept['budget']:,.0f}<br>
                    <b>Payroll:</b> ${dept['total_payroll']:,.0f} ({dept['budget_utilized_pct']}%)
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("HR Leadership Team (`HR_MANAGER` Entity)")
    hr_df = get_hr_managers()
    st.dataframe(
        hr_df.rename(columns={
            "hr_id": "HR ID",
            "hr_name": "Full Name",
            "email": "Email",
            "phone_number": "Phone",
            "designation": "Designation",
            "experience_years": "Experience (Years)",
            "managed_employees": "Directly Managed Staff"
        }),
        use_container_width=True,
        hide_index=True
    )


# -----------------------------------------------------------------------------
# 4. PROJECTS & STAFFING (AF -> I, AF -> J)
# -----------------------------------------------------------------------------
elif menu == "💼 Projects & Staffing (AF → I, J)":
    st.markdown("<div class='section-header'>💼 Projects, Staffing & Work Allocations</div>", unsafe_allow_html=True)
    st.info("💡 **Assignment Theory Focus**: Implements Functional Dependencies **$AF \\to I$** (`Employee_Role`) and **$AF \\to J$** (`Hours_Worked`) through the composite bridge table `EMPLOYEE_PROJECT`.")

    proj_df = get_projects()
    st.dataframe(
        proj_df.rename(columns={
            "project_id": "Project ID",
            "project_name": "Project Name",
            "client_name": "Client",
            "budget": "Budget ($)",
            "status": "Status",
            "department_name": "Owning Dept",
            "team_size": "Staffed Members",
            "total_hours_worked": "Hours Logged"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")
    p_col1, p_col2 = st.columns([1, 2])

    proj_options = {row["project_name"]: row["project_id"] for _, row in proj_df.iterrows()}
    with p_col1:
        st.subheader("Filter Assignments")
        sel_proj_name = st.selectbox("Select Project to Inspect", list(proj_options.keys()))
        sel_proj_id = proj_options[sel_proj_name]

    with p_col2:
        assignments_df = get_project_assignments(project_id=sel_proj_id)
        st.subheader(f"Staff Assigned to: {sel_proj_name}")
        if assignments_df.empty:
            st.warning("No staff members assigned to this project yet.")
        else:
            st.dataframe(
                assignments_df[["employee_name", "job_title", "employee_role", "hours_worked", "assigned_date"]].rename(columns={
                    "employee_name": "Employee",
                    "job_title": "Primary Job Title",
                    "employee_role": "Assigned Project Role (I)",
                    "hours_worked": "Hours Logged (J)",
                    "assigned_date": "Assigned Date"
                }),
                use_container_width=True,
                hide_index=True
            )

    # Assign Employee to Project Form
    with st.expander("➕ Assign Employee to Project (M:N Bridge Record)", expanded=False):
        emp_all = get_employees()
        emp_options = {row["full_name"]: row["employee_id"] for _, row in emp_all.iterrows()}
        with st.form("assign_project_form"):
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                assign_emp_name = st.selectbox("Select Employee", list(emp_options.keys()))
            with c2:
                assign_proj_name = st.selectbox("Select Project", list(proj_options.keys()))
            with c3:
                assign_role = st.text_input("Project Role (I)", placeholder="e.g. Lead QA Specialist")
            with c4:
                assign_hours = st.number_input("Hours Worked (J)", min_value=0.0, max_value=2000.0, value=40.0, step=5.0)

            submitted = st.form_submit_button("Create Project Assignment", use_container_width=True)
            if submitted:
                if not assign_role:
                    st.error("Please specify the role for this assignment.")
                else:
                    success, msg = assign_employee_to_project(
                        employee_id=emp_options[assign_emp_name],
                        project_id=proj_options[assign_proj_name],
                        assigned_date=str(datetime.date.today()),
                        role=assign_role,
                        hours=float(assign_hours)
                    )
                    if success:
                        st.success("Assignment created successfully!")
                        st.rerun()
                    else:
                        st.error(msg)


# -----------------------------------------------------------------------------
# 5. ATTENDANCE & LEAVE PORTAL
# -----------------------------------------------------------------------------
elif menu == "⏱️ Attendance & Leave Portal":
    st.markdown("<div class='section-header'>⏱️ Time, Attendance & Leave Management</div>", unsafe_allow_html=True)
    
    tab_att, tab_leave = st.tabs(["📅 Daily Attendance Logs", "🏖️ Leave Requests & Manager Approval"])

    with tab_att:
        att_df = get_attendance_records()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Logs Recorded", len(att_df))
        with col2:
            present_cnt = len(att_df[att_df["attendance_status"].isin(["Present", "Remote"])])
            st.metric("Present / Remote", present_cnt)
        with col3:
            leave_cnt = len(att_df[att_df["attendance_status"] == "On-Leave"])
            st.metric("On-Leave", leave_cnt)
        with col4:
            absent_cnt = len(att_df[att_df["attendance_status"] == "Absent"])
            st.metric("Absent", absent_cnt)

        st.markdown("---")
        st.dataframe(
            att_df.rename(columns={
                "attendance_id": "Log ID",
                "date": "Date",
                "employee_name": "Employee",
                "department_name": "Department",
                "check_in_time": "Check-In",
                "check_out_time": "Check-Out",
                "work_hours": "Hours Worked",
                "attendance_status": "Status"
            }),
            use_container_width=True,
            hide_index=True
        )

        with st.expander("⏱️ Log Manual Attendance Check-in", expanded=False):
            emp_all = get_employees()
            emp_dict = {row["full_name"]: row["employee_id"] for _, row in emp_all.iterrows()}
            with st.form("log_att_form"):
                ac1, ac2, ac3, ac4 = st.columns(4)
                with ac1:
                    sel_emp = st.selectbox("Employee", list(emp_dict.keys()), key="att_emp")
                    log_date = st.date_input("Date", value=datetime.date.today(), key="att_date")
                with ac2:
                    in_time = st.text_input("Check-In Time", value="09:00:00")
                    out_time = st.text_input("Check-Out Time", value="17:30:00")
                with ac3:
                    w_hours = st.number_input("Work Hours", min_value=0.0, max_value=24.0, value=8.5, step=0.5)
                with ac4:
                    att_status = st.selectbox("Status", ["Present", "Remote", "Half-Day", "On-Leave", "Absent"])

                if st.form_submit_button("Record Attendance", use_container_width=True):
                    ok, msg = log_attendance(
                        employee_id=emp_dict[sel_emp],
                        date_val=str(log_date),
                        check_in=in_time if att_status not in ["Absent", "On-Leave"] else None,
                        check_out=out_time if att_status not in ["Absent", "On-Leave"] else None,
                        hours=w_hours,
                        status=att_status
                    )
                    if ok:
                        st.success("Attendance entry logged!")
                        st.rerun()
                    else:
                        st.error(msg)

    with tab_leave:
        st.subheader("Manage Time-off Requests")
        leave_df = get_leave_requests()
        
        # Action workflow for pending requests
        pending_leaves = leave_df[leave_df["approval_status"] == "Pending"]
        if not pending_leaves.empty:
            st.warning(f"⚠️ You have **{len(pending_leaves)}** pending leave request(s) awaiting managerial review:")
            for _, r in pending_leaves.iterrows():
                with st.container():
                    lcol1, lcol2, lcol3, lcol4 = st.columns([3, 2, 1, 1])
                    with lcol1:
                        st.markdown(f"**{r['employee_name']}** ({r['department_name']}) — *{r['leave_type']} Leave*")
                        st.caption(f"Reason: {r['reason']}")
                    with lcol2:
                        st.caption(f"Duration: {r['start_date']} to {r['end_date']}")
                    with lcol3:
                        if st.button("✅ Approve", key=f"app_{r['leave_id']}", use_container_width=True):
                            update_leave_status(r["leave_id"], "Approved")
                            st.success(f"Leave request #{r['leave_id']} approved!")
                            st.rerun()
                    with lcol4:
                        if st.button("❌ Reject", key=f"rej_{r['leave_id']}", use_container_width=True):
                            update_leave_status(r["leave_id"], "Rejected")
                            st.info(f"Leave request #{r['leave_id']} rejected.")
                            st.rerun()
                st.markdown("---")
        else:
            st.success("All leave requests have been reviewed and processed.")

        st.markdown("##### All Historical Leave Records")
        st.dataframe(
            leave_df.rename(columns={
                "leave_id": "Leave ID",
                "employee_name": "Employee Name",
                "department_name": "Department",
                "leave_type": "Leave Type",
                "start_date": "From",
                "end_date": "To",
                "reason": "Reason",
                "approval_status": "Approval Status"
            }),
            use_container_width=True,
            hide_index=True
        )


# -----------------------------------------------------------------------------
# 6. PAYROLL & COMPENSATION
# -----------------------------------------------------------------------------
elif menu == "💰 Payroll & Compensation":
    st.markdown("<div class='section-header'>💰 Payroll & Compensation Reconciliation</div>", unsafe_allow_html=True)
    
    payroll_df = get_payroll_records()
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Net Disbursed", f"${payroll_df['net_salary'].sum():,.2f}")
    with c2:
        st.metric("Basic Salaries", f"${payroll_df['basic_salary'].sum():,.2f}")
    with c3:
        st.metric("Company Allowances", f"${payroll_df['allowances'].sum():,.2f}")
    with c4:
        st.metric("Taxes / Deductions", f"${payroll_df['deductions'].sum():,.2f}")

    st.markdown("---")
    
    pcol1, pcol2 = st.columns([3, 2])
    with pcol1:
        st.subheader("Salary Distribution Across Workforce")
        emp_df = get_employees()
        fig_hist = px.histogram(
            emp_df,
            x="salary",
            nbins=10,
            color="department_name",
            marginal="box",
            labels={"salary": "Annual Salary ($)", "department_name": "Department"}
        )
        fig_hist.update_layout(margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_hist, use_container_width=True)

    with pcol2:
        st.subheader("Net Compensation by Department")
        dept_payroll = payroll_df.groupby("department_name")["net_salary"].sum().reset_index()
        fig_bar = px.bar(
            dept_payroll,
            x="department_name",
            y="net_salary",
            labels={"net_salary": "Net Salary Paid ($)", "department_name": "Department"},
            color="net_salary",
            color_continuous_scale="Viridis"
        )
        fig_bar.update_layout(margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    st.subheader("Monthly Disbursement Records (`PAYROLL` Entity)")
    st.dataframe(
        payroll_df.rename(columns={
            "payroll_id": "Payroll ID",
            "payment_date": "Payment Date",
            "employee_name": "Employee Name",
            "department_name": "Department",
            "basic_salary": "Basic ($)",
            "allowances": "Allowances ($)",
            "deductions": "Deductions ($)",
            "net_salary": "Net Salary ($)"
        }),
        use_container_width=True,
        hide_index=True
    )


# -----------------------------------------------------------------------------
# 7. PERFORMANCE & TRAINING
# -----------------------------------------------------------------------------
elif menu == "🌟 Performance & Training":
    st.markdown("<div class='section-header'>🌟 Performance Reviews & Professional Development</div>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["🏆 Performance Appraisals", "🎓 Corporate Training Catalog"])

    with t1:
        reviews_df = get_performance_reviews()
        col1, col2 = st.columns([2, 3])
        with col1:
            st.subheader("Rating Distribution (1 - 5 Stars)")
            fig_ratings = px.bar(
                reviews_df["rating"].value_counts().sort_index().reset_index(),
                x="rating",
                y="count",
                labels={"rating": "Rating (Stars)", "count": "Evaluations"},
                color="rating",
                color_continuous_scale="Blues"
            )
            st.plotly_chart(fig_ratings, use_container_width=True)
        with col2:
            st.subheader("Recent Managerial Reviews")
            st.dataframe(
                reviews_df[["employee_name", "job_title", "reviewer_name", "rating", "comments", "review_date"]].rename(columns={
                    "employee_name": "Employee",
                    "job_title": "Role",
                    "reviewer_name": "Reviewer",
                    "rating": "Score",
                    "comments": "Feedback",
                    "review_date": "Date"
                }),
                use_container_width=True,
                hide_index=True
            )

        with st.expander("➕ Submit New Performance Evaluation", expanded=False):
            emp_all = get_employees()
            emp_dict = {row["full_name"]: row["employee_id"] for _, row in emp_all.iterrows()}
            with st.form("new_review_form"):
                r1, r2, r3 = st.columns(3)
                with r1:
                    rev_emp = st.selectbox("Employee Being Evaluated", list(emp_dict.keys()))
                with r2:
                    reviewer = st.text_input("Reviewer Name", placeholder="e.g. Dr. Robert Vance")
                with r3:
                    rating = st.slider("Rating (1 = Unsatisfactory, 5 = Outstanding)", 1, 5, 4)
                comments = st.text_area("Manager Feedback and Objectives", placeholder="Key achievements and development goals...")

                if st.form_submit_button("Record Evaluation"):
                    ok, msg = add_performance_review(emp_dict[rev_emp], reviewer, str(datetime.date.today()), rating, comments)
                    if ok:
                        st.success("Performance evaluation saved successfully!")
                        st.rerun()
                    else:
                        st.error(msg)

    with t2:
        train_df = get_trainings()
        st.subheader("Corporate Training Programs")
        st.dataframe(
            train_df.rename(columns={
                "training_id": "ID",
                "training_name": "Course Title",
                "trainer_name": "Lead Trainer",
                "training_type": "Category",
                "cost": "Program Cost ($)",
                "enrolled_count": "Employees Enrolled",
                "avg_assessment_score": "Average Test Score"
            }),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")
        st.subheader("Employee Course Completion & Assessment Scores (Bridge: `EMPLOYEE_TRAINING`)")
        train_options = {row["training_name"]: row["training_id"] for _, row in train_df.iterrows()}
        selected_course = st.selectbox("Inspect Enrollments for Course", list(train_options.keys()))
        enroll_df = get_training_enrollments(training_id=train_options[selected_course])
        if enroll_df.empty:
            st.info("No enrollment records found for this training session.")
        else:
            st.dataframe(
                enroll_df[["employee_name", "completion_status", "score"]].rename(columns={
                    "employee_name": "Enrolled Employee",
                    "completion_status": "Status",
                    "score": "Final Assessment Score (/100)"
                }),
                use_container_width=True,
                hide_index=True
            )


# -----------------------------------------------------------------------------
# 8. RECRUITMENT PIPELINE
# -----------------------------------------------------------------------------
elif menu == "🎯 Recruitment Funnel":
    st.markdown("<div class='section-header'>🎯 Talent Acquisition & Candidate Pipeline</div>", unsafe_allow_html=True)
    
    rec_df = get_recruitment_candidates()
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Candidates Screened", len(rec_df))
    with c2:
        comp_int = len(rec_df[rec_df["interview_status"] == "Completed"])
        st.metric("Interviews Completed", comp_int)
    with c3:
        offers_acc = len(rec_df[rec_df["offer_status"] == "Accepted"])
        st.metric("Offers Accepted", offers_acc)
    with c4:
        conv_rate = (offers_acc / len(rec_df) * 100) if len(rec_df) > 0 else 0
        st.metric("Offer Conversion Rate", f"{conv_rate:.1f}%")

    st.markdown("---")
    st.subheader("Candidate Records (`RECRUITMENT` Entity)")
    st.dataframe(
        rec_df.rename(columns={
            "recruitment_id": "Applicant ID",
            "candidate_name": "Candidate Full Name",
            "position_applied": "Target Position",
            "interview_date": "Interview Date",
            "interview_status": "Interview State",
            "offer_status": "Offer Status",
            "coordinator": "Assigned HR Lead"
        }),
        use_container_width=True,
        hide_index=True
    )


# -----------------------------------------------------------------------------
# 9. INTERACTIVE SQL STUDIO
# -----------------------------------------------------------------------------
elif menu == "⚡ Interactive SQL Studio":
    st.markdown("<div class='section-header'>⚡ Interactive SQL Studio (Graded Assignment Console)</div>", unsafe_allow_html=True)
    st.info("Run pre-written complex queries demonstrating **JOINs, Subqueries, Window Functions (`DENSE_RANK`), and Aggregations**, or write custom SQL statements live against the database.")

    selected_query_title = st.selectbox("Select a Graded Assignment Query to Load:", list(COMPLEX_QUERIES_CATALOG.keys()))
    catalog_entry = COMPLEX_QUERIES_CATALOG[selected_query_title]

    st.markdown(f"**Query Objective**: {catalog_entry['description']}")
    
    # Pre-populate code area
    query_code = st.text_area("SQL Statement (Editable)", value=catalog_entry["sql"], height=240)

    col1, col2 = st.columns([1, 4])
    with col1:
        execute_btn = st.button("🚀 Execute SQL", use_container_width=True)

    if execute_btn:
        try:
            res_df = run_query(query_code)
            st.success(f"Execution Successful! Retrieved **{len(res_df)}** row(s).")
            st.dataframe(res_df, use_container_width=True)

            # Auto chart if numeric columns present
            num_cols = res_df.select_dtypes(include=["number"]).columns.tolist()
            text_cols = res_df.select_dtypes(include=["object", "string"]).columns.tolist()
            if len(num_cols) >= 1 and len(text_cols) >= 1 and len(res_df) <= 30:
                with st.expander("📊 Instant Visual Representation", expanded=True):
                    fig_auto = px.bar(
                        res_df,
                        x=text_cols[0],
                        y=num_cols[0],
                        title=f"{num_cols[0].replace('_', ' ').title()} by {text_cols[0].replace('_', ' ').title()}",
                        color=num_cols[0],
                        color_continuous_scale="Teal"
                    )
                    st.plotly_chart(fig_auto, use_container_width=True)
        except Exception as e:
            st.error(f"SQL Error: {str(e)}")


# -----------------------------------------------------------------------------
# 10. 3NF NORMALIZATION THEORY
# -----------------------------------------------------------------------------
elif menu == "📜 3NF Normalization Theory":
    st.markdown("<div class='section-header'>📜 Relational Normalization & Functional Dependency Proof</div>", unsafe_allow_html=True)
    
    st.markdown("""
    ### 1. Attribute Dictionary
    | Symbol | Attribute Name | Semantic Meaning |
    |---|---|---|
    | **$A$** | `Employee_ID` | Unique employee surrogate key |
    | **$B$** | `Department_ID` | Unique department surrogate key |
    | **$C$** | `Department_Name` | Human-readable department name |
    | **$D$** | `Manager_ID` | Manager identifier for department |
    | **$E$** | `Manager_Name` | Manager full name |
    | **$F$** | `Project_ID` | Project unique identifier |
    | **$G$** | `Project_Name` | Project title |
    | **$H$** | `Project_Budget` | Total capital allocated to project |
    | **$I$** | `Employee_Role` | Staff role on a specific project |
    | **$J$** | `Hours_Worked` | Cumulative hours logged on a project |
    """)

    st.markdown("---")
    st.markdown("""
    ### 2. Functional Dependency Set ($F$)
    From the assignment problem statement:
    1. **$A \\to B$**: Each employee belongs to exactly one department.
    2. **$B \\to C$**: Department ID uniquely identifies Department Name.
    3. **$B \\to D$**: Department ID uniquely identifies Manager ID.
    4. **$D \\to E$**: Manager ID uniquely identifies Manager Name.
    5. **$F \\to G$**: Project ID uniquely identifies Project Name.
    6. **$F \\to H$**: Project ID uniquely identifies Project Budget.
    7. **$AF \\to I$**: Employee and Project jointly identify the Employee Role on that project.
    8. **$AF \\to J$**: Employee and Project jointly identify the Hours Worked.
    9. **$A \\to D$**: Employee transitively identifies Department Manager ($A \\to B$ and $B \\to D$).
    10. **$AF \\to B$**: Employee-project assignment determines Department ($A \\to B$ via Augmentation).
    """)

    st.markdown("---")
    st.markdown(r"""
    ### 3. Normalization Progression

    #### 🟢 First Normal Form (1NF)
    - **Rule**: Atomic attributes, unique row identities, and no repeating groups or multivalued attributes.
    - **Implementation**: The $M:N$ relationships between `EMPLOYEE` and `PROJECT`, as well as `EMPLOYEE` and `TRAINING`, are decomposed into the dedicated associative relations `EMPLOYEE_PROJECT` and `EMPLOYEE_TRAINING`.

    #### 🟢 Second Normal Form (2NF)
    - **Rule**: Relation is in 1NF, and **no partial dependencies** exist on composite keys.
    - **Implementation**: In `EMPLOYEE_PROJECT(Employee_ID, Project_ID)`, the attributes `Employee_Role` ($I$) and `Hours_Worked` ($J$) depend on the **entire composite key** $\{A, F\}$. The project-specific attributes ($G$: `Project_Name`, $H$: `Project_Budget`) depend only on $F$, so they are cleanly isolated in the independent `PROJECT` entity.

    #### 🟢 Third Normal Form (3NF)
    - **Rule**: Relation is in 2NF, and **no transitive dependencies** exist ($X \\to Y$ where $X$ is not a superkey).
    - **Implementation**: In `EMPLOYEE`, having `Department_Name` ($C$) and `Manager_Name` ($E$) would violate 3NF because $A \\to B \\to C$ and $B \\to D \\to E$. These dependencies are decomposed into separate tables (`DEPARTMENT` and `HR_MANAGER`), leaving only foreign keys (`department_id`, `hr_id`) in `EMPLOYEE`.
    """)

    st.markdown("---")
    st.markdown("""
    ### 4. Relational Schema Summary (12 Normalized Entities)
    1. **`HR_MANAGER`** (`hr_id` [PK], `hr_name`, `email`, `phone_number`, `designation`, `experience_years`)
    2. **`DEPARTMENT`** (`department_id` [PK], `department_name`, `location`, `budget`, `manager_name`)
    3. **`EMPLOYEE`** (`employee_id` [PK], `first_name`, `last_name`, `gender`, `date_of_birth`, `email`, `phone_number`, `address`, `hire_date`, `salary`, `job_title`, `department_id` [FK], `hr_id` [FK])
    4. **`PROJECT`** (`project_id` [PK], `project_name`, `start_date`, `end_date`, `budget`, `client_name`, `status`, `department_id` [FK])
    5. **`EMPLOYEE_PROJECT`** (`employee_id` [PK, FK], `project_id` [PK, FK], `assigned_date`, `employee_role`, `hours_worked`)
    6. **`ATTENDANCE`** (`attendance_id` [PK], `employee_id` [FK], `date`, `check_in_time`, `check_out_time`, `work_hours`, `attendance_status`)
    7. **`LEAVE`** (`leave_id` [PK], `employee_id` [FK], `leave_type`, `start_date`, `end_date`, `reason`, `approval_status`)
    8. **`PAYROLL`** (`payroll_id` [PK], `employee_id` [FK], `basic_salary`, `allowances`, `deductions`, `net_salary`, `payment_date`)
    9. **`PERFORMANCE_REVIEW`** (`review_id` [PK], `employee_id` [FK], `reviewer_name`, `review_date`, `rating`, `comments`)
    10. **`TRAINING`** (`training_id` [PK], `training_name`, `trainer_name`, `start_date`, `end_date`, `training_type`, `cost`)
    11. **`EMPLOYEE_TRAINING`** (`employee_id` [PK, FK], `training_id` [PK, FK], `completion_status`, `score`)
    12. **`RECRUITMENT`** (`recruitment_id` [PK], `candidate_name`, `position_applied`, `interview_date`, `interview_status`, `offer_status`, `hr_id` [FK])
    """)
