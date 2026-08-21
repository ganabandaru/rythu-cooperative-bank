"""
Rythu Cooperative Bank — Synthetic Data Generator
Generates realistic banking data (no external libraries like Faker needed)
using hand-built Telangana-region name/city pools.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# ---------- Reference pools ----------
FIRST_NAMES = [
    "Arjun","Karthik","Venkat","Lakshmi","Ramesh","Sneha","Ravi","Teja","Krishna","Divya",
    "Sameer","Meghana","Anitha","Suresh","Prasad","Kavya","Naveen","Swathi","Manoj","Priya",
    "Srinivas","Padma","Rajesh","Sunitha","Vijay","Bhavani","Kiran","Anjali","Mahesh","Radha",
    "Sandeep","Pallavi","Ramana","Vani","Nagesh","Sowmya","Ashok","Deepika","Ganesh","Harika",
    "Rakesh","Jyothi","Satish","Keerthi","Vinod","Madhavi","Prakash","Neha","Ramu","Sunil"
]
LAST_NAMES = [
    "Reddy","Rao","Naidu","Goud","Sharma","Kumar","Chary","Reddy","Rao","Naik",
    "Yadav","Verma","Prasad","Varma","Raju","Babu","Rathod","Patel","Setty","Murthy"
]
CITIES = ["Warangal","Karimnagar","Nizamabad","Khammam","Suryapet"]
OCCUPATIONS = ["Farmer","Small Business Owner","Teacher","Daily Wage Worker",
               "Government Employee","Student","Homemaker","Shop Owner","Auto Driver","Tailor"]
ROLES = ["Clerk","Cashier","Loan Officer","Branch Manager","Accountant"]
STREETS = ["Gandhi Nagar","Ashok Nagar","Market Street","Station Road","Temple Street",
           "Ring Road","Housing Board Colony","Old Town","New Colony","Bus Stand Road"]

def rand_name(): return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
def rand_phone(): return "9" + "".join(random.choices("0123456789", k=9))
def rand_address(city): return f"{random.randint(1,999)}-{random.randint(1,20)}, {random.choice(STREETS)}, {city}"
def rand_aadhaar(): return "".join(random.choices("0123456789", k=12))
def rand_pan():
    letters = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5))
    digits = "".join(random.choices("0123456789", k=4))
    return letters + digits + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
def rand_date(start, end):
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, max(delta, 0)))

YEARS = 3
TODAY = datetime(2026, 8, 4)
START = TODAY - timedelta(days=365 * YEARS)

# ---------- 1. BRANCHES ----------
N_BRANCHES = 5
branches = pd.DataFrame({
    "branch_id": range(1, N_BRANCHES + 1),
    "branch_name": [f"Rythu Cooperative Bank - {c}" for c in CITIES],
    "city": CITIES,
    "address": [rand_address(c) for c in CITIES],
    "manager_name": [rand_name() for _ in range(N_BRANCHES)]
})

# ---------- 2. EMPLOYEES ----------
N_EMPLOYEES = 40
employees = pd.DataFrame({
    "employee_id": range(1, N_EMPLOYEES + 1),
    "branch_id": np.random.choice(branches.branch_id, N_EMPLOYEES),
    "name": [rand_name() for _ in range(N_EMPLOYEES)],
    "role": np.random.choice(ROLES, N_EMPLOYEES, p=[0.35, 0.25, 0.2, 0.1, 0.1]),
    "phone": [rand_phone() for _ in range(N_EMPLOYEES)],
    "salary": np.random.randint(15000, 60000, N_EMPLOYEES)
})
employees.loc[0, "name"] = "Lakshmi Rao"
employees.loc[0, "role"] = "Clerk"

# ---------- 3. CUSTOMERS ----------
N_CUSTOMERS = 2000
cust_branch = np.random.choice(branches.branch_id, N_CUSTOMERS)
cust_city = [branches.set_index("branch_id").loc[b, "city"] for b in cust_branch]
customers = pd.DataFrame({
    "customer_id": range(1, N_CUSTOMERS + 1),
    "aadhaar": [rand_aadhaar() for _ in range(N_CUSTOMERS)],
    "pan": [rand_pan() for _ in range(N_CUSTOMERS)],
    "name": [rand_name() for _ in range(N_CUSTOMERS)],
    "phone": [rand_phone() for _ in range(N_CUSTOMERS)],
    "dob": [rand_date(datetime(1951, 1, 1), datetime(2008, 1, 1)).date() for _ in range(N_CUSTOMERS)],
    "address": [rand_address(c) for c in cust_city],
    "occupation": np.random.choice(OCCUPATIONS, N_CUSTOMERS),
    "branch_id": cust_branch
})
# Story character: Ramesh, a farmer, for the fraud arc
customers.loc[0, ["name", "occupation", "branch_id"]] = ["Ramesh Naik", "Farmer", 1]

# ---------- 4. ACCOUNTS ----------
acc_rows = []
account_id = 1
for cid, bid in zip(customers.customer_id, customers.branch_id):
    n_acc = np.random.choice([1, 2], p=[0.75, 0.25])
    for _ in range(n_acc):
        opened = rand_date(START, TODAY)
        acc_rows.append({
            "account_id": account_id, "customer_id": cid, "branch_id": bid,
            "account_type": np.random.choice(["Savings", "Current"], p=[0.8, 0.2]),
            "balance": round(float(np.random.uniform(500, 200000)), 2),
            "opened_date": opened.date(),
            "status": np.random.choice(["Active", "Closed"], p=[0.95, 0.05])
        })
        account_id += 1
accounts = pd.DataFrame(acc_rows)

# ---------- 5. LOANS ----------
N_LOANS = int(N_CUSTOMERS * 0.2)
loan_customers = np.random.choice(customers.customer_id, N_LOANS, replace=False)
cust_branch_map = customers.set_index("customer_id")["branch_id"]
loans = pd.DataFrame({
    "loan_id": range(1, N_LOANS + 1),
    "customer_id": loan_customers,
    "branch_id": [cust_branch_map.loc[c] for c in loan_customers],
    "staff_id": np.random.choice(employees.employee_id, N_LOANS),
    "loan_amount": np.random.randint(20000, 500000, N_LOANS),
    "interest_rate": np.round(np.random.uniform(7, 14, N_LOANS), 2),
    "duration_months": np.random.choice([12, 24, 36, 60], N_LOANS),
    "status": np.random.choice(["Active", "Closed", "Defaulted"], N_LOANS, p=[0.6, 0.3, 0.1]),
    "disbursed_date": [rand_date(START, TODAY - timedelta(days=60)).date() for _ in range(N_LOANS)]
})

# ---------- 6. LOAN_PAYMENTS ----------
payment_rows, payment_id = [], 1
for _, loan in loans.iterrows():
    n_payments = np.random.randint(1, 12)
    balance = loan.loan_amount
    disb = datetime.combine(loan.disbursed_date, datetime.min.time())
    for i in range(n_payments):
        pay_amt = round(loan.loan_amount / loan.duration_months * float(np.random.uniform(0.8, 1.2)), 2)
        balance = max(0, balance - pay_amt)
        payment_rows.append({
            "payment_id": payment_id, "loan_id": loan.loan_id, "amount": pay_amt,
            "payment_date": (disb + timedelta(days=30 * (i + 1))).date(),
            "balance_left": round(balance, 2)
        })
        payment_id += 1
loan_payments = pd.DataFrame(payment_rows)

# ---------- 7. TRANSACTIONS ----------
N_TXN = 300000
txn_types = ["Deposit", "Withdrawal", "Transfer", "Bill Payment"]
payment_modes = ["Cash", "UPI", "NEFT", "Cheque", "ATM"]
descriptions = ["Salary credit", "Grocery", "School fees", "Loan EMI", "Cash deposit",
                "ATM withdrawal", "Utility bill", "Fund transfer", "Medical expense", "Seed purchase"]
account_ids = accounts.account_id.values
employee_ids = employees.employee_id.values
txn_seconds = np.random.randint(0, 365 * YEARS * 86400, N_TXN)
txn_dates = [START + timedelta(seconds=int(s)) for s in txn_seconds]

transactions = pd.DataFrame({
    "transaction_id": range(1, N_TXN + 1),
    "account_id": np.random.choice(account_ids, N_TXN),
    "employee_id": np.random.choice(employee_ids, N_TXN),
    "transaction_type": np.random.choice(txn_types, N_TXN, p=[0.35, 0.3, 0.25, 0.1]),
    "amount": np.round(np.random.exponential(5000, N_TXN) + 100, 2),
    "payment_mode": np.random.choice(payment_modes, N_TXN),
    "transaction_date": txn_dates,
    "description": np.random.choice(descriptions, N_TXN)
})

# ---------- 8. FRAUD_ALERTS ----------
N_FRAUD = 150
fraud_txn_ids = np.random.choice(transactions.transaction_id, N_FRAUD, replace=False)
boost = np.random.uniform(5, 15, N_FRAUD)
transactions.loc[transactions.transaction_id.isin(fraud_txn_ids), "amount"] = (
    transactions.loc[transactions.transaction_id.isin(fraud_txn_ids), "amount"].values * boost
).round(2)

txn_date_map = transactions.set_index("transaction_id")["transaction_date"]
fraud_alerts = pd.DataFrame({
    "alert_id": range(1, N_FRAUD + 1),
    "transaction_id": fraud_txn_ids,
    "alert_type": np.random.choice(
        ["Unusual Amount", "Multiple Rapid Transactions", "Location Mismatch", "Duplicate Transaction"], N_FRAUD),
    "risk_score": np.round(np.random.uniform(0.5, 1.0, N_FRAUD), 2),
    "status": np.random.choice(["Under Review", "Confirmed Fraud", "False Positive"], N_FRAUD, p=[0.5, 0.2, 0.3]),
    "created_date": [txn_date_map.loc[t].date() for t in fraud_txn_ids]
})

# Ramesh's flagged incident — the story's fraud case
ramesh_account = accounts[accounts.customer_id == 1].account_id.values[0]
ramesh_txn = transactions[transactions.account_id == ramesh_account].transaction_id.values[0]
transactions.loc[transactions.transaction_id == ramesh_txn, "amount"] = 245000.00
transactions.loc[transactions.transaction_id == ramesh_txn, "description"] = "Suspicious large withdrawal"
new_alert = pd.DataFrame([{
    "alert_id": N_FRAUD + 1, "transaction_id": ramesh_txn,
    "alert_type": "Identity Mismatch - Loan Fraud Attempt", "risk_score": 0.98,
    "status": "Confirmed Fraud", "created_date": txn_date_map.loc[ramesh_txn].date()
}])
fraud_alerts = pd.concat([fraud_alerts, new_alert], ignore_index=True)

# ---------- Save ----------
import os
outdir = "./data"
os.makedirs(outdir, exist_ok=True)
for name, df in [("branches", branches), ("employees", employees), ("customers", customers),
                  ("accounts", accounts), ("loans", loans), ("loan_payments", loan_payments),
                  ("transactions", transactions), ("fraud_alerts", fraud_alerts)]:
    df.to_csv(f"{outdir}/{name}.csv", index=False)
    print(f"{name}: {len(df)} rows")

print("\nDone. Files saved to", outdir)
