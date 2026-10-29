"""
Bank Loan Executive Excel Workbook Generator
Creates a professionally styled, multi-sheet Excel workbook with formatted
underwriting KPIs, risk grade distributions, demographic breakdowns, and regional lending metrics.
"""

import os
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


def create_loan_excel_report():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clean_csv = os.path.join(base_dir, "data", "processed", "clean_loan_risk_complete.csv")
    output_excel = os.path.join(base_dir, "data", "processed", "bank_loan_executive_report.xlsx")

    df = pd.read_csv(clean_csv)

    # 1. High-Level KPI Summary Table
    total_apps = len(df)
    total_approved = int(df["Is_Approved"].sum())
    total_rejected = total_apps - total_approved
    approval_rate = (total_approved / total_apps)
    rejection_rate = (total_rejected / total_apps)
    total_funded = float(df["Funded_Amount"].sum())
    avg_loan_amt = float(df[df["Is_Approved"] == 1]["Funded_Amount"].mean())
    total_cash_collected = float(df["Total_Payment"].sum())
    avg_income = float(df["Annual_Income"].mean())
    avg_dti = float(df["DTI"].mean()) / 100.0
    avg_fico = float(df["FICO_Score"].mean())
    default_count = int(df["Is_Default"].sum())
    default_rate = (default_count / total_approved)
    total_net_loss = float(df["Net_Loss_Amount"].sum())

    kpi_df = pd.DataFrame([
        {"Key Performance Indicator": "Total Loan Applications", "Value": total_apps, "Format": "Integer"},
        {"Key Performance Indicator": "Approved Loans Count", "Value": total_approved, "Format": "Integer"},
        {"Key Performance Indicator": "Rejected Applications Count", "Value": total_rejected, "Format": "Integer"},
        {"Key Performance Indicator": "Loan Approval Rate", "Value": approval_rate, "Format": "Percent"},
        {"Key Performance Indicator": "Loan Rejection Rate", "Value": rejection_rate, "Format": "Percent"},
        {"Key Performance Indicator": "Total Funded Capital", "Value": total_funded, "Format": "Currency"},
        {"Key Performance Indicator": "Average Funded Loan Amount", "Value": avg_loan_amt, "Format": "Currency"},
        {"Key Performance Indicator": "Total Cash Payments Collected", "Value": total_cash_collected, "Format": "Currency"},
        {"Key Performance Indicator": "Average Applicant Annual Income", "Value": avg_income, "Format": "Currency"},
        {"Key Performance Indicator": "Average Debt-to-Income (DTI)", "Value": avg_dti, "Format": "Percent"},
        {"Key Performance Indicator": "Average Borrower FICO Score", "Value": avg_fico, "Format": "Decimal"},
        {"Key Performance Indicator": "Portfolio Default (Charge-off) Rate", "Value": default_rate, "Format": "Percent"},
        {"Key Performance Indicator": "Total Net Realized Credit Loss", "Value": total_net_loss, "Format": "Currency"},
    ])

    # 2. Risk Grade Breakdown
    grade_summary = df[df["Is_Approved"] == 1].groupby("Grade").agg(
        Total_Loans=("Application_ID", "count"),
        Total_Funded=("Funded_Amount", "sum"),
        Avg_Funded=("Funded_Amount", "mean"),
        Avg_Interest_Rate=("Interest_Rate", "mean"),
        Avg_FICO=("FICO_Score", "mean"),
        Avg_DTI=("DTI", "mean"),
        Default_Count=("Is_Default", "sum"),
        Net_Loss=("Net_Loss_Amount", "sum")
    ).reset_index()
    grade_summary["Default_Rate_Pct"] = (grade_summary["Default_Count"] / grade_summary["Total_Loans"]) * 100
    grade_summary = grade_summary.sort_values(by="Grade")

    # 3. Purpose Breakdown
    purpose_summary = df[df["Is_Approved"] == 1].groupby("Loan_Purpose").agg(
        Total_Loans=("Application_ID", "count"),
        Total_Funded=("Funded_Amount", "sum"),
        Avg_Loan_Amount=("Funded_Amount", "mean"),
        Default_Count=("Is_Default", "sum"),
        Total_Collected=("Total_Payment", "sum"),
        Net_Loss=("Net_Loss_Amount", "sum")
    ).reset_index()
    purpose_summary["Default_Rate_Pct"] = (purpose_summary["Default_Count"] / purpose_summary["Total_Loans"]) * 100
    purpose_summary = purpose_summary.sort_values(by="Total_Funded", ascending=False)

    # 4. Demographic Breakdown (Home Ownership & Employment)
    demo_summary = df.groupby(["Home_Ownership", "Employment_Length"]).agg(
        Applications=("Application_ID", "count"),
        Approval_Rate=("Is_Approved", "mean"),
        Total_Funded=("Funded_Amount", "sum"),
        Avg_Income=("Annual_Income", "mean"),
        Default_Rate=("Is_Default", "mean")
    ).reset_index()
    demo_summary["Approval_Rate"] = demo_summary["Approval_Rate"] * 100
    demo_summary["Default_Rate"] = demo_summary["Default_Rate"] * 100
    demo_summary = demo_summary.sort_values(by="Applications", ascending=False)

    # 5. Regional Lending Performance
    reg_summary = df.groupby(["Region", "State_Code", "State_Name"]).agg(
        Total_Applications=("Application_ID", "count"),
        Approved_Loans=("Is_Approved", "sum"),
        Total_Funded=("Funded_Amount", "sum"),
        Default_Loans=("Is_Default", "sum"),
        Net_Credit_Loss=("Net_Loss_Amount", "sum")
    ).reset_index()
    reg_summary["Approval_Rate_Pct"] = (reg_summary["Approved_Loans"] / reg_summary["Total_Applications"]) * 100
    reg_summary["Default_Rate_Pct"] = (reg_summary["Default_Loans"] / reg_summary["Approved_Loans"]) * 100
    reg_summary = reg_summary.sort_values(by="Total_Funded", ascending=False)

    # Write sheets
    with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
        kpi_df.to_excel(writer, sheet_name="KPI_Overview", index=False)
        grade_summary.to_excel(writer, sheet_name="Risk_Grade_Breakdown", index=False)
        purpose_summary.to_excel(writer, sheet_name="Loan_Purpose_Analysis", index=False)
        demo_summary.to_excel(writer, sheet_name="Demographics_Underwriting", index=False)
        reg_summary.to_excel(writer, sheet_name="Regional_Lending", index=False)
        df.head(2000).to_excel(writer, sheet_name="Sample_Clean_Loans", index=False)

    # Styling with Banking Navy & Gold
    from openpyxl import load_workbook
    wb = load_workbook(output_excel)

    navy_fill = PatternFill(start_color="0B2545", end_color="0B2545", fill_type="solid")
    gold_fill = PatternFill(start_color="D4AF37", end_color="D4AF37", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")

    for ws in wb.worksheets:
        ws.views.sheetView[0].showGridLines = True
        ws.row_dimensions[1].height = 26

        for cell in ws[1]:
            cell.fill = navy_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        for col in ws.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 13)

    # Custom formats for KPI_Overview
    ws_kpi = wb["KPI_Overview"]
    for row in range(2, len(kpi_df) + 2):
        fmt = ws_kpi.cell(row=row, column=3).value
        cell = ws_kpi.cell(row=row, column=2)
        if fmt == "Currency":
            cell.number_format = '$#,##0.00'
        elif fmt == "Percent":
            cell.number_format = '0.00%'
        elif fmt == "Integer":
            cell.number_format = '#,##0'
        elif fmt == "Decimal":
            cell.number_format = '0.0'
        cell.alignment = Alignment(horizontal="right")
        cell.font = Font(bold=True)

    # Custom formats for Risk_Grade_Breakdown
    ws_grade = wb["Risk_Grade_Breakdown"]
    for r in range(2, len(grade_summary) + 2):
        ws_grade.cell(row=r, column=2).number_format = '#,##0'
        ws_grade.cell(row=r, column=3).number_format = '$#,##0.00'
        ws_grade.cell(row=r, column=4).number_format = '$#,##0.00'
        ws_grade.cell(row=r, column=5).number_format = '0.00"%"'
        ws_grade.cell(row=r, column=6).number_format = '0.0'
        ws_grade.cell(row=r, column=7).number_format = '0.00"%"'
        ws_grade.cell(row=r, column=8).number_format = '#,##0'
        ws_grade.cell(row=r, column=9).number_format = '$#,##0.00'
        ws_grade.cell(row=r, column=10).number_format = '0.00"%"'

    wb.save(output_excel)
    print(f"[OK] Generated formatted Bank Loan Executive Excel Report: {output_excel}")


if __name__ == "__main__":
    create_loan_excel_report()
