"""
Raw Bank Loan Data Generator
Generates realistic enterprise lending applications with credit attributes,
underwriting outcomes (Approved, Rejected, Fully Paid, Charged Off),
and intentional data quirks for end-to-end cleaning and risk analytics.
"""

import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

np.random.seed(42)
random.seed(42)

TOTAL_APPLICATIONS = 10000

STATES = [
    ("CA", "California", "West"), ("NY", "New York", "East"),
    ("TX", "Texas", "South"), ("FL", "Florida", "South"),
    ("IL", "Illinois", "Midwest"), ("PA", "Pennsylvania", "East"),
    ("OH", "Ohio", "Midwest"), ("GA", "Georgia", "South"),
    ("NC", "North Carolina", "South"), ("WA", "Washington", "West"),
    ("CO", "Colorado", "West"), ("AZ", "Arizona", "West"),
    ("MA", "Massachusetts", "East"), ("VA", "Virginia", "South")
]

JOB_TITLES = [
    "Software Engineer", "Registered Nurse", "Operations Manager", "Teacher",
    "Sales Executive", "Financial Analyst", "Accountant", "Project Manager",
    "Electrician", "Administrative Assistant", "Pharmacist", "Marketing Specialist",
    "Police Officer", "Store Manager", "Truck Driver", "Mechanical Engineer"
]

PURPOSES = [
    "debt_consolidation", "credit_card", "home_improvement",
    "small_business", "major_purchase", "medical", "car"
]

HOME_OWNERSHIP = ["MORTGAGE", "RENT", "OWN"]
EMP_LENGTHS = ["< 1 year", "1-2 years", "3-5 years", "6-9 years", "10+ years"]
VERIFICATION_STATUSES = ["Verified", "Source Verified", "Not Verified"]
TERMS = ["36 months", "60 months"]

GRADES_CONFIG = {
    "A": {"int_min": 5.3, "int_max": 9.5, "fico_min": 750, "fico_max": 850, "default_risk": 0.04},
    "B": {"int_min": 9.6, "int_max": 13.5, "fico_min": 700, "fico_max": 760, "default_risk": 0.09},
    "C": {"int_min": 13.6, "int_max": 17.5, "fico_min": 660, "fico_max": 710, "default_risk": 0.16},
    "D": {"int_min": 17.6, "int_max": 21.5, "fico_min": 630, "fico_max": 670, "default_risk": 0.24},
    "E": {"int_min": 21.6, "int_max": 25.5, "fico_min": 600, "fico_max": 640, "default_risk": 0.33},
    "F": {"int_min": 25.6, "int_max": 29.5, "fico_min": 580, "fico_max": 615, "default_risk": 0.42},
}


