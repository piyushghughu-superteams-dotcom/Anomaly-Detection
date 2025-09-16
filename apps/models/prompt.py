# app/models/prompts.py

CASE_1_PROMPT = """
You are analyzing price anomaly data. You must process EVERY SINGLE TRANSACTION in the data.

For each price anomaly transaction, write one line in this exact format:
"Transaction ID [ID]: Customer [NAME] (ID: [CUSTOMER_ID]) purchased [PRODUCT] on [DATE]. The product has an actual catalog price of ₹[ACTUAL_PRICE] but was sold for ₹[TRANSACTION_PRICE], resulting in a [PERCENTAGE]% [DISCOUNT/MARKUP]. This represents a [SEVERITY] price anomaly - [IMPACT]."

WHERE:
- [ID] = transaction_id
- [NAME] = customer_name  
- [CUSTOMER_ID] = customer_id
- [PRODUCT] = product_name
- [DATE] = format transaction_date as "September 12, 2025"
- [ACTUAL_PRICE] = actual_price with 2 decimals
- [TRANSACTION_PRICE] = transaction_price with 2 decimals
- [PERCENTAGE] = calculate percentage difference (round to 1 decimal)
- [DISCOUNT/MARKUP] = "discount" if transaction_price < actual_price, "markup" if higher
- [SEVERITY] = "CRITICAL" if >50% difference, "HIGH" if 25-50%, "MODERATE" if 10-25%
- [IMPACT] = "significant revenue loss" for underpricing, "customer overcharged" for overpricing

CRITICAL: You must output ALL transactions from the data. Do not skip any. Do not summarize.
If the data contains 9 transactions, you MUST write exactly 9 lines.

Example:
Transaction ID 904: Customer Eva Green (ID: 5) purchased Mouse on September 12, 2025. The product has an actual catalog price of ₹500.00 but was sold for ₹68.00, resulting in a 86.4% discount. This represents a CRITICAL price anomaly - significant revenue loss.
"""


CASE_2_PROMPT = """
You are analyzing daily sales data. You must process EVERY SINGLE DAY in the data.

For each low-performing day, write one line in this exact format:
"[DATE]: [TRANSACTIONS] transactions, ₹[AMOUNT] sales - low performance"

WHERE:
- [DATE] = convert transaction_day (2025-09-15) to "September 15, 2025" format
- [TRANSACTIONS] = total_transactions number
- [AMOUNT] = total_amount_per_day with commas

CRITICAL: You must output ALL days from the data. Do not skip any. Do not summarize.
If the data contains 5 days, you MUST write exactly 5 lines.

Example for multiple days:
September 8, 2025: 77 transactions, ₹3,544,100 sales - low performance
September 13, 2025: 80 transactions, ₹5,333,700 sales - low performance
September 14, 2025: 60 transactions, ₹2,976,800 sales - low performance
September 15, 2025: 17 transactions, ₹333,200 sales - low performance
September 16, 2025: 4 transactions, ₹3,570 sales - low performance
"""

CASE_3_PROMPT = """
You are analyzing spam transaction data. You must process EVERY SINGLE SPAM INCIDENT in the data.

For each spam incident, write one line in this exact format:
"Customer [NAME] (ID: [ID]) made [COUNT] transactions on [DATE] at [TIME] - suspicious activity detected"

WHERE:
- [NAME] = customer_name from the data
- [ID] = customer_id from the data  
- [COUNT] = txn_count from the data
- [DATE] = format txn_day as "September 11, 2025"
- [TIME] = format txn_hour:txn_minute as "17:02"

CRITICAL: You must output ALL spam incidents from the data. Do not group by customer. Do not summarize.
If the data contains 57 spam incidents, you MUST write exactly 57 lines.
Each incident (different day/time) gets its own line, even for the same customer.

Example:
Customer Alice Johnson (ID: 1) made 8 transactions on September 8, 2025 at 17:02 - suspicious activity detected
Customer Alice Johnson (ID: 1) made 11 transactions on September 11, 2025 at 17:02 - suspicious activity detected
Customer Alice Johnson (ID: 1) made 7 transactions on September 12, 2025 at 17:02 - suspicious activity detected
"""


CASE_4_PROMPT = """
You are a transaction reporting bot. Your only job is to list failed transactions.
For EACH transaction in the provided JSON data, create a single-line summary.
Do not add any extra analysis, introductory sentences, or conclusions.

Follow this template exactly for each line:
Transaction Failed: [Date and Time] - Customer: [Customer Name] (ID: [Customer ID]) - Product: [Product Name]

Example:
Transaction Failed: 2025-09-16 17:30:15 - Customer: Eva Green (ID: 5) - Product: Printer
"""