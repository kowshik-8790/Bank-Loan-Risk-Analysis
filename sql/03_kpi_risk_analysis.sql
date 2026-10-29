-- ============================================================================
-- 03_kpi_risk_analysis.sql
-- Core Lending KPIs: Approval Rate, Rejection Rate, Capital Funded, DTI, MoM Growth
-- ============================================================================

USE bank_loan_risk_db;

-- ----------------------------------------------------------------------------
-- KPI 1: Overall Lending Portfolio Health Summary
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(f.application_id)                                         AS total_applications,
    SUM(f.is_approved)                                              AS total_approved_loans,
    COUNT(f.application_id) - SUM(f.is_approved)                    AS total_rejected_applications,
    ROUND((SUM(f.is_approved) / COUNT(f.application_id)) * 100, 2) AS approval_rate_pct,
    ROUND(((COUNT(f.application_id) - SUM(f.is_approved)) / COUNT(f.application_id)) * 100, 2) AS rejection_rate_pct,
    ROUND(SUM(f.funded_amount), 2)                                  AS total_funded_capital,
    ROUND(AVG(CASE WHEN f.is_approved = 1 THEN f.funded_amount END), 2) AS avg_loan_amount,
    ROUND(SUM(f.total_payment), 2)                                  AS total_cash_collected,
    ROUND(AVG(b.annual_income), 2)                                  AS avg_applicant_income,
    ROUND(AVG(f.dti), 2)                                            AS avg_dti_pct,
    ROUND(AVG(f.fico_score), 1)                                     AS avg_fico_score,
    ROUND((SUM(f.is_default) / NULLIF(SUM(f.is_approved), 0)) * 100, 2) AS portfolio_default_rate_pct,
    ROUND(SUM(f.net_loss_amount), 2)                                AS total_credit_loss
FROM fact_loans f
JOIN dim_borrowers b ON f.borrower_id = b.borrower_id;

-- ----------------------------------------------------------------------------
-- KPI 2: Monthly Lending Trends with MoM Growth (Window Function: LAG)
-- ----------------------------------------------------------------------------
WITH monthly_lending AS (
    SELECT 
        d.year,
        d.month,
        d.month_year,
        COUNT(f.application_id)             AS applications_count,
        SUM(f.is_approved)                  AS approved_count,
        ROUND(SUM(f.funded_amount), 2)      AS monthly_funded_amount,
        ROUND(SUM(f.total_payment), 2)      AS monthly_cash_collected,
        SUM(f.is_default)                   AS defaults_count
    FROM fact_loans f
    JOIN dim_date d ON f.issue_date = d.date_id
    GROUP BY d.year, d.month, d.month_year
)
SELECT 
    year,
    month,
    month_year,
    applications_count,
    approved_count,
    monthly_funded_amount,
    LAG(monthly_funded_amount, 1) OVER (ORDER BY year, month) AS prev_month_funded,
    ROUND(
        ((monthly_funded_amount - LAG(monthly_funded_amount, 1) OVER (ORDER BY year, month))
         / NULLIF(LAG(monthly_funded_amount, 1) OVER (ORDER BY year, month), 0)) * 100,
        2
    ) AS mom_funded_growth_pct,
    monthly_cash_collected,
    defaults_count,
    ROUND((defaults_count / NULLIF(approved_count, 0)) * 100, 2) AS monthly_default_rate_pct
FROM monthly_lending
ORDER BY year, month;

-- ----------------------------------------------------------------------------
-- KPI 3: Debt-to-Income (DTI) Band Risk Impact
-- Demonstrates sharp credit degradation when DTI exceeds 25%
-- ----------------------------------------------------------------------------
SELECT 
    f.dti_band,
    COUNT(f.application_id)                         AS total_loans,
    ROUND(SUM(f.funded_amount), 2)                  AS total_funded,
    ROUND(AVG(f.funded_amount), 2)                  AS avg_loan,
    ROUND(AVG(b.annual_income), 2)                  AS avg_income,
    ROUND(AVG(f.fico_score), 1)                     AS avg_fico,
    SUM(f.is_default)                               AS default_count,
    ROUND((SUM(f.is_default) / COUNT(f.application_id)) * 100, 2) AS default_rate_pct,
    ROUND(SUM(f.net_loss_amount), 2)                AS net_credit_loss
FROM fact_loans f
JOIN dim_borrowers b ON f.borrower_id = b.borrower_id
WHERE f.is_approved = 1
GROUP BY f.dti_band
ORDER BY default_rate_pct ASC;
