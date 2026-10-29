-- ============================================================================
-- 04_demographic_underwriting.sql
-- Borrower Demographics, Employment Length, Home Ownership & Loan Purpose
-- ============================================================================

USE bank_loan_risk_db;

-- ----------------------------------------------------------------------------
-- 1. Home Ownership vs Credit Risk (Mortgage vs Rent vs Own)
-- ----------------------------------------------------------------------------
SELECT 
    b.home_ownership,
    COUNT(f.application_id)                         AS total_applications,
    SUM(f.is_approved)                              AS approved_loans,
    ROUND((SUM(f.is_approved) / COUNT(f.application_id)) * 100, 2) AS approval_rate_pct,
    ROUND(SUM(f.funded_amount), 2)                  AS total_funded_capital,
    ROUND(AVG(b.annual_income), 2)                  AS avg_annual_income,
    ROUND(AVG(f.dti), 2)                            AS avg_dti,
    ROUND(AVG(b.fico_score), 1)                     AS avg_fico,
    SUM(f.is_default)                               AS total_defaults,
    ROUND((SUM(f.is_default) / NULLIF(SUM(f.is_approved), 0)) * 100, 2) AS default_rate_pct
FROM fact_loans f
JOIN dim_borrowers b ON f.borrower_id = b.borrower_id
GROUP BY b.home_ownership
ORDER BY total_funded_capital DESC;

-- ----------------------------------------------------------------------------
-- 2. Employment Stability vs Default Likelihood
-- ----------------------------------------------------------------------------
SELECT 
    b.employment_length,
    COUNT(f.application_id)                         AS applications,
    ROUND(SUM(f.funded_amount), 2)                  AS funded_amount,
    ROUND(AVG(b.annual_income), 2)                  AS avg_income,
    ROUND(AVG(b.fico_score), 1)                     AS avg_fico,
    SUM(f.is_default)                               AS charged_off_count,
    ROUND((SUM(f.is_default) / COUNT(f.application_id)) * 100, 2) AS default_rate_pct
FROM fact_loans f
JOIN dim_borrowers b ON f.borrower_id = b.borrower_id
WHERE f.is_approved = 1
GROUP BY b.employment_length
ORDER BY default_rate_pct ASC;

-- ----------------------------------------------------------------------------
-- 3. Loan Purpose Risk & Volume Breakdown
-- ----------------------------------------------------------------------------
SELECT 
    f.loan_purpose,
    COUNT(f.application_id)                         AS approved_loans,
    ROUND(SUM(f.funded_amount), 2)                  AS total_capital_funded,
    ROUND(AVG(f.funded_amount), 2)                  AS avg_loan_size,
    ROUND(AVG(f.interest_rate), 2)                  AS avg_interest_rate,
    SUM(f.is_default)                               AS defaults_count,
    ROUND((SUM(f.is_default) / COUNT(f.application_id)) * 100, 2) AS default_rate_pct,
    ROUND(SUM(f.net_loss_amount), 2)                AS net_credit_loss
FROM fact_loans f
WHERE f.is_approved = 1
GROUP BY f.loan_purpose
ORDER BY total_capital_funded DESC;
