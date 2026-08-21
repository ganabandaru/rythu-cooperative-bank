-- ============================================================
-- Rythu Cooperative Bank — Sample Queries
-- ============================================================

-- 1. Investigate a single customer's full transaction history
--    (used to trace the Ramesh Naik case — the ₹2,45,000 flagged withdrawal)
SELECT t.transaction_id, t.amount, t.transaction_type,
       t.payment_mode, t.transaction_date, t.description
FROM transactions t
JOIN accounts a   ON t.account_id = a.account_id
JOIN customers c  ON a.customer_id = c.customer_id
WHERE c.name = 'Ramesh Naik'
ORDER BY t.transaction_date;


-- 2. Branch-wise active loan count
SELECT b.branch_name, COUNT(l.loan_id) AS active_loans
FROM branches b
JOIN loans l ON l.branch_id = b.branch_id
WHERE l.status = 'Active'
GROUP BY b.branch_name
ORDER BY active_loans DESC;


-- 3. Top 10 customers by total account balance
SELECT c.name, SUM(a.balance) AS total_balance
FROM customers c
JOIN accounts a ON a.customer_id = c.customer_id
GROUP BY c.name
ORDER BY total_balance DESC
LIMIT 10;


-- 4. Average transaction amount per branch (baseline for "normal" behavior)
SELECT b.branch_name, ROUND(AVG(t.amount), 2) AS avg_transaction_amount
FROM transactions t
JOIN accounts a  ON t.account_id = a.account_id
JOIN branches b  ON a.branch_id = b.branch_id
GROUP BY b.branch_name;


-- 5. All transactions currently flagged for fraud review
SELECT t.transaction_id, c.name, t.amount, t.transaction_date, f.alert_type, f.risk_score
FROM fraud_alerts f
JOIN transactions t ON f.transaction_id = t.transaction_id
JOIN accounts a      ON t.account_id = a.account_id
JOIN customers c     ON a.customer_id = c.customer_id
WHERE f.status = 'Under Review'
ORDER BY f.risk_score DESC;


-- 6. Loan default rate by branch
SELECT b.branch_name,
       COUNT(CASE WHEN l.status = 'Defaulted' THEN 1 END) * 100.0 / COUNT(*) AS default_rate_pct
FROM loans l
JOIN branches b ON l.branch_id = b.branch_id
GROUP BY b.branch_name
ORDER BY default_rate_pct DESC;
