-- ============================================================================
-- 01_schema_setup.sql
-- Star Schema Database Architecture for Bank Loan Risk Analytics
-- Compatible with MySQL 8.0+
-- ============================================================================

CREATE DATABASE IF NOT EXISTS bank_loan_risk_db
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE bank_loan_risk_db;

-- Drop tables in order of dependency if re-creating
DROP TABLE IF EXISTS fact_loans;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_geography;
DROP TABLE IF EXISTS dim_borrowers;

-- 1. Dimension: Borrowers
CREATE TABLE dim_borrowers (
    borrower_id         VARCHAR(30) PRIMARY KEY,
    employment_title    VARCHAR(120) NOT NULL,
    employment_length   VARCHAR(50)  NOT NULL DEFAULT '3-5 years',
    home_ownership      VARCHAR(50)  NOT NULL,
    annual_income       DECIMAL(12, 2) NOT NULL,
    fico_score          INT NOT NULL,
    delinq_2yrs         INT NOT NULL DEFAULT 0,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_borrower_fico (fico_score),
    INDEX idx_borrower_home (home_ownership),
    INDEX idx_borrower_emp (employment_length)
) ENGINE=InnoDB;

-- 2. Dimension: Geography
CREATE TABLE dim_geography (
    state_code          VARCHAR(10) PRIMARY KEY,
    state_name          VARCHAR(100) NOT NULL,
    region              VARCHAR(50)  NOT NULL,
    INDEX idx_geo_region (region)
) ENGINE=InnoDB;

-- 3. Dimension: Calendar Date
CREATE TABLE dim_date (
    date_id             DATE PRIMARY KEY,
    year                INT NOT NULL,
    quarter             VARCHAR(5) NOT NULL,
    month               INT NOT NULL,
    month_name          VARCHAR(20) NOT NULL,
    month_year          VARCHAR(20) NOT NULL,
    day                 INT NOT NULL,
    INDEX idx_date_ym (year, month)
) ENGINE=InnoDB;

-- 4. Fact: Loan Applications & Risk Performance
CREATE TABLE fact_loans (
    application_id      VARCHAR(30) PRIMARY KEY,
    borrower_id         VARCHAR(30) NOT NULL,
    issue_date          DATE NOT NULL,
    state_code          VARCHAR(10) NOT NULL,
    grade               VARCHAR(5)  NOT NULL,
    sub_grade           VARCHAR(10) NOT NULL,
    term                VARCHAR(30) NOT NULL,
    loan_purpose        VARCHAR(60) NOT NULL,
    verification_status VARCHAR(40) NOT NULL,
    loan_amount         DECIMAL(12, 2) NOT NULL,
    funded_amount       DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    interest_rate       DECIMAL(6, 2)  NOT NULL,
    installment         DECIMAL(10, 2) NOT NULL,
    dti                 DECIMAL(6, 2)  NOT NULL,
    dti_band            VARCHAR(30) NOT NULL,
    fico_score          INT NOT NULL,
    fico_band           VARCHAR(30) NOT NULL,
    loan_status         VARCHAR(50) NOT NULL,
    is_approved         TINYINT(1)  NOT NULL DEFAULT 0,
    is_default          TINYINT(1)  NOT NULL DEFAULT 0,
    loan_quality        VARCHAR(40) NOT NULL,
    total_payment       DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    recovery_amount     DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    net_loss_amount     DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Foreign Key Constraints
    CONSTRAINT fk_loan_borrower FOREIGN KEY (borrower_id)
        REFERENCES dim_borrowers(borrower_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_loan_geo FOREIGN KEY (state_code)
        REFERENCES dim_geography(state_code) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_loan_date FOREIGN KEY (issue_date)
        REFERENCES dim_date(date_id) ON DELETE RESTRICT ON UPDATE CASCADE,

    -- Analytical Indexes
    INDEX idx_loan_status (loan_status),
    INDEX idx_loan_grade (grade),
    INDEX idx_loan_purpose (loan_purpose),
    INDEX idx_loan_approval (is_approved),
    INDEX idx_loan_default (is_default)
) ENGINE=InnoDB;
