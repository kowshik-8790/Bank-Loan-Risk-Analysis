-- ============================================================================
-- 02_data_cleaning_views.sql
-- Data Sanitization and Analytical Views in SQL
-- ============================================================================

USE bank_loan_risk_db;

-- 1. Deduplication script
DELETE l1 FROM fact_loans l1
INNER JOIN fact_loans l2 
WHERE l1.created_at > l2.created_at 
  AND l1.application_id = l2.application_id;

-- 2. Standardize whitespace and casing
UPDATE dim_borrowers
SET 
    employment_title = TRIM(employment_title),
    home_ownership   = UPPER(TRIM(home_ownership));

-- 3. Executive Portfolio View
CREATE OR REPLACE VIEW v_portfolio_executive_summary AS
SELECT 
    d.year,
    d.quarter,
    d.month,
    d.month_name,
    COUNT(f.application_id)                         AS total_applications,
    SUM(f.is_approved)                              AS approved_loans,
    COUNT(f.application_id) - SUM(f.is_approved)    AS rejected_loans,
    ROUND((SUM(f.is_approved) / COUNT(f.application_id)) * 100, 2) AS approval_rate_pct,
    ROUND(SUM(f.funded_amount), 2)                  AS total_capital_funded,
    ROUND(AVG(CASE WHEN f.is_approved = 1 THEN f.funded_amount END), 2) AS avg_funded_loan_amount,
    ROUND(SUM(f.total_payment), 2)                  AS total_cash_collected,
    ROUND(SUM(f.net_loss_amount), 2)                AS total_credit_loss,
    ROUND((SUM(f.is_default) / NULLIF(SUM(f.is_approved), 0)) * 100, 2) AS default_rate_pct
FROM fact_loans f
JOIN dim_date d ON f.issue_date = d.date_id
GROUP BY d.year, d.quarter, d.month, d.month_name;

-- 4. Credit Grade Risk Matrix View
CREATE OR REPLACE VIEW v_risk_grade_matrix AS
SELECT 
    f.grade,
    COUNT(f.application_id)                         AS total_loans,
    ROUND(SUM(f.funded_amount), 2)                  AS total_funded,
    ROUND(AVG(f.funded_amount), 2)                  AS avg_funded,
    ROUND(AVG(f.interest_rate), 2)                  AS avg_interest_rate,
    ROUND(AVG(f.dti), 2)                            AS avg_dti,
    ROUND(AVG(f.fico_score), 1)                     AS avg_fico,
    SUM(f.is_default)                               AS charged_off_loans,
    ROUND((SUM(f.is_default) / COUNT(f.application_id)) * 100, 2) AS default_rate_pct,
    ROUND(SUM(f.net_loss_amount), 2)                AS total_net_loss
FROM fact_loans f
WHERE f.is_approved = 1
GROUP BY f.grade;
