# case4_failed_transactions.py

from db import get_connection

def get_failed_transactions():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        t.transaction_id,
        t.transaction_date,
        c.customer_id,
        c.customer_name,
        ti.product_name,
        t.total_amount
    FROM transactions t
    JOIN customers c ON t.customer_id = c.customer_id
    JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
    WHERE t.status = 'FAILED'
    ORDER BY t.transaction_date DESC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows