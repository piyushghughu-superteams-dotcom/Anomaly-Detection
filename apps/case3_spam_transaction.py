# case3_spam_transaction.py

from db import get_connection

def detect_spam_transactions():
    """
    Detects spam transactions where a customer makes more than 5 
    transactions within the same minute.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        t.customer_id,
        c.customer_name,
        DATE(t.transaction_date) AS txn_day,
        HOUR(t.transaction_date) AS txn_hour,
        MINUTE(t.transaction_date) AS txn_minute,
        COUNT(*) AS txn_count
    FROM transactions t
    JOIN customers c ON t.customer_id = c.customer_id
    GROUP BY t.customer_id, txn_day, txn_hour, txn_minute
    HAVING COUNT(*) > 5
    ORDER BY t.customer_id, txn_day, txn_hour, txn_minute;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    conn.close()
    return rows