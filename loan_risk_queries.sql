-- ====================================================================
-- Bank Loan Risk Analysis SQL Business KPI Queries
-- Author: Kasanaboina Kowshik (kasanaboinakowshik@gmail.com)
-- ====================================================================

USE bank_loan_risk_db;

-- 1. EXECUTIVE OVERALL LENDING KPIs
-- Total Loan Amount, Average Loan Amount, Total Applications, Approval & Rejection Rates
SELECT 
    COUNT(application_id) AS total_applications,
    ROUND(SUM(loan_amount), 2) AS total_portfolio_loan_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(applicant_income), 2) AS avg_applicant_income,
    ROUND(SUM(CASE WHEN loan_status = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS approval_rate_pct,
    ROUND(SUM(CASE WHEN loan_status = 'Rejected' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS rejection_rate_pct
FROM loan_applications;

-- 2. APPROVED VS REJECTED PORTFOLIO BREAKDOWN
SELECT 
    loan_status,
    COUNT(application_id) AS application_count,
    ROUND(SUM(loan_amount), 2) AS total_requested_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(credit_score), 1) AS avg_credit_score,
    ROUND(AVG(dti_ratio), 2) AS avg_dti_ratio,
    ROUND(AVG(applicant_income), 2) AS avg_annual_income
FROM loan_applications
GROUP BY loan_status;

-- 3. RISK GRADE PORTFOLIO DISTRIBUTION (Grades A through D/F)
SELECT 
    risk_grade,
    COUNT(application_id) AS total_applicants,
    ROUND(SUM(loan_amount), 2) AS total_funded_volume,
    ROUND(AVG(credit_score), 0) AS avg_credit_score,
    ROUND(AVG(dti_ratio), 1) AS avg_dti_ratio,
    ROUND(SUM(CASE WHEN loan_status = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS grade_approval_rate_pct
FROM loan_applications
GROUP BY risk_grade
ORDER BY avg_credit_score DESC;

-- 4. LENDING PERFORMANCE BY LOAN PURPOSE
SELECT 
    loan_purpose,
    COUNT(application_id) AS total_applications,
    ROUND(SUM(loan_amount), 2) AS total_loan_volume,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(SUM(CASE WHEN loan_status = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS approval_rate_pct
FROM loan_applications
GROUP BY loan_purpose
ORDER BY total_loan_volume DESC;

-- 5. DEBT-TO-INCOME (DTI) STRESS BRACKET ANALYSIS
SELECT 
    CASE 
        WHEN dti_ratio < 20 THEN 'Low DTI (< 20%)'
        WHEN dti_ratio BETWEEN 20 AND 35 THEN 'Healthy DTI (20% - 35%)'
        WHEN dti_ratio BETWEEN 35 AND 43 THEN 'High DTI (35% - 43%)'
        ELSE 'Severe DTI (> 43%)'
    END AS dti_bracket,
    COUNT(application_id) AS applicants,
    ROUND(AVG(applicant_income), 2) AS avg_income,
    ROUND(SUM(CASE WHEN loan_status = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS approval_rate_pct
FROM loan_applications
GROUP BY dti_bracket
ORDER BY approval_rate_pct DESC;

-- 6. EMPLOYMENT STABILITY & CREDIT RISK CORRELATION
SELECT 
    CASE 
        WHEN employment_length_years >= 10 THEN '10+ Years (Tenured)'
        WHEN employment_length_years >= 5 THEN '5 - 9 Years (Established)'
        WHEN employment_length_years >= 2 THEN '2 - 4 Years (Intermediate)'
        ELSE '< 2 Years (Entry)'
    END AS employment_tenure,
    COUNT(application_id) AS applicant_count,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(credit_score), 0) AS avg_fico_score,
    ROUND(SUM(CASE WHEN loan_status = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS approval_rate_pct
FROM loan_applications
GROUP BY employment_tenure
ORDER BY approval_rate_pct DESC;
