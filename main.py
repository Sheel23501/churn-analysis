import pandas as pd
import sqlite3

# ============================================
# STEP 1: Load CSV into SQLite
# ============================================
db = sqlite3.connect('churn_analysis.db')
df = pd.read_csv('Telco_customer_churn.csv')

df.to_sql('customer', con=db, if_exists='replace', index=False)

cursor = db.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
print("Tables:", cursor.fetchall())

cursor.execute('SELECT COUNT(*) FROM customer')
print("Row count:", cursor.fetchone())

# ============================================
# STEP 2: Explore data
# ============================================
print(pd.read_sql_query("SELECT * FROM customer LIMIT 5", db))
print(pd.read_sql_query('SELECT "Churn Label", COUNT(*) FROM customer GROUP BY "Churn Label"', db))

# ============================================
# STEP 3: Business Questions
# ============================================

# Q1: Overall churn rate
q1 = """
SELECT 
  ROUND(100.0 * SUM(CASE WHEN "Churn Label"='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customer;
"""
print("\n--- Overall Churn Rate ---")
print(pd.read_sql_query(q1, db))

# Q2: Churn rate by contract type
q2 = """
SELECT 
  Contract,
  COUNT(*) AS total_customers,
  SUM(CASE WHEN "Churn Label"='Yes' THEN 1 ELSE 0 END) AS churned,
  ROUND(100.0 * SUM(CASE WHEN "Churn Label"='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_pct
FROM customer
GROUP BY Contract
ORDER BY churn_pct DESC;
"""
print("\n--- Churn Rate by Contract Type ---")
print(pd.read_sql_query(q2, db))

# Q3: Avg monthly charges - churned vs retained
q3 = """
SELECT 
  "Churn Label",
  ROUND(AVG("Monthly Charges"), 2) AS avg_monthly_charge
FROM customer
GROUP BY "Churn Label";
"""
print("\n--- Avg Monthly Charges: Churned vs Retained ---")
print(pd.read_sql_query(q3, db))

# Q4: Tenure < 12 months vs churn
q4 = """
SELECT 
  CASE WHEN "Tenure Months" < 12 THEN 'New (<12mo)' ELSE 'Established (12mo+)' END AS tenure_group,
  COUNT(*) AS total_customers,
  ROUND(100.0 * SUM(CASE WHEN "Churn Label"='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_pct
FROM customer
GROUP BY tenure_group;
"""
print("\n--- Churn by Tenure Group ---")
print(pd.read_sql_query(q4, db))

# Q5: Churn rate by state (geography)
q5 = """
SELECT 
  State,
  COUNT(*) AS total_customers,
  SUM(CASE WHEN "Churn Label"='Yes' THEN 1 ELSE 0 END) AS churned,
  ROUND(100.0 * SUM(CASE WHEN "Churn Label"='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_pct
FROM customer
GROUP BY State
ORDER BY churn_pct DESC
LIMIT 10;
"""
print("\n--- Top 10 States by Churn Rate ---")
print(pd.read_sql_query(q5, db))

# Q6: Top churn reasons
q6 = """
SELECT 
  "Churn Reason",
  COUNT(*) AS count
FROM customer
WHERE "Churn Label" = 'Yes' AND "Churn Reason" IS NOT NULL AND "Churn Reason" != ''
GROUP BY "Churn Reason"
ORDER BY count DESC
LIMIT 10;
"""
print("\n--- Top Churn Reasons ---")
print(pd.read_sql_query(q6, db))

# Q7: Avg CLTV - churned vs retained (business impact)
q7 = """
SELECT 
  "Churn Label",
  ROUND(AVG(CLTV), 2) AS avg_cltv,
  COUNT(*) AS customer_count
FROM customer
GROUP BY "Churn Label";
"""
print("\n--- Avg CLTV: Churned vs Retained ---")
print(pd.read_sql_query(q7, db))

# ============================================
# STEP 4: CTE Example (for skills demonstration)
# ============================================
q8 = """
WITH contract_summary AS (
  SELECT Contract, "Churn Label", COUNT(*) AS cnt
  FROM customer
  GROUP BY Contract, "Churn Label"
)
SELECT 
  Contract,
  SUM(CASE WHEN "Churn Label"='Yes' THEN cnt ELSE 0 END) AS churned,
  SUM(cnt) AS total
FROM contract_summary
GROUP BY Contract;
"""
print("\n--- CTE Example: Churned vs Total by Contract ---")
print(pd.read_sql_query(q8, db))

# ============================================
# STEP 5: Stretch Goal - Risk Score for active customers
# ============================================
q9 = """
SELECT 
  CustomerID,
  "Tenure Months",
  "Monthly Charges",
  Contract,
  CASE 
    WHEN "Tenure Months" < 12 AND Contract = 'Month-to-month' AND "Monthly Charges" > 70 THEN 'High'
    WHEN "Tenure Months" BETWEEN 12 AND 24 AND Contract = 'Month-to-month' THEN 'Medium'
    ELSE 'Low'
  END AS churn_risk
FROM customer
WHERE "Churn Label" = 'No';
"""
print("\n--- Risk Score for Active Customers (sample) ---")
risk_df = pd.read_sql_query(q9, db)
print(risk_df.head(10))
print("\nRisk distribution:")
print(risk_df['churn_risk'].value_counts())

db.close()