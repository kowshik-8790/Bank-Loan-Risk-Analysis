"""
Bank Loan Database Connector & Standalone SQL Execution Engine
Populates SQLite embedded database and connects to MySQL 8.0+ for analytics.
"""

import os
import sys
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

DEFAULT_MYSQL_URL = os.getenv(
    "MYSQL_URI", "mysql+pymysql://root:password@localhost:3306/bank_loan_risk_db"
)


def get_base_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_processed_data_to_sqlite():
    base_dir = get_base_dir()
    db_path = os.path.join(base_dir, "data", "loan_risk_analytics.db")
    proc_dir = os.path.join(base_dir, "data", "processed")

    print(f"Initializing local SQLite database at: {db_path}")
    conn = sqlite3.connect(db_path)

    tables = {
        "dim_borrowers": "dim_borrowers.csv",
        "dim_geography": "dim_geography.csv",
        "dim_date": "dim_date.csv",
        "fact_loans": "clean_fact_loans.csv",
    }

    for tbl_name, filename in tables.items():
        file_path = os.path.join(proc_dir, filename)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df.to_sql(tbl_name, conn, if_exists="replace", index=False)
            print(f"  [OK] Loaded {len(df):,} rows into '{tbl_name}'")
        else:
            print(f"  [WARN] File not found: {file_path}")

    conn.close()
    print("Database sync complete.\n")
    return db_path


def run_sample_kpis(db_path):
    conn = sqlite3.connect(db_path)

    print("=" * 70)
    print("         EXECUTIVE BANK LOAN RISK KPI REPORT (SQL ENGINE)")
    print("=" * 70)

    # 1. High-Level KPIs
    q1 = """
    SELECT 
        COUNT(f.application_id) AS applications,
        SUM(f.is_approved) AS approved,
        ROUND((SUM(f.is_approved) * 100.0 / COUNT(f.application_id)), 2) AS approval_rate_pct,
        ROUND(SUM(f.funded_amount), 2) AS total_funded,
        ROUND(AVG(CASE WHEN f.is_approved = 1 THEN f.funded_amount END), 2) AS avg_funded,
        ROUND(AVG(b.annual_income), 2) AS avg_applicant_income,
        ROUND(AVG(f.dti), 2) AS avg_dti,
        ROUND((SUM(f.is_default) * 100.0 / SUM(f.is_approved)), 2) AS default_rate_pct
    FROM fact_loans f
    JOIN dim_borrowers b ON f.borrower_id = b.borrower_id;
    """
    res1 = pd.read_sql_query(q1, conn)
    print("\n--- 1. OVERALL LENDING PORTFOLIO KPIS ---")
    print(res1.to_string(index=False))

    # 2. Risk Grade Breakdown
    q2 = """
    SELECT 
        grade,
        COUNT(application_id) AS loans,
        ROUND(SUM(funded_amount), 2) AS funded,
        ROUND(AVG(interest_rate), 2) AS avg_rate,
        ROUND(AVG(fico_score), 1) AS avg_fico,
        SUM(is_default) AS defaults,
        ROUND((SUM(is_default) * 100.0 / COUNT(application_id)), 2) AS default_rate_pct
    FROM fact_loans
    WHERE is_approved = 1
    GROUP BY grade
    ORDER BY grade ASC;
    """
    res2 = pd.read_sql_query(q2, conn)
    print("\n--- 2. RISK GRADE STRATIFICATION (A - F) ---")
    print(res2.to_string(index=False))

    # 3. Purpose Breakdown
    q3 = """
    SELECT 
        loan_purpose,
        COUNT(application_id) AS loans,
        ROUND(SUM(funded_amount), 2) AS funded,
        SUM(is_default) AS defaults,
        ROUND((SUM(is_default) * 100.0 / COUNT(application_id)), 2) AS default_rate_pct
    FROM fact_loans
    WHERE is_approved = 1
    GROUP BY loan_purpose
    ORDER BY funded DESC
    LIMIT 5;
    """
    res3 = pd.read_sql_query(q3, conn)
    print("\n--- 3. TOP 5 LOAN PURPOSES & DEFAULT RATES ---")
    print(res3.to_string(index=False))

    conn.close()
    print("\n" + "=" * 70)


def load_to_mysql(connection_uri=DEFAULT_MYSQL_URL):
    try:
        engine = create_engine(connection_uri)
        with engine.connect() as conn:
            print(f"Connected to MySQL successfully at {connection_uri}")
            base_dir = get_base_dir()
            proc_dir = os.path.join(base_dir, "data", "processed")

            for tbl, fname in [
                ("dim_borrowers", "dim_borrowers.csv"),
                ("dim_geography", "dim_geography.csv"),
                ("dim_date", "dim_date.csv"),
                ("fact_loans", "clean_fact_loans.csv"),
            ]:
                df = pd.read_csv(os.path.join(proc_dir, fname))
                df.to_sql(tbl, engine, if_exists="append", index=False)
                print(f"  [OK] Exported {len(df):,} rows to MySQL table `{tbl}`")
    except Exception as e:
        print(f"Note: MySQL live connection not established ({e}).")
        print("Using local standalone database engine for all SQL analyses.")


if __name__ == "__main__":
    db_file = load_processed_data_to_sqlite()
    run_sample_kpis(db_file)
    if len(sys.argv) > 1 and sys.argv[1] == "--mysql":
        load_to_mysql()
