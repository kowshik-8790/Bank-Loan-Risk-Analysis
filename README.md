# 🏦 Bank Loan Risk Analysis & Portfolio Dossier

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![PowerBI](https://img.shields.io/badge/PowerBI-Financial%20Risk-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Excel](https://img.shields.io/badge/Microsoft%20Excel-Financial%20Modeling-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)

---

## 📌 Executive Summary
An end-to-end banking loan risk evaluation system and interactive business intelligence dashboard developed to analyze **2,500+ loan applications** totaling **$39.61M in lending portfolio data**. Cleaned, transformed, and validated relational datasets using **Python (`Pandas`, `NumPy`)**, **SQL (`MySQL`)**, and **Excel** to ensure strict credit underwriting precision and regulatory reporting compliance.

---

## 🚀 Key Business KPIs & Risk Engineering
- **2,500+ Applications Analyzed**: Evaluated $39.61M in consumer, commercial, and small business loan requests.
- **Credit Risk Classification**:
  - **Approval Rate**: **81.0%**
  - **Rejection Rate**: **19.0%**
  - Applications classified by FICO credit score tiers, Debt-to-Income (DTI) thresholds, and employment stability.
- **Executive Lending Metrics**:
  - **Total Portfolio Loan Amount**: `$39.61M`
  - **Average Loan Amount**: `$15,845`
  - **Average Applicant Annual Income**: `$65,988`
- **Credit Stress Testing & Slicers**:
  - Multi-tier risk grading (Grade A Low Risk through Grade D/F High Risk).
  - Real-time loan assessment calculator and interactive drill-through applicant dossier.

---

## 🛠️ Tech Stack & Skills
| Layer | Technologies & Tools | Key Role |
| :--- | :--- | :--- |
| **Data Cleaning & ETL** | Python (`pandas`, `numpy`), Excel | Data validation, missing value handling, outlier normalization |
| **Relational Database** | MySQL 8.0 / MariaDB / SQLite | Schema definition (`schema.sql`), risk distribution queries (`loan_risk_queries.sql`) |
| **Business Intelligence** | Power BI Desktop, DAX | Interactive dashboard with dynamic slicers & drill-through functionality (`powerbi_dashboard_guide.md`) |
| **Web Dashboard** | HTML5, CSS3, JavaScript, Chart.js | Real-time interactive portfolio dashboard & risk calculator |

---

## 📂 Repository Structure
```
bank-loan-risk-analysis/
├── schema.sql                 # MySQL relational schema & performance indexes
├── loan_risk_queries.sql      # Analytical SQL queries (Approval rates, DTI, Risk Grades)
├── powerbi_dashboard_guide.md # Power BI DAX calculations & data modeling blueprint
├── process_loans.py           # Python ETL & data generation script
├── loans_data.csv             # Full dataset (2,500 loan application records)
├── loans_data.json            # JSON dataset powering interactive charts
├── bank_loans.db              # SQLite relational database
├── index.html                 # Interactive risk evaluation web interface
├── app.js                     # Dynamic slicers & risk calculator logic
└── README.md                  # Comprehensive documentation
```

---

## 💻 How to Run

### 1. Python Data Processing
```bash
python process_loans.py
```

### 2. SQL Schema & Risk Analytics
Execute `schema.sql` and `loan_risk_queries.sql` in MySQL Workbench or terminal:
```sql
SOURCE schema.sql;
SOURCE loan_risk_queries.sql;
```

### 3. Interactive Web Dashboard
Open `index.html` in your browser or run:
```bash
python -m http.server 8080
```
Navigate to `http://localhost:8080`.

---

## 👤 Author
- **Kasanaboina Kowshik**
- **Education:** B.Tech in Computer Science (Artificial Intelligence), Parul University
- **Email:** [kasanaboinakowshik@gmail.com](mailto:kasanaboinakowshik@gmail.com)
- **Phone:** +91 8790211519
