"""
Employee & HR Management System
Upgraded Streamlit dashboard:
- responsive dashboard UI
- searchable/filterable data views
- real CRUD workflows
- exports
- read-only SQL studio
- schema explorer + relationship viewer
- lightweight demo RBAC
"""

import datetime as dt
import re
import io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from database.connection import get_connection_status, try_connect_mysql, DB_CONFIG, run_query
from database.queries import (
    get_executive_kpis, get_employees, add_employee, update_employee, delete_employee,
    get_departments, get_projects, add_project, update_project_status,
    get_project_assignments, assign_employee_to_project,
    get_attendance_records, log_attendance,
    get_leave_requests, add_leave_request, update_leave_status,
    get_payroll_records, add_payroll_record,
    get_performance_reviews, add_performance_review,
    get_trainings, add_training, get_training_enrollments, enroll_employee_training,
    get_recruitment_candidates, add_recruitment_candidate, update_recruitment_status,
    get_hr_managers, get_schema_metadata, get_relationships, get_table_data,
    COMPLEX_QUERIES_CATALOG
)

# ---------------------------------------------------------------------------
# Page + theme
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="HR Management Hub",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
:root { --border:#243044; --panel:#111827; --muted:#94a3b8; }
[data-testid="stAppViewContainer"] { background:#080d16; }
[data-testid="stSidebar"] { background:#0b111b; border-right:1px solid #1e293b; }
.block-container { padding-top:1.4rem; padding-bottom:2rem; max-width:1500px; }
h1,h2,h3 { letter-spacing:-.02em; }
h1 { font-size:2rem !important; }
h2 { font-size:1.35rem !important; }
h3 { font-size:1rem !important; }
div[data-testid="stMetric"] {
  background:linear-gradient(135deg,#111827,#0d1522);
  border:1px solid #243044; border-radius:12px; padding:14px;
}
div[data-testid="stMetricValue"] { font-size:1.55rem; }
div[data-testid="stMetricLabel"] { color:#94a3b8; }
.stButton>button,.stDownloadButton>button {
  border-radius:8px; font-weight:600; min-height:38px;
}
div[data-testid="stExpander"] { border:1px solid #243044; border-radius:10px; }
.small-muted { color:#94a3b8; font-size:.82rem; }
.hero {
  padding:20px 22px; border:1px solid #243044; border-radius:16px;
  background:linear-gradient(120deg,#111827,#0d1726);
  margin-bottom:16px;
}
.hero-title { font-size:1.55rem; font-weight:800; color:#f8fafc; }
.hero-sub { color:#94a3b8; margin-top:4px; font-size:.88rem; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def flash(ok, msg):
    (st.success if ok else st.error)(msg)
    if ok:
        st.cache_data.clear()

def csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")

def download_df(df: pd.DataFrame, filename: str, label="⬇️ Export CSV"):
    st.download_button(
        label=label,
        data=csv_bytes(df),
        file_name=filename,
        mime="text/csv",
        use_container_width=False,
    )

def employee_maps():
    df = get_employees()
    names = {r["full_name"]: int(r["employee_id"]) for _, r in df.iterrows()}
    return df, names

def dept_map():
    d = get_departments()
    return d, {r["department_name"]: int(r["department_id"]) for _, r in d.iterrows()}

def hr_map():
    h = get_hr_managers()
    return h, {r["hr_name"]: int(r["hr_id"]) for _, r in h.iterrows()}

def status_badge(value):
    v = str(value)
    cls = {
        "Approved":"🟢", "Present":"🟢", "Remote":"🔵", "Completed":"🟢",
        "Pending":"🟡", "Scheduled":"🟡", "Planning":"🟡",
        "Rejected":"🔴", "Absent":"🔴", "On-Leave":"🟠",
        "Ongoing":"🔵", "Completed":"🟢", "Cancelled":"🔴"
    }.get(v, "⚪")
    return f"{cls} {v}"

def require_role(role):
    roles = {"Viewer":0, "HR Manager":1, "Administrator":2}
    current = st.session_state.get("role", "Administrator")
    return roles[current] >= roles[role]

def safe_sql(sql):
    """Allow only a single read-only SQL statement."""
    q = sql.strip()
    if not q:
        raise ValueError("Enter a query.")
    if q.count(";") > 1 or (";" in q and not q.endswith(";")):
        raise ValueError("Only one SQL statement is allowed.")
    q = q.rstrip(";").strip()
    first = re.match(r"^\s*(\w+)", q, flags=re.I)
    keyword = first.group(1).upper() if first else ""
    allowed = {"SELECT", "WITH", "SHOW", "DESCRIBE", "DESC", "EXPLAIN"}
    if keyword not in allowed:
        raise ValueError("SQL Studio is read-only. Use SELECT, WITH, SHOW, DESCRIBE, DESC or EXPLAIN.")
    forbidden = re.search(
        r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE|REPLACE|GRANT|REVOKE|CALL|SET|USE|ATTACH|DETACH|PRAGMA)\b",
        q, flags=re.I
    )
    if forbidden:
        raise ValueError(f"Read-only SQL blocked: {forbidden.group(1).upper()}")
    return q

def render_df(df, height=420):
    if df is None or df.empty:
        st.info("No records match the current filters.")
        return
    st.dataframe(df, use_container_width=True, hide_index=True, height=height)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🏢 HR Management Hub")
    st.caption("Normalized Employee & HR platform • 3NF")
    status = get_connection_status()
    if status["is_mysql"]:
        st.success(f"🟢 {status['engine']}\n\n{status['details']}")
    else:
        st.warning(f"🟡 {status['engine']}\n\n{status['details']}")

    st.markdown("### Access")
    role = st.selectbox(
        "Demo role",
        ["Administrator", "HR Manager", "Viewer"],
        index=["Administrator","HR Manager","Viewer"].index(st.session_state.get("role","Administrator")),
    )
    st.session_state["role"] = role
    st.caption({
        "Administrator":"Full data-management access",
        "HR Manager":"HR records + approvals; no destructive employee deletion",
        "Viewer":"Read-only analytics and exports",
    }[role])

    st.markdown("---")
    menu = st.radio(
        "Workspace",
        [
            "📊 Overview",
            "👥 Employees",
            "🏛️ Departments",
            "💼 Projects",
            "⏱️ Attendance & Leave",
            "💰 Payroll",
            "🌟 Performance & Training",
            "🎯 Recruitment",
            "🗄️ Schema Explorer",
            "⚡ SQL Studio",
            "📈 Reports & Export",
            "📜 3NF / Functional Dependencies",
        ],
    )

    with st.expander("⚙️ MySQL connection"):
        host = st.text_input("Host", DB_CONFIG["host"])
        port = st.number_input("Port", value=DB_CONFIG["port"], step=1)
        user = st.text_input("User", DB_CONFIG["user"])
        password = st.text_input("Password", DB_CONFIG["password"], type="password")
        database = st.text_input("Database", DB_CONFIG["database"])
        if st.button("Connect / initialize MySQL", use_container_width=True):
            ok, msg = try_connect_mysql({
                "host":host, "port":int(port), "user":user,
                "password":password, "database":database
            })
            flash(ok, msg)
            if ok: st.rerun()

    st.markdown("---")
    st.caption("Built for academic demo + GitHub showcase")

# ---------------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------------
if menu == "📊 Overview":
    k = get_executive_kpis()
    st.markdown("""
    <div class="hero">
      <div class="hero-title">Executive HR Dashboard</div>
      <div class="hero-sub">One place for workforce, payroll, attendance, projects and talent analytics.</div>
    </div>
    """, unsafe_allow_html=True)

    if "error" in k:
        st.error(k["error"])
    else:
        cols = st.columns(6)
        metrics = [
            ("Employees", k["total_employees"], "Current headcount"),
            ("Avg Salary", f"${k['avg_salary']:,.0f}", "Annual average"),
            ("Payroll", f"${k['total_payroll']:,.0f}", "Annual salary base"),
            ("Projects", f"{k['active_projects']} / {k['total_projects']}", "Ongoing / total"),
            ("Attendance", f"{k['attendance_rate']:.1f}%", "Present + Remote"),
            ("Avg Rating", f"{k['avg_rating']:.2f} / 5", "Performance reviews"),
        ]
        for c, (label,val,sub) in zip(cols,metrics):
            with c: st.metric(label,val,help=sub)

    dept = get_departments()
    projects = get_projects()
    leave = get_leave_requests()
    c1,c2 = st.columns([1.45,1])
    with c1:
        st.subheader("Department budget vs payroll")
        if not dept.empty:
            fig = go.Figure()
            fig.add_bar(x=dept.department_name, y=dept.budget, name="Budget")
            fig.add_bar(x=dept.department_name, y=dept.total_payroll, name="Payroll")
            fig.update_layout(barmode="group", height=360, margin=dict(l=10,r=10,t=20,b=70))
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Workforce distribution")
        if not dept.empty:
            fig = px.pie(dept, names="department_name", values="employee_count", hole=.5)
            fig.update_layout(height=360, margin=dict(l=5,r=5,t=20,b=20))
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Operational snapshot")
    a,b,c = st.columns(3)
    with a:
        st.metric("Projects needing staffing", int((projects.team_size == 0).sum()) if not projects.empty else 0)
    with b:
        st.metric("Pending leave requests", int((leave.approval_status == "Pending").sum()) if not leave.empty else 0)
    with c:
        st.metric("Departments", len(dept))
    st.dataframe(
        projects[["project_name","client_name","status","department_name","team_size","total_hours_worked"]]
        if not projects.empty else projects,
        use_container_width=True, hide_index=True
    )

# ---------------------------------------------------------------------------
# Employees
# ---------------------------------------------------------------------------
elif menu == "👥 Employees":
    st.markdown("## 👥 Employee Directory")
    emp, names = employee_maps()
    dept, dmap = dept_map()
    hr, hmap = hr_map()

    c1,c2,c3,c4 = st.columns([1.4,2.2,1,1])
    with c1:
        dept_filter = st.selectbox("Department", ["All"] + list(dmap.keys()))
    with c2:
        search = st.text_input("🔎 Search name, title or email")
    with c3:
        st.metric("Records", len(get_employees(
            dmap.get(dept_filter), search or None
        )))
    with c4:
        if not emp.empty: download_df(emp, "employees.csv")

    filtered = get_employees(dmap.get(dept_filter), search or None)
    display = filtered[["employee_id","full_name","job_title","department_name","salary","hire_date","email","phone_number","hr_manager"]].copy()
    display.columns = ["ID","Employee","Job Title","Department","Salary","Hire Date","Email","Phone","HR Partner"]
    render_df(display, 390)

    if not filtered.empty:
        st.markdown("---")
        selected_name = st.selectbox("Employee profile", filtered["full_name"].tolist())
        selected = filtered[filtered.full_name == selected_name].iloc[0]
        p1,p2,p3,p4 = st.columns(4)
        p1.metric("Employee ID", int(selected.employee_id))
        p2.metric("Salary", f"${selected.salary:,.0f}")
        p3.metric("Department", selected.department_name)
        p4.metric("HR", selected.hr_manager)
        st.caption(f"📧 {selected.email}  •  📞 {selected.phone_number}  •  📍 {selected.address}")

    if require_role("HR Manager"):
        with st.expander("➕ Add employee"):
            with st.form("add_employee"):
                r1,r2,r3 = st.columns(3)
                first = r1.text_input("First name")
                last = r2.text_input("Last name")
                gender = r3.selectbox("Gender", ["Female","Male","Non-binary","Prefer not to say"])
                r4,r5,r6 = st.columns(3)
                dob = r4.date_input("Date of birth", dt.date(1998,1,1))
                email = r5.text_input("Email")
                phone = r6.text_input("Phone")
                r7,r8,r9 = st.columns(3)
                address = r7.text_input("Address")
                hire = r8.date_input("Hire date", dt.date.today())
                salary = r9.number_input("Annual salary", min_value=1.0, value=60000.0, step=1000.0)
                r10,r11 = st.columns(2)
                title = r10.text_input("Job title")
                dep_name = r11.selectbox("Department", list(dmap.keys()))
                hr_name = st.selectbox("HR manager", list(hmap.keys()))
                if st.form_submit_button("Create employee", use_container_width=True):
                    if not first.strip() or not last.strip() or not email.strip() or not title.strip():
                        st.error("First name, last name, email and job title are required.")
                    else:
                        ok,msg=add_employee(first,last,gender,str(dob),email,phone,address,str(hire),
                                             salary,title,dmap[dep_name],hmap[hr_name])
                        flash(ok,msg)
                        if ok: st.rerun()

        with st.expander("✏️ Edit employee"):
            if not filtered.empty:
                edit_id = int(st.selectbox("Employee", filtered.employee_id.tolist(), format_func=lambda x: filtered.loc[filtered.employee_id==x,"full_name"].iloc[0]))
                e = filtered[filtered.employee_id==edit_id].iloc[0]
                with st.form("edit_employee"):
                    a,b,c=st.columns(3)
                    f=a.text_input("First name", e.first_name)
                    l=b.text_input("Last name", e.last_name)
                    g=c.selectbox("Gender",["Female","Male","Non-binary","Prefer not to say"], index=max(0,["Female","Male","Non-binary","Prefer not to say"].index(str(e.gender)) if str(e.gender) in ["Female","Male","Non-binary","Prefer not to say"] else 0))
                    a,b,c=st.columns(3)
                    edob=a.date_input("DOB", pd.to_datetime(e.date_of_birth).date())
                    em=b.text_input("Email", e.email)
                    ph=c.text_input("Phone", e.phone_number)
                    a,b,c=st.columns(3)
                    ad=a.text_input("Address", e.address)
                    hd=b.date_input("Hire date", pd.to_datetime(e.hire_date).date())
                    sal=c.number_input("Salary", min_value=1.0, value=float(e.salary), step=1000.0)
                    a,b=st.columns(2)
                    jt=a.text_input("Job title", e.job_title)
                    dn=b.selectbox("Department", list(dmap.keys()), index=list(dmap.keys()).index(e.department_name))
                    hn=st.selectbox("HR manager", list(hmap.keys()), index=list(hmap.keys()).index(e.hr_manager))
                    if st.form_submit_button("Save changes", use_container_width=True):
                        ok,msg=update_employee(edit_id,f,l,g,str(edob),em,ph,ad,str(hd),sal,jt,dmap[dn],hmap[hn])
                        flash(ok,msg)
                        if ok: st.rerun()

        if require_role("Administrator") and not filtered.empty:
            with st.expander("🗑️ Delete employee"):
                delete_id = st.selectbox("Employee to delete", filtered.employee_id.tolist(), format_func=lambda x: filtered.loc[filtered.employee_id==x,"full_name"].iloc[0], key="delete_emp")
                st.warning("This deletes the employee record and dependent bridge/attendance/review/training records according to the FK rules.")
                if st.button("Delete selected employee", type="secondary"):
                    ok,msg=delete_employee(int(delete_id))
                    flash(ok,msg)
                    if ok: st.rerun()

# ---------------------------------------------------------------------------
# Departments
# ---------------------------------------------------------------------------
elif menu == "🏛️ Departments":
    st.markdown("## 🏛️ Departments & Managers")
    d = get_departments()
    c1,c2,c3=st.columns(3)
    c1.metric("Departments",len(d))
    c2.metric("Allocated budget",f"${d.budget.sum():,.0f}" if not d.empty else "$0")
    c3.metric("Payroll",f"${d.total_payroll.sum():,.0f}" if not d.empty else "$0")
    render_df(d.rename(columns={
        "department_id":"ID","department_name":"Department","location":"Location",
        "budget":"Budget","manager_name":"Manager","employee_count":"Headcount",
        "total_payroll":"Payroll","budget_utilized_pct":"Payroll / Budget %"
    }))
    if not d.empty:
        fig=px.bar(d,x="department_name",y="budget_utilized_pct",labels={"department_name":"Department","budget_utilized_pct":"Payroll / Budget %"})
        st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------
elif menu == "💼 Projects":
    st.markdown("## 💼 Projects & Staffing")
    p = get_projects()
    if not p.empty:
        c1,c2,c3=st.columns(3)
        c1.metric("Projects",len(p))
        c2.metric("Ongoing",int((p.status=="Ongoing").sum()))
        c3.metric("Hours logged",f"{p.total_hours_worked.sum():,.0f}")
        render_df(p.rename(columns={
            "project_id":"ID","project_name":"Project","client_name":"Client","budget":"Budget",
            "status":"Status","start_date":"Start","end_date":"End","department_name":"Owner",
            "team_size":"Team","total_hours_worked":"Hours"
        }))
        if require_role("HR Manager"):
            with st.expander("➕ Create project"):
                d,dmap=dept_map()
                with st.form("project_form"):
                    a,b=st.columns(2)
                    name=a.text_input("Project name")
                    client=b.text_input("Client")
                    a,b,c=st.columns(3)
                    start=a.date_input("Start",dt.date.today())
                    end=b.date_input("End",dt.date.today()+dt.timedelta(days=90))
                    budget=c.number_input("Budget",min_value=0.0,value=100000.0,step=5000.0)
                    a,b=st.columns(2)
                    status= a.selectbox("Status",["Planning","Ongoing","Completed","Cancelled"])
                    owner=b.selectbox("Department",list(dmap.keys()))
                    if st.form_submit_button("Create project",use_container_width=True):
                        ok,msg=add_project(name,str(start),str(end),budget,client,status,dmap[owner])
                        flash(ok,msg)
                        if ok: st.rerun()

        with st.expander("👥 Project staffing"):
            project_name=st.selectbox("Project",p.project_name.tolist())
            pid=int(p.loc[p.project_name==project_name,"project_id"].iloc[0])
            assignments=get_project_assignments(pid)
            render_df(assignments[["employee_name","job_title","employee_role","hours_worked","assigned_date"]]
                      if not assignments.empty else assignments, 280)
            if require_role("HR Manager"):
                emp,emap=employee_maps()
                with st.form("assign_project"):
                    a,b,c,d=st.columns(4)
                    en=a.selectbox("Employee",list(emap.keys()))
                    role=a.text_input("Project role",key="project_role")
                    hours=b.number_input("Hours worked",0.0,2000.0,40.0,5.0)
                    assigned=c.date_input("Assigned date",dt.date.today())
                    if st.form_submit_button("Assign",use_container_width=True):
                        if not role.strip():
                            st.error("Project role is required.")
                        else:
                            ok,msg=assign_employee_to_project(emap[en],pid,str(assigned),role,hours)
                            flash(ok,msg)
                            if ok: st.rerun()
                new_status=st.selectbox("Update project status",["Planning","Ongoing","Completed","Cancelled"],key="proj_status")
                if st.button("Save project status"):
                    ok,msg=update_project_status(pid,new_status)
                    flash(ok,msg)
                    if ok: st.rerun()

# ---------------------------------------------------------------------------
# Attendance & Leave
# ---------------------------------------------------------------------------
elif menu == "⏱️ Attendance & Leave":
    st.markdown("## ⏱️ Attendance & Leave")
    tab1,tab2=st.tabs(["Attendance","Leave"])
    with tab1:
        att=get_attendance_records()
        a,b,c,d=st.columns(4)
        a.metric("Logs",len(att))
        b.metric("Present / Remote",int(att.attendance_status.isin(["Present","Remote"]).sum()) if not att.empty else 0)
        c.metric("Absent",int((att.attendance_status=="Absent").sum()) if not att.empty else 0)
        d.metric("Avg hours",f"{att.work_hours.mean():.1f}" if not att.empty else "0")
        filter_by_date = st.checkbox("Filter by date", value=False)
        date_filter = st.date_input("Attendance date", value=dt.date.today()) if filter_by_date else None
        att_view = get_attendance_records(str(date_filter)) if date_filter else att
        render_df(att_view.rename(columns={
            "attendance_id":"ID","date":"Date","employee_name":"Employee","department_name":"Department",
            "check_in_time":"Check-in","check_out_time":"Check-out","work_hours":"Hours","attendance_status":"Status"
        }))
        download_df(att_view,"attendance.csv")
        if require_role("HR Manager"):
            with st.expander("➕ Log attendance"):
                emp,emap=employee_maps()
                with st.form("attendance_form"):
                    a,b,c,d=st.columns(4)
                    en=a.selectbox("Employee",list(emap.keys()))
                    day=b.date_input("Date",dt.date.today())
                    cin=c.text_input("Check-in","09:00:00")
                    cout=c.text_input("Check-out","17:30:00")
                    hours=d.number_input("Work hours",0.0,24.0,8.5,.5)
                    status=a.selectbox("Status",["Present","Remote","Half-Day","On-Leave","Absent"])
                    if st.form_submit_button("Record attendance",use_container_width=True):
                        ok,msg=log_attendance(emap[en],str(day),None if status in ["Absent","On-Leave"] else cin,
                                              None if status in ["Absent","On-Leave"] else cout,hours,status)
                        flash(ok,msg)
                        if ok: st.rerun()
    with tab2:
        leave=get_leave_requests()
        pending=leave[leave.approval_status=="Pending"] if not leave.empty else leave
        c1,c2,c3=st.columns(3)
        c1.metric("Requests",len(leave)); c2.metric("Pending",len(pending)); c3.metric("Approved",int((leave.approval_status=="Approved").sum()) if not leave.empty else 0)
        if not pending.empty and require_role("HR Manager"):
            st.subheader("Pending approvals")
            for _,r in pending.iterrows():
                x1,x2,x3=st.columns([3,2,1])
                x1.markdown(f"**{r.employee_name}** • {r.leave_type}")
                x1.caption(r.reason or "No reason supplied")
                x2.write(f"{r.start_date} → {r.end_date}")
                if x3.button("Approve",key=f"approve_{r.leave_id}"):
                    ok,msg=update_leave_status(int(r.leave_id),"Approved"); flash(ok,msg); st.rerun()
                if x3.button("Reject",key=f"reject_{r.leave_id}"):
                    ok,msg=update_leave_status(int(r.leave_id),"Rejected"); flash(ok,msg); st.rerun()
        render_df(leave.rename(columns={
            "leave_id":"ID","employee_name":"Employee","department_name":"Department",
            "leave_type":"Type","start_date":"From","end_date":"To","reason":"Reason","approval_status":"Status"
        }))
        download_df(leave,"leave_requests.csv")
        if require_role("HR Manager"):
            with st.expander("➕ Submit leave request"):
                emp,emap=employee_maps()
                with st.form("leave_form"):
                    a,b,c=st.columns(3)
                    en=a.selectbox("Employee",list(emap.keys()))
                    lt=b.selectbox("Leave type",["Annual","Sick","Casual","Unpaid"])
                    reason=c.text_input("Reason")
                    a,b=st.columns(2)
                    start=a.date_input("From",dt.date.today())
                    end=b.date_input("To",dt.date.today())
                    if st.form_submit_button("Submit leave",use_container_width=True):
                        if end < start: st.error("End date cannot be before start date.")
                        else:
                            ok,msg=add_leave_request(emap[en],lt,str(start),str(end),reason); flash(ok,msg)
                            if ok: st.rerun()

# ---------------------------------------------------------------------------
# Payroll
# ---------------------------------------------------------------------------
elif menu == "💰 Payroll":
    st.markdown("## 💰 Payroll & Compensation")
    pay=get_payroll_records()
    emp=get_employees()
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Net paid",f"${pay.net_salary.sum():,.0f}" if not pay.empty else "$0")
    c2.metric("Basic",f"${pay.basic_salary.sum():,.0f}" if not pay.empty else "$0")
    c3.metric("Allowances",f"${pay.allowances.sum():,.0f}" if not pay.empty else "$0")
    c4.metric("Deductions",f"${pay.deductions.sum():,.0f}" if not pay.empty else "$0")
    render_df(pay.rename(columns={
        "payroll_id":"ID","payment_date":"Payment Date","employee_name":"Employee",
        "department_name":"Department","basic_salary":"Basic","allowances":"Allowances",
        "deductions":"Deductions","net_salary":"Net Salary"
    }))
    download_df(pay,"payroll.csv")
    if not emp.empty and not pay.empty:
        by_dept=pay.groupby("department_name",as_index=False).net_salary.sum()
        fig=px.bar(by_dept,x="department_name",y="net_salary",labels={"net_salary":"Net salary paid","department_name":"Department"})
        st.plotly_chart(fig,use_container_width=True)
    if require_role("Administrator"):
        with st.expander("➕ Add payroll record"):
            _,emap=employee_maps()
            with st.form("payroll_form"):
                a,b,c,d=st.columns(4)
                en=a.selectbox("Employee",list(emap.keys()))
                basic=b.number_input("Basic salary",1.0,10000000.0,50000.0,1000.0)
                allowances=c.number_input("Allowances",0.0,1000000.0,5000.0,500.0)
                deductions=d.number_input("Deductions",0.0,1000000.0,3000.0,500.0)
                day=st.date_input("Payment date",dt.date.today())
                if st.form_submit_button("Create payroll record",use_container_width=True):
                    ok,msg=add_payroll_record(emap[en],basic,allowances,deductions,str(day)); flash(ok,msg)
                    if ok: st.rerun()

# ---------------------------------------------------------------------------
# Performance & Training
# ---------------------------------------------------------------------------
elif menu == "🌟 Performance & Training":
    st.markdown("## 🌟 Performance & Training")
    tab1,tab2=st.tabs(["Performance","Training"])
    with tab1:
        reviews=get_performance_reviews()
        c1,c2=st.columns([1,2])
        with c1:
            if not reviews.empty:
                counts=reviews.rating.value_counts().sort_index().reset_index()
                fig=px.bar(counts,x="rating",y="count",labels={"rating":"Rating","count":"Reviews"})
                st.plotly_chart(fig,use_container_width=True)
        with c2:
            render_df(reviews.rename(columns={
                "review_id":"ID","review_date":"Date","employee_name":"Employee",
                "job_title":"Role","department_name":"Department","reviewer_name":"Reviewer",
                "rating":"Rating","comments":"Feedback"
            }))
        download_df(reviews,"performance_reviews.csv")
        if require_role("HR Manager"):
            with st.expander("➕ Add performance review"):
                _,emap=employee_maps()
                with st.form("review_form"):
                    en=st.selectbox("Employee",list(emap.keys()))
                    reviewer=st.text_input("Reviewer")
                    rating=st.slider("Rating",1,5,4)
                    comments=st.text_area("Feedback")
                    if st.form_submit_button("Save review",use_container_width=True):
                        if not reviewer.strip(): st.error("Reviewer is required.")
                        else:
                            ok,msg=add_performance_review(emap[en],reviewer,str(dt.date.today()),rating,comments); flash(ok,msg)
                            if ok: st.rerun()
    with tab2:
        train=get_trainings()
        c1,c2,c3=st.columns(3)
        c1.metric("Programs",len(train)); c2.metric("Enrollments",int(train.enrolled_count.sum()) if not train.empty else 0)
        c3.metric("Avg score",f"{train.avg_assessment_score.mean():.1f}" if not train.empty and train.avg_assessment_score.notna().any() else "—")
        render_df(train.rename(columns={
            "training_id":"ID","training_name":"Course","trainer_name":"Trainer",
            "training_type":"Type","cost":"Cost","start_date":"Start","end_date":"End",
            "enrolled_count":"Enrolled","avg_assessment_score":"Avg score"
        }))
        download_df(train,"training_catalog.csv")
        if not train.empty:
            selected=st.selectbox("Inspect course",train.training_name.tolist())
            tid=int(train.loc[train.training_name==selected,"training_id"].iloc[0])
            enroll=get_training_enrollments(tid)
            render_df(enroll[["employee_name","completion_status","score"]].rename(columns={
                "employee_name":"Employee","completion_status":"Status","score":"Score"
            }),250)
            if require_role("HR Manager"):
                _,emap=employee_maps()
                with st.form("enroll_form"):
                    en=st.selectbox("Employee",list(emap.keys()))
                    status=st.selectbox("Completion status",["Enrolled","In Progress","Completed"])
                    score=st.number_input("Score (optional)",0.0,100.0,0.0,1.0)
                    if st.form_submit_button("Enroll employee",use_container_width=True):
                        ok,msg=enroll_employee_training(emap[en],tid,status,None if score==0 else score); flash(ok,msg)
                        if ok: st.rerun()
        if require_role("Administrator"):
            with st.expander("➕ Create training program"):
                with st.form("training_form"):
                    a,b=st.columns(2); name=a.text_input("Training name"); trainer=b.text_input("Trainer")
                    a,b,c=st.columns(3)
                    start=a.date_input("Start",dt.date.today()); end=b.date_input("End",dt.date.today()+dt.timedelta(days=1))
                    typ=c.selectbox("Type",["Technical","Compliance","Leadership","Soft Skills"])
                    cost=st.number_input("Cost",0.0,1000000.0,1000.0,100.0)
                    if st.form_submit_button("Create training",use_container_width=True):
                        ok,msg=add_training(name,trainer,str(start),str(end),typ,cost); flash(ok,msg)
                        if ok: st.rerun()

# ---------------------------------------------------------------------------
# Recruitment
# ---------------------------------------------------------------------------
elif menu == "🎯 Recruitment":
    st.markdown("## 🎯 Recruitment Funnel")
    rec=get_recruitment_candidates()
    c1,c2,c3,c4=st.columns(4)
    total=len(rec)
    c1.metric("Candidates",total)
    c2.metric("Interviews completed",int((rec.interview_status=="Completed").sum()) if total else 0)
    c3.metric("Offers accepted",int((rec.offer_status=="Accepted").sum()) if total else 0)
    accepted=int((rec.offer_status=="Accepted").sum()) if total else 0
    c4.metric("Conversion",f"{accepted/total*100:.1f}%" if total else "0%")
    render_df(rec.rename(columns={
        "recruitment_id":"ID","candidate_name":"Candidate","position_applied":"Position",
        "interview_date":"Interview","interview_status":"Interview Status",
        "offer_status":"Offer Status","coordinator":"HR Coordinator"
    }))
    download_df(rec,"recruitment.csv")
    if require_role("HR Manager"):
        with st.expander("➕ Add candidate"):
            _,hmap=hr_map()
            with st.form("candidate_form"):
                a,b,c=st.columns(3)
                name=a.text_input("Candidate name"); position=b.text_input("Position")
                day=c.date_input("Interview date",dt.date.today())
                a,b,c=st.columns(3)
                ist=a.selectbox("Interview status",["Scheduled","Completed","Cancelled"])
                ost=b.selectbox("Offer status",["Pending","Accepted","Rejected"])
                hrn=c.selectbox("Coordinator",list(hmap.keys()))
                if st.form_submit_button("Add candidate",use_container_width=True):
                    if not name.strip() or not position.strip(): st.error("Candidate and position are required.")
                    else:
                        ok,msg=add_recruitment_candidate(name,position,str(day),ist,ost,hmap[hrn]); flash(ok,msg)
                        if ok: st.rerun()
        if not rec.empty:
            with st.expander("✏️ Update candidate status"):
                rid=st.selectbox("Candidate",rec.recruitment_id.tolist(),format_func=lambda x: rec.loc[rec.recruitment_id==x,"candidate_name"].iloc[0])
                rr=rec[rec.recruitment_id==rid].iloc[0]
                a,b=st.columns(2)
                ist=a.selectbox("Interview",["Scheduled","Completed","Cancelled"],index=["Scheduled","Completed","Cancelled"].index(rr.interview_status))
                ost=b.selectbox("Offer",["Pending","Accepted","Rejected"],index=["Pending","Accepted","Rejected"].index(rr.offer_status))
                if st.button("Save status"):
                    ok,msg=update_recruitment_status(int(rid),ist,ost); flash(ok,msg)
                    if ok: st.rerun()

# ---------------------------------------------------------------------------
# Schema explorer
# ---------------------------------------------------------------------------
elif menu == "🗄️ Schema Explorer":
    st.markdown("## 🗄️ Schema Explorer")
    meta=get_schema_metadata()
    rel=get_relationships()
    c1,c2,c3=st.columns(3)
    c1.metric("Tables",meta.table_name.nunique() if not meta.empty else 0)
    c2.metric("Columns",len(meta))
    c3.metric("Foreign keys",len(rel))
    tabs=st.tabs(["Tables & columns","Relationships","Table data"])
    with tabs[0]:
        if not meta.empty:
            table_counts=meta.groupby("table_name").size().reset_index(name="columns")
            selected=st.selectbox("Inspect table",table_counts.table_name.tolist())
            st.dataframe(meta[meta.table_name==selected],use_container_width=True,hide_index=True)
    with tabs[1]:
        if rel.empty: st.info("No foreign-key metadata found.")
        else:
            st.dataframe(rel,use_container_width=True,hide_index=True)
            # compact relationship matrix
            nodes=sorted(set(rel.child_table.tolist()+rel.parent_table.tolist()))
            node_index={n:i for i,n in enumerate(nodes)}
            fig=go.Figure()
            for _,r in rel.iterrows():
                x=[node_index[r.child_table],node_index[r.parent_table]]
                y=[0,0]
                fig.add_trace(go.Scatter(x=x,y=y,mode="lines",line=dict(width=1),showlegend=False,hovertext=f"{r.child_table}.{r.child_column} → {r.parent_table}.{r.parent_column}",hoverinfo="text"))
            fig.add_trace(go.Scatter(
                x=list(range(len(nodes))),y=[0]*len(nodes),mode="markers+text",
                text=nodes,textposition="top center",marker=dict(size=18),showlegend=False
            ))
            fig.update_layout(height=260,xaxis=dict(showticklabels=False),yaxis=dict(visible=False),margin=dict(l=20,r=20,t=30,b=40))
            st.plotly_chart(fig,use_container_width=True)
    with tabs[2]:
        tables=sorted(meta.table_name.unique().tolist()) if not meta.empty else []
        if tables:
            table=st.selectbox("Table",tables)
            limit=st.slider("Rows",10,500,100,10)
            data=get_table_data(table,limit)
            render_df(data,420)
            download_df(data,f"{table}.csv")

# ---------------------------------------------------------------------------
# SQL Studio
# ---------------------------------------------------------------------------
elif menu == "⚡ SQL Studio":
    st.markdown("## ⚡ Read-only SQL Studio")
    st.caption("Borrowed from the other team's stronger DBA workflow: presets, keyboard execution, clear errors and CSV export.")
    preset_names=list(COMPLEX_QUERIES_CATALOG.keys())
    preset=st.selectbox("Preset query",["Custom"]+preset_names)
    default="" if preset=="Custom" else COMPLEX_QUERIES_CATALOG[preset]["sql"]
    query=st.text_area("SQL",value=default,height=260,placeholder="SELECT ...",key="sql_editor")
    if preset!="Custom":
        st.info(COMPLEX_QUERIES_CATALOG[preset]["description"])
    if st.button("▶ Run query",type="primary"):
        try:
            q=safe_sql(query)
            with st.spinner("Executing read-only query..."):
                result=run_query(q)
            st.success(f"Query executed • {len(result):,} row(s)")
            render_df(result,460)
            download_df(result,"sql_query_result.csv")
            if not result.empty:
                numeric=result.select_dtypes(include="number").columns.tolist()
                text_cols=result.select_dtypes(include=["object","string"]).columns.tolist()
                if numeric and text_cols and len(result)<=50:
                    fig=px.bar(result,x=text_cols[0],y=numeric[0])
                    st.plotly_chart(fig,use_container_width=True)
        except Exception as e:
            st.error(str(e))

# ---------------------------------------------------------------------------
# Reports & Export
# ---------------------------------------------------------------------------
elif menu == "📈 Reports & Export":
    st.markdown("## 📈 Reports & Export")
    st.caption("This is the other team's report/export pattern adapted to the Employee & HR domain.")
    k=get_executive_kpis()
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Employees",k.get("total_employees",0))
    c2.metric("Payroll",f"${k.get('total_payroll',0):,.0f}")
    c3.metric("Avg salary",f"${k.get('avg_salary',0):,.0f}")
    c4.metric("Attendance",f"{k.get('attendance_rate',0):.1f}%")
    report_tabs=st.tabs(["Workforce","Finance","Talent","Operations"])
    emp=get_employees(); pay=get_payroll_records(); perf=get_performance_reviews()
    rec=get_recruitment_candidates(); train=get_trainings(); att=get_attendance_records(); leave=get_leave_requests()
    with report_tabs[0]:
        download_df(emp,"workforce_report.csv","⬇️ Workforce CSV")
        render_df(emp[["employee_id","full_name","job_title","department_name","salary","hire_date","hr_manager"]])
    with report_tabs[1]:
        download_df(pay,"payroll_report.csv","⬇️ Payroll CSV")
        if not pay.empty:
            by_dept=pay.groupby("department_name",as_index=False).agg(net_salary=("net_salary","sum"),deductions=("deductions","sum"))
            render_df(by_dept)
    with report_tabs[2]:
        download_df(perf,"performance_report.csv","⬇️ Performance CSV")
        download_df(train,"training_report.csv","⬇️ Training CSV")
        download_df(rec,"recruitment_report.csv","⬇️ Recruitment CSV")
    with report_tabs[3]:
        download_df(att,"attendance_report.csv","⬇️ Attendance CSV")
        download_df(leave,"leave_report.csv","⬇️ Leave CSV")

# ---------------------------------------------------------------------------
# 3NF
# ---------------------------------------------------------------------------
elif menu == "📜 3NF / Functional Dependencies":
    st.markdown("## 📜 3NF & Functional Dependency Proof")
    st.markdown("""
    **Core dependencies**

    - `Employee_ID → Department_ID, HR_ID, employee attributes`
    - `Department_ID → Department_Name, Location, Budget, Manager_Name`
    - `Project_ID → Project_Name, Budget, Client_Name, Status, Department_ID`
    - `{Employee_ID, Project_ID} → Employee_Role, Hours_Worked`
    - `{Employee_ID, Training_ID} → Completion_Status, Score`
    - `HR_ID → HR manager attributes`

    **1NF:** attributes are atomic and M:N relationships are represented by bridge tables.

    **2NF:** attributes of `EMPLOYEE_PROJECT` and `EMPLOYEE_TRAINING` depend on their complete composite keys.

    **3NF:** department and HR-manager facts are separated from `EMPLOYEE`, removing transitive dependencies such as
    `Employee_ID → Department_ID → Department_Name`.

    **Result:** the core academic schema remains decomposed into the 12 normalized entities already present in the project.
    """)
    st.info("Use **Schema Explorer → Relationships** to inspect the actual foreign-key structure from the running database.")
