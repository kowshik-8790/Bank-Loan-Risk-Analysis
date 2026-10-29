# Bank Loan Risk Data Model Architecture

## 1. Dimensional Star Schema Design
The data warehouse architecture is engineered in a pristine **Star Schema** optimized for high-volume in-memory VertiPaq analytics and real-time DAX performance in Power BI.

```mermaid
erDiagram
    dim_date ||--o{ fact_loans : "1:N (date_id = issue_date)"
    dim_borrowers ||--o{ fact_loans : "1:N (borrower_id)"
    dim_geography ||--o{ fact_loans : "1:N (state_code)"

    dim_date {
        date date_id PK
        int year
        string quarter
        int month
        string month_name
        string month_year
        int day
    }

    dim_borrowers {
        string borrower_id PK
        string employment_title
        string employment_length
        string home_ownership
        decimal annual_income
        int fico_score
        int delinq_2yrs
    }

    dim_geography {
        string state_code PK
        string state_name
        string region
    }

    fact_loans {
        string application_id PK
        string borrower_id FK
        date issue_date FK
        string state_code FK
        string grade
        string sub_grade
        string term
        string loan_purpose
        string verification_status
        decimal loan_amount
        decimal funded_amount
        decimal interest_rate
        decimal installment
        decimal dti
        string dti_band
        int fico_score
        string fico_band
        string loan_status
        int is_approved
        int is_default
        string loan_quality
        decimal total_payment
        decimal recovery_amount
        decimal net_loss_amount
    }
```

---

## 2. Relationships & Cardinality Configuration

| Dimension Table | Fact Table | Primary Key &rarr; Foreign Key | Cardinality | Filter Direction | Active |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `dim_date` | `fact_loans` | `date_id` &rarr; `issue_date` | 1 : * (One-to-Many) | Single | **Active** |
| `dim_borrowers`| `fact_loans` | `borrower_id` &rarr; `borrower_id` | 1 : * (One-to-Many) | Single | **Active** |
| `dim_geography`| `fact_loans` | `state_code` &rarr; `state_code` | 1 : * (One-to-Many) | Single | **Active** |

### Modeling Principles:
1. **Single-Direction Filtering (1 &rarr; *)**: Ensures deterministic filter contexts and prevents circular model ambiguities.
2. **Date Table**: `dim_date` is marked as the official Date Table in Power BI for time-intelligence DAX functions (`SAMEPERIODLASTYEAR`, `DATEADD`, `TOTALYTD`).
3. **Optimized Data Types**: Floating point numeric values are stored as fixed decimal (`Currency` or `Decimal Number`) to eliminate floating-point rounding discrepancies.
