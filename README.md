# Customer Churn Analysis — Telco Dataset

## Overview
This project analyzes customer churn patterns using the IBM Telco Customer Churn dataset. The goal is to identify which customer segments are most likely to churn, understand the business drivers behind churn, and build a rule-based risk-scoring system to flag active customers who are likely to leave.

This type of analysis is common in telecom and subscription-based businesses, where reducing churn directly improves revenue and customer lifetime value.

## Dataset
- Source: IBM Telco Customer Churn (Kaggle)
- Size: 7,043 customers and 33 columns
- Key fields: contract type, tenure, monthly charges, total charges, services subscribed, churn label, churn reason, and CLTV

## Tech Stack
- Python
- pandas
- sqlite3
- matplotlib
- SQLite for analytical querying

SQL concepts used in the analysis include:
- CASE WHEN logic
- aggregate functions
- GROUP BY
- subqueries
- CTEs (Common Table Expressions)

## Project Structure
```text
Customer Churn Analysis/
├── churn_analysis.db          # SQLite database created from the CSV
├── main.py                    # Loads CSV into SQLite and runs analysis queries
├── visualize.py               # Generates charts for key churn insights
├── Telco_customer_churn.csv   # Raw dataset
└── README.md
```

## How to Run
```bash
python main.py
python visualize.py
```

## Business Questions Answered
1. What is the overall customer churn rate?
2. Which contract type has the highest churn rate?
3. What is the average monthly charge for churned vs. retained customers?
4. Are customers with less than 12 months of tenure more likely to churn?
5. What are the top reasons customers give for leaving?
6. What is the average Customer Lifetime Value (CLTV) for churned vs. retained customers?
7. Can we assign a churn-risk label to currently active customers?

## Key Findings

| Metric | Value |
|---|---:|
| Overall churn rate | 26.54% |
| Month-to-month contract churn rate | 42.71% |
| Two-year contract churn rate | 2.83% |
| Churn rate for customers with <12 months tenure | 48.28% |
| Churn rate for customers with 12+ months tenure | 17.49% |
| Avg monthly charge (churned) | $74.44 |
| Avg monthly charge (retained) | $61.27 |
| Avg CLTV (churned) | $4,149 |
| Avg CLTV (retained) | $4,491 |

### Top churn reasons
1. Attitude of support person
2. Competitor offered higher download speeds
3. Competitor offered more data
4. Competitor made better offer
5. Attitude of service provider

## Insights and Recommendations
- Contract type is the strongest churn predictor. Month-to-month customers churn at nearly 15x the rate of two-year customers.
- New customers are high-risk. Nearly half of customers with under 12 months of tenure churn.
- Churn is not driven only by price. Customer support experience appears to be a major driver.
- High-value customers are also at risk, which makes retention efforts financially important.

## Stretch Goal: Churn Risk Scoring
A rule-based risk score is assigned to currently active customers using CASE WHEN logic based on tenure, monthly charges, and contract type.

Example logic:
```sql
CASE
  WHEN "Tenure Months" < 12 AND Contract = 'Month-to-month' AND "Monthly Charges" > 70 THEN 'High'
  WHEN "Tenure Months" BETWEEN 12 AND 24 AND Contract = 'Month-to-month' THEN 'Medium'
  ELSE 'Low'
END AS churn_risk
```

This flags a targeted group of at-risk customers for retention outreach rather than applying a broad campaign to the entire customer base.

## Limitations
- The dataset is limited to customers in California, so region-level comparisons were not possible.
- Tenure is recorded in months rather than actual signup dates, so calendar-time cohort analysis is limited.

## Future Improvements
- Build a true cohort analysis using a dataset with signup and churn dates
- Train a supervised machine-learning model and compare it with the rule-based score
- Expand the analysis to a multi-region dataset
