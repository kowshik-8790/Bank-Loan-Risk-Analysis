-- ============================================================================
-- 05_portfolio_risk_segmentation.sql
-- Credit Grade Stratification, Good vs Bad Loans, and Loss Risk Tiers
-- ============================================================================

USE bank_loan_risk_db;

-- ----------------------------------------------------------------------------
-- 1. Good Loans vs Bad Loans Quality Ratio
-- ----------------------------------------------------------------------------
SELECT 
    f.loan_quality,
    COUNT(f.application_id)                         AS loan_count,
    ROUND((COUNT(f.application_id) * 100.0 / (SELECT COUNT(*) FROM fact_loans WHERE is_approved = 1)), 2) AS volume_share_pct,
    ROUND(SUM(f.funded_amount), 2)                  AS total_funded_capital,
    ROUND(SUM(f.total_payment), 2)                  AS total_cash_received,
    ROUND(AVG(f.interest_rate), 2)                  AS avg_interest_rate,
    ROUND(AVG(f.dti), 2)                            AS avg_dti,
    ROUND(SUM(f.net_loss_amount), 2)                AS total_credit_loss
FROM fact_loans f
WHERE f.is_approved = 1
GROUP BY f.loan_quality;

-- ----------------------------------------------------------------------------
-- 2. Risk Grade Stratification (A through F)
-- ----------------------------------------------------------------------------
SELECT 
    f.grade,
    COUNT(f.application_id)                         AS loans_funded,
    ROUND(SUM(f.funded_amount), 2)                  AS capital_deployed,
    ROUND(AVG(f.interest_rate), 2)                  AS weighted_avg_rate,
    ROUND(AVG(f.dti), 2)                            AS avg_dti,
    ROUND(AVG(f.fico_score), 1)                     AS avg_fico,
    SUM(f.is_default)                               AS charged_off_loans,
    ROUND((SUM(f.is_default) / COUNT(f.application_id)) * 100, 2) AS default_rate_pct,
    ROUND(SUM(f.net_loss_amount), 2)                AS realized_loss,
    ROUND((SUM(f.net_loss_amount) / SUM(f.funded_amount)) * 100, 2) AS capital_loss_rate_pct
FROM fact_loans f
WHERE f.is_approved = 1
GROUP BY f.grade
ORDER BY f.grade ASC;

-- ----------------------------------------------------------------------------
-- 3. Loan Amount Quartile Segmentation (NTILE)
-- ----------------------------------------------------------------------------
WITH loan_quartiles AS (
    SELECT 
        f.application_id,
        f.funded_amount,
        f.is_default,
        f.net_loss_amount,
        NTILE(4) OVER (ORDER BY f.funded_amount ASC) AS size_quartile
    FROM fact_loans f
    WHERE f.is_approved = 1
)
SELECT 
    size_quartile,
    COUNT(application_id)                           AS loan_count,
    MIN(funded_amount)                              AS min_loan_amount,
    MAX(funded_amount)                              AS max_loan_amount,
    ROUND(SUM(funded_amount), 2)                    AS total_funded,
    SUM(is_default)                                 AS total_defaults,
    ROUND((SUM(is_default) * 100.0 / COUNT(*)), 2)  AS default_rate_pct,
    ROUND(SUM(net_loss_amount), 2)                  AS total_loss
FROM loan_quartiles
GROUP BY size_quartile
ORDER BY size_quartile;
