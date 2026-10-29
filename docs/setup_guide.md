# Bank Loan Risk Analysis - Setup & Execution Guide

Follow these steps to configure and run the project across **Python**, **MySQL**, **Power BI**, and **Excel**.

---

## 1. Environment & Python Setup

1. **Open Project Folder**:
   ```powershell
   cd C:\Users\kasan\.gemini\antigravity\scratch\bank-loan-risk-analysis
   ```

2. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Execute Data Pipeline**:
   ```powershell
   # Step 1: Generate Raw Data
   python src/generate_loan_data.py

   # Step 2: Clean, validate, and create Star-Schema datasets
   python src/etl_pipeline.py

   # Step 3: Generate the multi-sheet styled Excel Executive Report
   python src/generate_excel_report.py

   # Step 4: Populate database and run sample SQL KPI analytics
   python src/db_connector.py
   ```

---

## 2. MySQL Database Configuration

1. **Execute Schema Setup**:
   ```bash
   mysql -u root -p < sql/01_schema_setup.sql
   ```

2. **Load Data into MySQL**:
   ```powershell
   python src/db_connector.py --mysql
   ```

3. **Run Analytical Queries**:
   - `sql/02_data_cleaning_views.sql`: Instantiate executive views.
   - `sql/03_kpi_risk_analysis.sql`: Underwriting KPIs and MoM funded growth.
   - `sql/04_demographic_underwriting.sql`: Demographics, home ownership, and purpose metrics.
   - `sql/05_portfolio_risk_segmentation.sql`: Risk grades and NTILE size quartiles.

---

## 3. Power BI Desktop Connection

1. Open **Power BI Desktop**.
2. **Import Data**:
   - Navigate to `Get Data` &rarr; `Text/CSV` &rarr; Load files from `data/processed/`.
3. **Verify Relationships**:
   - Link `dim_borrowers[borrower_id]` to `fact_loans[borrower_id]`.
   - Link `dim_geography[state_code]` to `fact_loans[state_code]`.
   - Link `dim_date[date_id]` to `fact_loans[issue_date]`.
4. **Load DAX Measures**:
   - Copy measures from `powerbi/dax_measures.dax`.
5. **Apply Executive Theme**:
   - `View` &rarr; `Themes` &rarr; `Browse for themes...` &rarr; Select `powerbi/bank_executive_theme.json`.
6. Follow wireframes in `powerbi/dashboard_visual_spec.md`.

---

## 4. Interactive Browser Preview

Open `dashboard_preview/index.html` in any browser to interact with the dashboard, charts, KPI cards, and dynamic risk filters immediately.
