import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

db = sqlite3.connect('churn_analysis.db')

# ============================================
# Chart 1: Churn Rate by Contract Type
# ============================================
q1 = """
SELECT Contract,
  ROUND(100.0 * SUM(CASE WHEN "Churn Label"='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_pct
FROM customer
GROUP BY Contract
ORDER BY churn_pct DESC;
"""
df1 = pd.read_sql_query(q1, db)

plt.figure(figsize=(6,4))
plt.bar(df1['Contract'], df1['churn_pct'], color='steelblue')
plt.title('Churn Rate by Contract Type')
plt.ylabel('Churn %')
plt.tight_layout()

# ============================================
# Chart 2: Churn Rate by Tenure Group
# ============================================
q2 = """
SELECT 
  CASE WHEN "Tenure Months" < 12 THEN 'New (<12mo)' ELSE 'Established (12mo+)' END AS tenure_group,
  ROUND(100.0 * SUM(CASE WHEN "Churn Label"='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_pct
FROM customer
GROUP BY tenure_group;
"""
df2 = pd.read_sql_query(q2, db)

plt.figure(figsize=(5,4))
plt.bar(df2['tenure_group'], df2['churn_pct'], color='coral')
plt.title('Churn Rate by Tenure Group')
plt.ylabel('Churn %')
plt.tight_layout()

# ============================================
# Chart 3: Avg Monthly Charges - Churned vs Retained
# ============================================
q3 = """
SELECT 
  "Churn Label",
  ROUND(AVG("Monthly Charges"), 2) AS avg_monthly_charge
FROM customer
GROUP BY "Churn Label";
"""
df3 = pd.read_sql_query(q3, db)

plt.figure(figsize=(4,4))
plt.bar(df3['Churn Label'], df3['avg_monthly_charge'], color='seagreen')
plt.title('Avg Monthly Charges: Churned vs Retained')
plt.ylabel('Avg Monthly Charges ($)')
plt.tight_layout()

# ============================================
# Chart 4: Top 10 Churn Reasons
# ============================================
q4 = """
SELECT 
  "Churn Reason",
  COUNT(*) AS count
FROM customer
WHERE "Churn Label" = 'Yes' AND "Churn Reason" IS NOT NULL AND "Churn Reason" != ''
GROUP BY "Churn Reason"
ORDER BY count DESC
LIMIT 10;
"""
df4 = pd.read_sql_query(q4, db)

plt.figure(figsize=(7,5))
plt.barh(df4['Churn Reason'], df4['count'], color='darkorange')
plt.title('Top 10 Churn Reasons')
plt.xlabel('Number of Customers')
plt.gca().invert_yaxis()
plt.tight_layout()

db.close()

# Show all charts at once
plt.show()