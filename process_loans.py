import pandas as pd
import numpy as np
import json
import sqlite3

np.random.seed(2025)
n_apps = 2500

incomes = np.random.normal(65988, 18000, n_apps)
incomes = np.clip(incomes, 20000, 180000)

loan_amounts = np.random.normal(15845, 5500, n_apps)
loan_amounts = np.clip(loan_amounts, 4000, 45000)

credit_scores = np.random.normal(690, 65, n_apps)
credit_scores = np.clip(credit_scores, 450, 850).astype(int)

dti_ratios = np.random.uniform(10, 48, n_apps)

df = pd.DataFrame({
    'application_id': [f"LNK-{80000 + i}" for i in range(n_apps)],
    'applicant_income': np.round(incomes, 2),
    'loan_amount': np.round(loan_amounts, 2),
    'credit_score': credit_scores,
    'dti_ratio': np.round(dti_ratios, 1),
    'employment_length_years': np.random.randint(1, 15, n_apps),
    'loan_purpose': np.random.choice(['Debt Consolidation', 'Home Improvement', 'Small Business', 'Major Purchase'], p=[0.45, 0.25, 0.18, 0.12])
})

sorted_idx = df.sort_values(by=['credit_score', 'dti_ratio'], ascending=[False, True]).index
df['loan_status'] = 'Rejected'
df.loc[sorted_idx[:2025], 'loan_status'] = 'Approved'

# Adjust average loan amount to $15,845
avg_loan_scale = 15845.0 / df['loan_amount'].mean()
df['loan_amount'] = (df['loan_amount'] * avg_loan_scale).round(2)

# Adjust incomes to average $65,988
inc_scale = 65988.0 / df['applicant_income'].mean()
df['applicant_income'] = (df['applicant_income'] * inc_scale).round(2)

def get_risk_grade(row):
    if row['credit_score'] >= 720 and row['dti_ratio'] < 25: return 'Grade A (Low Risk)'
    elif row['credit_score'] >= 660 and row['dti_ratio'] < 35: return 'Grade B (Moderate Risk)'
    elif row['credit_score'] >= 600 and row['dti_ratio'] < 42: return 'Grade C (Elevated Risk)'
    else: return 'Grade D/F (High Risk)'

df['risk_grade'] = df.apply(get_risk_grade, axis=1)

total_loan_amount = df['loan_amount'].sum()

print("Bank Loan Risk Analysis Data Summary:")
print(f"Total Applications: {len(df)}")
print(f"Approval Rate: {(df['loan_status']=='Approved').mean()*100:.1f}%")
print(f"Rejection Rate: {(df['loan_status']=='Rejected').mean()*100:.1f}%")
print(f"Total Portfolio Value: ${total_loan_amount/1e6:.2f}M")
print(f"Average Loan Amount: ${df['loan_amount'].mean():,.2f}")
print(f"Average Applicant Income: ${df['applicant_income'].mean():,.2f}")

conn = sqlite3.connect('bank_loans.db')
df.to_sql('loan_applications', conn, if_exists='replace', index=False)
conn.close()

df.to_json('loans_data.json', orient='records')
print("Exported bank_loans.db and loans_data.json successfully.")
