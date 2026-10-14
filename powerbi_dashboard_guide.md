# 🏦 Power BI Bank Loan Risk Analysis Dashboard Blueprint

**Author:** Kasanaboina Kowshik  
**Email:** kasanaboinakowshik@gmail.com  
**Tech Stack:** Power BI Desktop, DAX, Power Query, MySQL, Excel  

---

## 🏗️ 1. Architecture & Data Modeling
Connect Power BI Desktop to `loans_data.csv` or MySQL database `bank_loan_risk_db`.
- **Primary Fact Table:** `Fact_LoanApplications`
  - Columns: `application_id`, `applicant_income`, `loan_amount`, `credit_score`, `dti_ratio`, `employment_length_years`, `loan_purpose`, `loan_status`, `risk_grade`.
- **Derived Risk Dimensions:**
  - `Dim_CreditTier` (Excellent: 750+, Good: 700-749, Fair: 650-699, Poor: <650)
  - `Dim_DTIBand` (<20%, 20-35%, 35-43%, >43%)

---

## 🧮 2. Key DAX Measures
Create a dedicated `_Measures` table in Power BI and implement the following:

```dax
// 1. Total Applications
Total Applications = COUNTROWS(Fact_LoanApplications)

// 2. Total Loan Portfolio Value ($)
Total Loan Volume = SUM(Fact_LoanApplications[loan_amount])

// 3. Total Approved Loan Amount ($)
Total Approved Amount = 
CALCULATE(
    SUM(Fact_LoanApplications[loan_amount]),
    Fact_LoanApplications[loan_status] = "Approved"
)

// 4. Overall Approval Rate (%)
Approval Rate % = 
DIVIDE(
    CALCULATE(COUNTROWS(Fact_LoanApplications), Fact_LoanApplications[loan_status] = "Approved"),
    COUNTROWS(Fact_LoanApplications),
    0
)

// 5. Rejection Rate (%)
Rejection Rate % = 1 - [Approval Rate %]

// 6. Average Loan Amount ($)
Avg Loan Amount = AVERAGE(Fact_LoanApplications[loan_amount])

// 7. Average Applicant Income ($)
Avg Applicant Income = AVERAGE(Fact_LoanApplications[applicant_income])

// 8. High Risk Exposure Amount ($)
High Risk Loan Exposure = 
CALCULATE(
    SUM(Fact_LoanApplications[loan_amount]),
    Fact_LoanApplications[risk_grade] = "Grade D/F (High Risk)"
)

// 9. Weighted Average FICO Credit Score
Weighted Credit Score = 
DIVIDE(
    SUMX(Fact_LoanApplications, Fact_LoanApplications[credit_score] * Fact_LoanApplications[loan_amount]),
    [Total Loan Volume],
    0
)
```

---

## 📊 3. Interactive Visual Layout & Drill-Through
1. **Executive Scorecards (KPI Cards):**
   - **Total Applications:** `2,500`
   - **Total Portfolio Value:** `$39.61M`
   - **Approval Rate:** `81.0%`
   - **Rejection Rate:** `19.0%`
   - **Average Loan Amount:** `$15,845`
   - **Average Applicant Income:** `$65,988`

2. **Approval Status & Risk Grade Visuals (Donut & Matrix):**
   - Donut Chart: `Approved` vs `Rejected` proportion
   - Clustered Bar: `Total Applications` by `Risk Grade (A, B, C, D/F)`

3. **Demographic & Lending Performance (Tree Map & Bar Charts):**
   - Loan Purpose breakdown (`Debt Consolidation`, `Home Improvement`, `Small Business`, `Major Purchase`)
   - Employment Tenure vs Approval Rate line

4. **Drill-Through Applicant Dossier Page:**
   - Right-click on any Risk Grade to drill through to an individual applicant audit table showing credit scores, DTI ratios, and recommended credit underwriting decisions.

5. **Dynamic Slicers:**
   - Loan Purpose dropdown
   - Risk Grade multi-select tiles
   - FICO Credit Score range slider
   - DTI Ratio range slider
