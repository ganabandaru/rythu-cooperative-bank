-- ============================================================
-- Rythu Cooperative Bank — Database Schema
-- 8 tables, modeling a small-town cooperative bank's operations
-- ============================================================

CREATE TABLE branches (
    branch_id       INT PRIMARY KEY,
    branch_name     VARCHAR(100) NOT NULL,
    city            VARCHAR(50),
    address         VARCHAR(200),
    manager_name    VARCHAR(100)
);

CREATE TABLE employees (
    employee_id     INT PRIMARY KEY,
    branch_id       INT NOT NULL,
    name            VARCHAR(100) NOT NULL,
    role            VARCHAR(50),
    phone           VARCHAR(15),
    salary          DECIMAL(10,2),
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

CREATE TABLE customers (
    customer_id     INT PRIMARY KEY,
    aadhaar         VARCHAR(12) UNIQUE,
    pan             VARCHAR(10) UNIQUE,
    name            VARCHAR(100) NOT NULL,
    phone           VARCHAR(15),
    dob             DATE,
    address         VARCHAR(200),
    occupation      VARCHAR(50),
    branch_id       INT,
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

CREATE TABLE accounts (
    account_id      INT PRIMARY KEY,
    customer_id     INT NOT NULL,
    branch_id       INT NOT NULL,
    account_type    VARCHAR(20) CHECK (account_type IN ('Savings','Current')),
    balance         DECIMAL(12,2) DEFAULT 0,
    opened_date     DATE,
    status          VARCHAR(20) CHECK (status IN ('Active','Closed')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

CREATE TABLE loans (
    loan_id         INT PRIMARY KEY,
    customer_id     INT NOT NULL,
    branch_id       INT NOT NULL,
    staff_id        INT,                       -- references employees.employee_id
    loan_amount     DECIMAL(12,2),
    interest_rate   DECIMAL(5,2),
    duration_months INT,
    status          VARCHAR(20) CHECK (status IN ('Active','Closed','Defaulted')),
    disbursed_date  DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id),
    FOREIGN KEY (staff_id) REFERENCES employees(employee_id)
);

CREATE TABLE loan_payments (
    payment_id      INT PRIMARY KEY,
    loan_id         INT NOT NULL,
    amount          DECIMAL(10,2),
    payment_date    DATE,
    balance_left    DECIMAL(12,2),
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id)
);

CREATE TABLE transactions (
    transaction_id      INT PRIMARY KEY,
    account_id           INT NOT NULL,
    employee_id           INT,
    transaction_type      VARCHAR(20) CHECK (transaction_type IN ('Deposit','Withdrawal','Transfer','Bill Payment')),
    amount                 DECIMAL(12,2),
    payment_mode           VARCHAR(20),
    transaction_date       DATETIME,
    description             VARCHAR(200),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

CREATE TABLE fraud_alerts (
    alert_id        INT PRIMARY KEY,
    transaction_id  INT UNIQUE NOT NULL,      -- one transaction has at most one alert
    alert_type      VARCHAR(50),
    risk_score      DECIMAL(3,2),
    status          VARCHAR(20) CHECK (status IN ('Under Review','Confirmed Fraud','False Positive')),
    created_date    DATE,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);

-- ============================================================
-- Notes:
-- - loans.staff_id references employees.employee_id (naming mismatch
--   found and fixed manually during Power BI relationship setup —
--   auto-detect could not link these two columns automatically).
-- - branches -> loans relationship was initially missed during the
--   first schema pass and had to be added after model verification.
-- ============================================================
