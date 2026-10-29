"""
Bank Loan ETL Pipeline & Risk Feature Engineering
Cleans raw loan application data using Python, Pandas, and NumPy,
applies banking credit risk transformations, produces Star-Schema dimensions,
and exports clean datasets for MySQL, Power BI, and Excel.
"""

import os
import numpy as np
import pandas as pd


def clean_currency(val):
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    val_str = str(val).replace("$", "").replace(",", "").strip()
    try:
        return float(val_str)
    except ValueError:
        return 0.0


def clean_percentage(val):
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    val_str = str(val).replace("%", "").strip()
    try:
        return float(val_str)
    except ValueError:
        return 0.0


def parse_mixed_dates(series):
    return pd.to_datetime(series, format="mixed", dayfirst=False, errors="coerce")


def run_loan_etl():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw", "bank_loan_raw_applications.csv")
    proc_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(proc_dir, exist_ok=True)

    print("Step 1: Loading raw loan applications...")
    df = pd.read_csv(raw_path)
    initial_count = len(df)
    print(f"Loaded {initial_count:,} raw applications.")

    print("\nStep 2: Deduplication...")
    df = df.drop_duplicates(subset=["Application_ID"], keep="first")
    print(f"Dropped {initial_count - len(df)} duplicate records. Unique applications: {len(df):,}")

    print("\nStep 3: Text & String Sanitization...")
    text_cols = [
        "Employment_Title", "Employment_Length", "Home_Ownership", "Verification_Status",
        "Loan_Purpose", "State_Code", "State_Name", "Region", "Loan_Status", "Grade", "Sub_Grade", "Term"
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df["Home_Ownership"] = df["Home_Ownership"].str.upper()
    df["Home_Ownership"] = df["Home_Ownership"].replace({"NONE": "OTHER", "ANY": "OTHER", "NAN": "RENT"})

    print("\nStep 4: Imputing Missing Values...")
    df["Employment_Length"] = df["Employment_Length"].replace(["nan", "None", ""], "3-5 years").fillna("3-5 years")
    median_dti = df["DTI"].median()
    df["DTI"] = df["DTI"].fillna(median_dti)

    print("\nStep 5: Numeric & Currency Parsing...")
    df["Loan_Amount"] = df["Loan_Amount"].apply(clean_currency)
    df["Funded_Amount"] = df["Funded_Amount"].apply(clean_currency)
    df["Interest_Rate"] = df["Interest_Rate"].apply(clean_percentage)
    df["Installment"] = pd.to_numeric(df["Installment"], errors="coerce").fillna(0.0)
    df["Annual_Income"] = pd.to_numeric(df["Annual_Income"], errors="coerce").fillna(50000.0)
    df["DTI"] = pd.to_numeric(df["DTI"], errors="coerce").fillna(median_dti)
    df["FICO_Score"] = pd.to_numeric(df["FICO_Score"], errors="coerce").fillna(680).astype(int)
    df["Delinq_2Yrs"] = pd.to_numeric(df["Delinq_2Yrs"], errors="coerce").fillna(0).astype(int)
    df["Total_Payment"] = pd.to_numeric(df["Total_Payment"], errors="coerce").fillna(0.0)
    df["Recovery_Amount"] = pd.to_numeric(df["Recovery_Amount"], errors="coerce").fillna(0.0)

    print("\nStep 6: Date Parsing & Validation...")
    df["Issue_Date"] = parse_mixed_dates(df["Issue_Date"])
    df = df.dropna(subset=["Issue_Date"]).copy()

    print("\nStep 7: Credit Risk Feature Engineering...")
    # Approval and Status Flags
    df["Is_Approved"] = (df["Loan_Status"] != "Rejected").astype(int)
    df["Is_Default"] = (df["Loan_Status"] == "Charged Off").astype(int)

    def categorize_loan_quality(status):
        if status in ["Fully Paid", "Current"]:
            return "Good Loan"
        elif status == "Charged Off":
            return "Bad Loan (Default)"
        return "Rejected Application"

    df["Loan_Quality"] = df["Loan_Status"].apply(categorize_loan_quality)

    # Net Realized Credit Loss on Defaults
    df["Net_Loss_Amount"] = np.where(
        df["Loan_Status"] == "Charged Off",
        np.maximum(0.0, df["Funded_Amount"] - df["Total_Payment"] - df["Recovery_Amount"]),
        0.0
    )

    # DTI & FICO Bands
    df["DTI_Band"] = pd.cut(
        df["DTI"],
        bins=[-0.1, 15.0, 25.0, 35.0, 100.0],
        labels=["Low (<15%)", "Moderate (15-25%)", "High (25-35%)", "Critical (>35%)"]
    )

    df["FICO_Band"] = pd.cut(
        df["FICO_Score"],
        bins=[0, 579, 669, 739, 799, 900],
        labels=["Poor (<580)", "Fair (580-669)", "Good (670-739)", "Very Good (740-799)", "Exceptional (800+)"]
    )

    df["Issue_Year"] = df["Issue_Date"].dt.year
    df["Issue_Month"] = df["Issue_Date"].dt.month
    df["Issue_Quarter"] = "Q" + df["Issue_Date"].dt.quarter.astype(str)
    df["Issue_Year_Month"] = df["Issue_Date"].dt.strftime("%Y-%m")

    print("\nStep 8: Star Schema Modeling & Export...")

    # Dimension 1: Borrowers
    dim_borrowers = (
        df[["Borrower_ID", "Employment_Title", "Employment_Length", "Home_Ownership", "Annual_Income", "FICO_Score", "Delinq_2Yrs"]]
        .drop_duplicates(subset=["Borrower_ID"])
        .sort_values(by="Borrower_ID")
    )
    borrower_path = os.path.join(proc_dir, "dim_borrowers.csv")
    dim_borrowers.to_csv(borrower_path, index=False)
    print(f"Exported {len(dim_borrowers):,} records to {borrower_path}")

    # Dimension 2: Geography
    dim_geography = (
        df[["State_Code", "State_Name", "Region"]]
        .drop_duplicates(subset=["State_Code"])
        .sort_values(by="State_Code")
    )
    geo_path = os.path.join(proc_dir, "dim_geography.csv")
    dim_geography.to_csv(geo_path, index=False)
    print(f"Exported {len(dim_geography)} records to {geo_path}")

    # Dimension 3: Calendar Date
    min_date = df["Issue_Date"].min()
    max_date = df["Issue_Date"].max()
    date_range = pd.date_range(start=min_date, end=max_date, freq="D")
    dim_date = pd.DataFrame({
        "Date": date_range.strftime("%Y-%m-%d"),
        "Year": date_range.year,
        "Quarter": "Q" + date_range.quarter.astype(str),
        "Month": date_range.month,
        "Month_Name": date_range.strftime("%B"),
        "Month_Year": date_range.strftime("%b %Y"),
        "Day": date_range.day
    })
    date_path = os.path.join(proc_dir, "dim_date.csv")
    dim_date.to_csv(date_path, index=False)
    print(f"Exported {len(dim_date)} dates to {date_path}")

    # Fact: Loans
    fact_cols = [
        "Application_ID", "Borrower_ID", "Issue_Date", "State_Code", "Grade", "Sub_Grade",
        "Term", "Loan_Purpose", "Verification_Status", "Loan_Amount", "Funded_Amount",
        "Interest_Rate", "Installment", "DTI", "DTI_Band", "FICO_Score", "FICO_Band",
        "Loan_Status", "Is_Approved", "Is_Default", "Loan_Quality",
        "Total_Payment", "Recovery_Amount", "Net_Loss_Amount"
    ]
    fact_loans = df[fact_cols].copy()
    fact_loans["Issue_Date"] = fact_loans["Issue_Date"].dt.strftime("%Y-%m-%d")
    fact_path = os.path.join(proc_dir, "clean_fact_loans.csv")
    fact_loans.to_csv(fact_path, index=False)
    print(f"Exported {len(fact_loans):,} fact records to {fact_path}")

    # Consolidated Clean Dataset for direct Power BI / Excel import
    complete_path = os.path.join(proc_dir, "clean_loan_risk_complete.csv")
    df_export = df.copy()
    df_export["Issue_Date"] = df_export["Issue_Date"].dt.strftime("%Y-%m-%d")
    df_export.to_csv(complete_path, index=False)
    print(f"Exported consolidated dataset ({len(df_export):,} rows) to {complete_path}")

    total_apps = len(df)
    total_approved = df["Is_Approved"].sum()
    approval_rate = (total_approved / total_apps) * 100
    rejection_rate = 100 - approval_rate
    total_funded = df["Funded_Amount"].sum()
    avg_funded = df[df["Is_Approved"] == 1]["Funded_Amount"].mean()
    total_collected = df["Total_Payment"].sum()
    avg_income = df["Annual_Income"].mean()
    default_count = df["Is_Default"].sum()
    default_rate = (default_count / total_approved) * 100

    print("\n" + "=" * 65)
    print("        BANK LOAN PORTFOLIO KPI SUMMARY (ETL RESULTS)")
    print("=" * 65)
    print(f"  • Total Loan Applications:    {total_apps:,}")
    print(f"  • Approved Applications:      {total_approved:,} ({approval_rate:.2f}%)")
    print(f"  • Rejection Rate:             {rejection_rate:.2f}%")
    print(f"  • Total Capital Funded:       ${total_funded:,.2f}")
    print(f"  • Average Loan Amount:        ${avg_funded:,.2f}")
    print(f"  • Total Cash Collected:       ${total_collected:,.2f}")
    print(f"  • Average Applicant Income:   ${avg_income:,.2f}")
    print(f"  • Default / Charged-off Rate: {default_rate:.2f}% ({default_count:,} loans)")
    print(f"  • Total Net Realized Loss:    ${df['Net_Loss_Amount'].sum():,.2f}")
    print("=" * 65)


if __name__ == "__main__":
    run_loan_etl()
