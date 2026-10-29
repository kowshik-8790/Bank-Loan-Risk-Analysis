# Bank Loan Risk Analysis KPI Dictionary

| Key Performance Indicator | Mathematical / DAX Definition | Target Benchmark | Business Action When Triggered |
| :--- | :--- | :--- | :--- |
| **Approval Rate %** | `(Total Approved Loans / Total Applications) * 100` | 90.0% &ndash; 92.0% | If &gt; 95%, review credit score cutoffs to avoid over-lenient risk acceptance. |
| **Rejection Rate %** | `(Total Rejected Apps / Total Applications) * 100` | 8.0% &ndash; 10.0% | If &lt; 5%, audit automated scorecard rules for missing adverse action triggers. |
| **Total Capital Funded** | `SUM(fact_loans[funded_amount])` | Capital Plan &plusmn; 5% | Adjust marketing spend or tighten loan approval caps per risk segment. |
| **Average Loan Amount** | `Total Capital Funded / Total Approved Loans` | \$18,000 &ndash; \$20,000 | Monitor single-borrower concentration risk; enforce credit tier maximums. |
| **Applicant Income** | `AVERAGE(dim_borrowers[annual_income])` | &ge; \$65,000 | Adjust income verification protocols if low-income cohorts show rising DTI. |
| **Debt-to-Income (DTI)** | `AVERAGE(fact_loans[dti])` | &le; 22.0% | Cap discretionary approvals when DTI exceeds 28%; require direct creditor payoff. |
| **Portfolio Default Rate %** | `(Bad Loans (Defaults) / Total Approved Loans) * 100` | &le; 10.0% | Tighten subprime lending; halt Grade F origination; increase collection outreach. |
| **Net Realized Loss** | `SUM(Funded - Payment - Recovery)` | &le; 8.0% of Capital | Adjust loss reserves (CECL / IFRS 9 provisions) and raise subgrade pricing. |
