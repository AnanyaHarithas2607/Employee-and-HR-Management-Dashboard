import os
import sys

# Ensure project root is in Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database.connection import get_connection_status, run_query
from database.queries import get_executive_kpis, get_employees, COMPLEX_QUERIES_CATALOG

print("==================================================")
print("     EMPLOYEE & HR SYSTEM VERIFICATION SUITE      ")
print("==================================================")

status = get_connection_status()
print(f"Engine : {status['engine']}")
print(f"Status : {status['status']}")
print(f"Details: {status['details']}")

print("\n--- Executive KPIs ---")
kpis = get_executive_kpis()
for k, v in kpis.items():
    print(f"  {k}: {v}")

print("\n--- Employee Records ---")
emps = get_employees()
print(f"Total employees fetched: {len(emps)}")
print(f"Sample: {emps.iloc[0]['full_name']} | {emps.iloc[0]['job_title']} | {emps.iloc[0]['department_name']}")

print("\n--- Executing 10 Graded Assignment Queries ---")
all_passed = True
for title, item in COMPLEX_QUERIES_CATALOG.items():
    try:
        df = run_query(item["sql"])
        print(f"  [PASS] {title} -> {len(df)} row(s)")
    except Exception as e:
        print(f"  [FAIL] {title} -> Error: {e}")
        all_passed = False

if all_passed:
    print("\n>>> ALL TESTS PASSED! System is 100% operational.")
else:
    print("\n>>> Some tests failed.")
