# Excel Bank Loan Analysis & Power Query Workflow

This document details how loan data is processed, cleaned, and modeled inside **Microsoft Excel** using **Power Query** and **Pivot Tables**.

---

## 1. Power Query Data Cleaning Steps

1. **Load Raw Data**:
   - `Data` &rarr; `Get Data` &rarr; `From File` &rarr; `From Text/CSV` &rarr; Select `bank_loan_raw_applications.csv`.
2. **Deduplication**:
   - Select `Application_ID` &rarr; Right click &rarr; **Remove Duplicates**.
3. **Trim & Format Clean Up**:
   - Select text columns (`Employment_Title`, `Home_Ownership`, `State_Name`) &rarr; `Transform` &rarr; `Format` &rarr; `Trim`.
   - Select `Home_Ownership` &rarr; `Transform` &rarr; `Uppercase`.
4. **Data Type Correction**:
   - Clean currency symbols (`$`) and percentage signs (`%`) using `Replace Values`.
   - Set `Loan_Amount`, `Funded_Amount`, `Total_Payment` to **Decimal Number / Currency**.
   - Set `Issue_Date` to **Date** using `Locale: English (US)`.
5. **Feature Engineering**:
   - Add Custom Column **Good Loan Indicator**:
     `if [Loan_Status] = "Charged Off" then "Bad Loan" else if [Loan_Status] = "Rejected" then "Rejected" else "Good Loan"`
   - Add Custom Column **Net Realized Loss**:
     `if [Loan_Status] = "Charged Off" then [Funded_Amount] - [Total_Payment] - [Recovery_Amount] else 0`

---

## 2. Pivot Table Modeling & KPI Calculations

| Business Metric | Excel Formula / Pivot Field |
| :--- | :--- |
| **Approval Rate %** | `=COUNTIF(Status_Range, "<>Rejected") / COUNTA(Status_Range)` |
| **Default Rate %** | `=COUNTIF(Status_Range, "Charged Off") / COUNTIF(Status_Range, "<>Rejected")` |
| **Average Loan Size** | `=AVERAGEIF(Status_Range, "<>Rejected", Funded_Amount_Range)` |
| **Credit Tier Lookup** | `=XLOOKUP(Grade_Cell, Grade_Table[Grade], Grade_Table[Risk_Tier], "Unknown")` |
| **Multi-Condition Loss** | `=SUMIFS(Loss_Range, Grade_Range, "E", State_Range, "CA")` |
