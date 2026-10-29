# Executive Underwriting & Credit Risk Analysis Report

**Reporting Portfolio**: Retail & Commercial Unsecured Installment Loans (2022 &ndash; 2025)  
**Data Infrastructure**: Python (Pandas/NumPy) &rarr; MySQL 8.0 &rarr; Power BI & Microsoft Excel  
**Audience**: Chief Risk Officer (CRO), Head of Credit Underwriting, Credit Risk Committee  

---

## 1. Executive Summary & Lending Portfolio Health

| Portfolio Metric | Portfolio Realized | Target Benchmark | Risk Assessment |
| :--- | :--- | :--- | :--- |
| **Total Loan Applications** | **10,000** | 9,500 | Strong origination pipeline |
| **Approval Rate %** | **96.85%** | 90.00% &ndash; 92.00% | Underwriting standards too lenient |
| **Rejection Rate %** | **3.15%** | 8.00% &ndash; 10.00% | Low adverse action rate |
| **Total Capital Funded** | **\$190,823,500.00** | \$175.00M | Above capital allocation target |
| **Average Loan Amount** | **\$19,702.99** | \$18,500.00 | Higher ticket exposure |
| **Total Cash Recovered** | **\$168,832,347.37** | \$160.00M | Healthy cash flow generation |
| **Average Applicant Income** | **\$72,936.25** | \$68,000.00 | Strong baseline earning capacity |
| **Portfolio Default Rate %** | **13.83%** | &le; 10.00% | **Elevated Credit Risk (+3.83%)** |
| **Net Realized Credit Loss** | **\$18,190,869.04** | &le; \$14.00M | **Loss Severity: 9.53% of Capital** |

---

## 2. Core Credit Risk Findings

### Finding 1: Subprime Grade Degradation (Grades E & F)
- **Observation**:
  - Grade E borrowers incur a **34.66% default rate** (\$3.12M net loss).
  - Grade F borrowers incur a **42.34% default rate** (\$838K net loss).
  - Combined, Grades E and F account for only **6.88% of funded loans**, yet generate **21.8% (\$3.96M) of total credit losses**.
- **Root Cause**: Reliance on high nominal interest rates (23.5% &ndash; 27.7%) failed to offset the surge in credit losses, leading to negative Net Interest Margins (NIM) in these subprime tiers.
- **Actionable Recommendation**:
  1. Increase the minimum underwriting FICO cutoff from **580 to 620**.
  2. Implement an automated decline rule for any application with FICO &lt; 620 and DTI &gt; 25%.
  3. **Estimated Profit Recovery**: Eliminating Grade F and capping Grade E origination will save **\$2.85M annually** in write-offs.

---

### Finding 2: Debt-to-Income (DTI) as Primary Default Predictor
- **Observation**:
  - Borrowers with DTI &lt; 15% exhibit a default rate of only **7.8%**.
  - In contrast, borrowers with DTI &gt; 30% suffer a **22.4% default rate** (a **2.87x risk escalation**).
- **Root Cause**: Current underwriting thresholds permit approval up to 38% DTI without secondary asset verification.
- **Actionable Recommendation**:
  1. Institute a strict maximum front-end DTI cap of **30%** for unsecured personal loans.
  2. For DTI between 25% and 30%, require verified debt consolidation payoff guarantees directly to third-party creditors.

---

### Finding 3: Home Ownership Security Effect
- **Observation**:
  - Homeowners with a **Mortgage** maintain the lowest default rate (**11.4%**) and highest average income (\$81,200).
  - **Renters** display a default rate of **16.9%** and lower recovery amounts during default.
- **Actionable Recommendation**: Apply a 50 bps interest rate concession for mortgage holders to capture higher-quality volume while tightening debt limits on renters.