def generate_loan_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)

    start_date = datetime(2022, 1, 1)
    end_date = datetime(2025, 12, 31)
    days_range = (end_date - start_date).days

    records = []
    for i in range(1, TOTAL_APPLICATIONS + 1):
        app_id = f"LN-{200000 + i}"
        borrower_id = f"BORR-{10000 + (i % 3500)}"

        # Date
        issue_dt = start_date + timedelta(days=random.randint(0, days_range))

        # Risk Grade distribution
        grade = np.random.choice(["A", "B", "C", "D", "E", "F"], p=[0.22, 0.30, 0.24, 0.14, 0.07, 0.03])
        sub_grade = f"{grade}{random.randint(1, 5)}"
        g_cfg = GRADES_CONFIG[grade]

        # Financial parameters
        loan_amount = float(random.choice([
            5000, 7500, 10000, 12000, 15000, 18000, 20000, 25000, 30000, 35000, 40000
        ]))
        int_rate = round(float(random.uniform(g_cfg["int_min"], g_cfg["int_max"])), 2)
        term = random.choice(TERMS)
        months = 36 if "36" in term else 60

        # Amortization monthly installment formula
        r = (int_rate / 100.0) / 12.0
        installment = round(float(loan_amount * (r * (1 + r)**months) / ((1 + r)**months - 1)), 2)

        # Borrower demographics
        annual_income = round(float(np.random.lognormal(mean=11.1, sigma=0.45)), -2)
        annual_income = float(np.clip(annual_income, 24000.0, 300000.0))

        fico_score = random.randint(g_cfg["fico_min"], g_cfg["fico_max"])
        dti = round(float(random.uniform(6.0, 38.0)), 2)
        # Higher DTI for lower grades
        if grade in ["D", "E", "F"]:
            dti = round(min(dti + random.uniform(4.0, 12.0), 45.0), 2)

        emp_title = random.choice(JOB_TITLES)
        emp_length = random.choice(EMP_LENGTHS)
        home_ownership = random.choice(HOME_OWNERSHIP)
        verification_status = random.choice(VERIFICATION_STATUSES)
        purpose = random.choice(PURPOSES)
        state_info = random.choice(STATES)
        delinq_2yrs = int(np.random.choice([0, 1, 2, 3], p=[0.82, 0.12, 0.04, 0.02]))

        # Underwriting Decision logic (Approval vs Rejection)
        # Rejection occurs when DTI > 36% and FICO < 620, or FICO < 600
        is_rejected = (dti > 36.0 and fico_score < 630) or (fico_score < 590 and random.random() < 0.75)

        if is_rejected:
            loan_status = "Rejected"
            funded_amount = 0.0
            total_payment = 0.0
            recovery_amount = 0.0
        else:
            # Approved Loan Outcome (Fully Paid, Current, Charged Off)
            funded_amount = loan_amount
            outcome_roll = random.random()

            if outcome_roll < g_cfg["default_risk"]:
                loan_status = "Charged Off"
                # Charged off recovered partial principal
                months_paid = random.randint(3, 14)
                total_payment = round(months_paid * installment, 2)
                recovery_amount = round(random.uniform(200.0, 1800.0), 2)
            elif outcome_roll < (g_cfg["default_risk"] + 0.55):
                loan_status = "Fully Paid"
                total_payment = round(installment * months, 2)
                recovery_amount = 0.0
            else:
                loan_status = "Current"
                months_active = random.randint(6, 24)
                total_payment = round(months_active * installment, 2)
                recovery_amount = 0.0

        # Inject realistic data quirks for Python/Excel cleaning demo
        date_format_roll = random.random()
        if date_format_roll < 0.70:
            date_str = issue_dt.strftime("%Y-%m-%d")
        elif date_format_roll < 0.85:
            date_str = issue_dt.strftime("%m/%d/%Y")
        else:
            date_str = issue_dt.strftime("%d-%m-%Y")

        # Dirty currency strings in 4% of rows
        loan_amount_val = loan_amount
        if random.random() < 0.04:
            loan_amount_val = f"${loan_amount:,.2f}"

        # Dirty interest rate string with %
        int_rate_val = int_rate
        if random.random() < 0.05:
            int_rate_val = f"{int_rate}%"

        # Missing employment length or DTI in 2% of rows
        if random.random() < 0.025:
            emp_length = None
        if random.random() < 0.02:
            dti = None

        # Casing inconsistency
        if random.random() < 0.05:
            home_ownership = home_ownership.lower()

        # Whitespace quirks in job title
        if random.random() < 0.04:
            emp_title = f"  {emp_title}  "

        records.append({
            "Application_ID": app_id,
            "Borrower_ID": borrower_id,
            "Issue_Date": date_str,
            "Term": term,
            "Loan_Amount": loan_amount_val,
            "Funded_Amount": funded_amount,
            "Interest_Rate": int_rate_val,
            "Installment": installment,
            "Grade": grade,
            "Sub_Grade": sub_grade,
            "Employment_Title": emp_title,
            "Employment_Length": emp_length,
            "Home_Ownership": home_ownership,
            "Annual_Income": annual_income,
            "Verification_Status": verification_status,
            "Loan_Purpose": purpose,
            "State_Code": state_info[0],
            "State_Name": state_info[1],
            "Region": state_info[2],
            "DTI": dti,
            "FICO_Score": fico_score,
            "Delinq_2Yrs": delinq_2yrs,
            "Loan_Status": loan_status,
            "Total_Payment": total_payment,
            "Recovery_Amount": recovery_amount
        })

    df = pd.DataFrame(records)

    # Inject 45 duplicate applications to mimic enterprise batch replay
    dup_sample = df.sample(n=45, random_state=42)
    df = pd.concat([df, dup_sample], ignore_index=True)

    csv_path = os.path.join(raw_dir, "bank_loan_raw_applications.csv")
    df.to_csv(csv_path, index=False)
    print(f"Generated raw loan applications CSV: {csv_path} ({len(df)} records)")

    # Save Excel sample
    excel_path = os.path.join(raw_dir, "bank_loan_raw_sample.xlsx")
    df.head(2500).to_excel(excel_path, sheet_name="Raw_Loan_Apps", index=False)
    print(f"Generated sample Excel: {excel_path} (2500 records)")

    return csv_path


if __name__ == "__main__":
    generate_loan_data()
