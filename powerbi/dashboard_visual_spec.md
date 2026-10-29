# Power BI Dashboard Visual Design & Wireframe Specification

## Canvas Specs
- **Aspect Ratio**: 16:9 Widescreen (1920 x 1080 px)
- **Palette**: Executive Banking Palette
  - **Navy**: `#0B2545`
  - **Gold / Accent**: `#D4AF37`
  - **Good Loan Green**: `#10B981`
  - **Bad Loan / Charge-off Red**: `#EF4444`
  - **Surface**: `#FFFFFF` | Background: `#F8FAFC`

---

## Page 1: Executive Lending & Underwriting Overview

### Top Navigation & Slicers
- Slicers: Year/Quarter Slider, Risk Grade (A - F), Loan Purpose dropdown, Region (West, East, South, Midwest).

### KPI Cards Row (5 Cards)
1. **Total Applications**: `10,000` | Subtext: `Approval Rate: 96.85%`
2. **Total Capital Funded**: `$190.82M` | Subtext: `Avg Loan: $19,702.99`
3. **Total Cash Collected**: `$168.83M` | Subtext: `Principal + Interest`
4. **Portfolio Default Rate**: `13.83%` | Subtext: `1,339 Charged Off Loans`
5. **Net Realized Credit Loss**: `$18.19M` | Subtext: `Loss Severity: 9.53% of Capital`

### Main Visuals
- **Monthly Capital Funded & Default Trend (Line and Clustered Column Chart)**:
  - *X-Axis*: `dim_date[month_year]`
  - *Column Y-Axis*: `[Total Capital Funded]` (Navy `#0B2545`)
  - *Line Y-Axis*: `[Portfolio Default Rate %]` (Red `#EF4444`)
- **Good Loans vs Bad Loans Quality Donut Chart**:
  - Values: `[Good Loans Funded Capital]` vs `[Bad Loans Funded Capital]`
  - Colors: `#10B981` (Good) vs `#EF4444` (Bad)
- **Risk Grade Capital Deployment & Loss Table**:
  - Columns: Grade, Applications, Funded Capital, Avg Rate %, Default Rate %, Net Loss $.

---

## Page 2: Credit Risk & Risk Grade Deep-Dive

### Key Visuals
1. **Default Rate by Credit Grade Bar Chart**:
   - Compares default rate across Grades A (4.1%), B (8.9%), C (16.3%), D (24.7%), E (34.7%), F (42.3%).
2. **Debt-to-Income (DTI) vs Interest Rate Scatter Plot**:
   - *X-Axis*: `DTI %`
   - *Y-Axis*: `Interest Rate %`
   - *Bubble Size*: `Funded Amount`
   - *Color*: Loan Status (Fully Paid vs Charged Off)
3. **Loss Severity Matrix Table with Data Bars**:
   - Subgrades A1 through F5 with conditional data bars showing default rate escalation.

---

## Page 3: Borrower Demographics & Underwriting

### Key Visuals
1. **Home Ownership vs Default Likelihood**:
   - Clustered column chart comparing Mortgage vs Rent vs Own.
2. **Employment Stability Breakdown**:
   - Analysis of borrowers by tenure (<1 yr, 1-2 yrs, 3-5 yrs, 6-9 yrs, 10+ yrs).
3. **Annual Income Quintiles & Average Funded Amount**:
   - Shows loan demand scaling against borrower income bands.

---

## Page 4: Geographic & Regional Lending

### Key Visuals
1. **State-Level Funded Capital & Risk Map (Shape / Azure Map)**:
   - Bubble size: `[Total Capital Funded]`
   - Color saturation: `[Portfolio Default Rate %]`
2. **Top States by Lending Volume**:
   - Horizontal bar chart of California, New York, Texas, Florida, Illinois.
