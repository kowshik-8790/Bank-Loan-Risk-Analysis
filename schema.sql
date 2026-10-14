-- ====================================================================
-- Bank Loan Risk Analysis & Portfolio Database Schema
-- Author: Kasanaboina Kowshik (kasanaboinakowshik@gmail.com)
-- Database: MySQL 8.0+ / MariaDB / Compatible RDBMS
-- ====================================================================

CREATE DATABASE IF NOT EXISTS bank_loan_risk_db;
USE bank_loan_risk_db;

DROP TABLE IF EXISTS loan_applications;

CREATE TABLE loan_applications (
    application_id VARCHAR(20) PRIMARY KEY,
    applicant_income DECIMAL(12, 2) NOT NULL,
    loan_amount DECIMAL(12, 2) NOT NULL,
    credit_score INT NOT NULL,
    dti_ratio DECIMAL(5, 2) NOT NULL,
    employment_length_years INT NOT NULL,
    loan_purpose VARCHAR(50) NOT NULL,
    loan_status VARCHAR(20) NOT NULL, -- 'Approved' or 'Rejected'
    risk_grade VARCHAR(30) NOT NULL,   -- 'Grade A (Low Risk)', 'Grade B', etc.
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_loan_status (loan_status),
    INDEX idx_risk_grade (risk_grade),
    INDEX idx_credit_score (credit_score),
    INDEX idx_loan_purpose (loan_purpose)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
