# Rythu Cooperative Bank — End-to-End Data Analytics & AI Project

A story-driven, end-to-end data project: a fictional small-town cooperative bank's
digital transformation, built one real layer at a time — **SQL → Python → Power BI → Machine Learning → GenAI/Agentic AI**.

> Two friends, a coffee shop, and a bank still running on paper registers.
> Every table, dashboard, and model in this project exists because the
> story needed it — not because a syllabus listed it.

---

## 📊 Project Scale

| Table | Records |
|---|---|
| Branches | 5 |
| Employees | 40 |
| Customers | 2,000 |
| Accounts | 2,496 |
| Loans | 400 |
| Loan Payments | 2,434 |
| Transactions | 300,000 |
| Fraud Alerts | 151 |
| **Total** | **305,526** |

## 🧱 Tech Stack & Status

| Phase | Tools | Status |
|---|---|---|
| SQL & Data Modeling | MySQL, joins, CTEs, window functions, constraints, indexing | ✅ Complete |
| Python & Data Engineering | Python, Pandas, NumPy, Matplotlib, Seaborn | ✅ Complete |
| Power BI | Power Query, Data Modeling, DAX | ⚡ In Progress |
| Machine Learning | Scikit-learn — fraud detection, loan default prediction | ⭕ Planned |
| GenAI / Agentic AI | RAG, text-to-SQL, multi-agent orchestration | ⭕ Planned |
| Deployment | Power BI Service, GitHub Pages, cloud exploration | ⭕ Planned |

## 📁 Repository Structure

```
rythu-cooperative-bank/
├── sql/
│   ├── schema.sql          -- CREATE TABLE statements, all 8 tables
│   └── sample_queries.sql  -- investigation & business queries
├── python/
│   └── generate_data.py    -- synthetic data generator (305,526 records)
├── data/                   -- sample CSVs (see note below)
├── powerbi/                -- .pbix file (added once dashboard is complete)
└── README.md
```

## 🗄️ Data Model

8 tables, 10 relationships, all one-to-many:

```
branches ──< employees
branches ──< accounts
branches ──< loans
customers ──< accounts
customers ──< loans
accounts ──< transactions
employees ──< transactions
employees ──< loans (staff_id → employee_id)
loans ──< loan_payments
transactions ──< fraud_alerts (0 or 1)
```

Two relationship bugs were found and fixed manually during modeling —
a missing `branches → loans` link, and a silent `loans.staff_id` /
`employees.employee_id` naming mismatch that Power BI's autodetect
couldn't catch on its own.

## 🕵️ The Story So Far

A customer, Ramesh Naik, disputes a ₹2,45,000 withdrawal. SQL traces
his full transaction history and isolates the one transaction that
breaks his normal pattern. The follow-up question — *is this the only
one?* — can't be answered by hand across 300,000+ transactions, so the
investigation moves into Python: `pandas`, `mean()`/`std()`, and a
Seaborn distribution plot surface 150+ transactions that don't fit the
expected pattern. That gap — a one-time manual check vs. a system that
watches continuously — is what the Machine Learning phase is built to close.

## 🚀 Running the Data Generator

```bash
pip install pandas numpy
python python/generate_data.py
```

Outputs 8 CSV files to `./data`, matching the counts in the table above.
No external APIs or libraries like Faker are required — names, cities,
and addresses are generated from hand-built Telangana-region pools.

## 🔗 Links

- **Portfolio / Case Study:** _(add your GitHub Pages link here)_
- **LinkedIn build-in-public series:** _(add your LinkedIn post links here)_

---

*Built by Ganapathi Bandaru — updated as each phase completes.*
