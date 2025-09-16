from db import get_connection

def less_sale_days():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        transaction_day,
        total_transactions,
        total_amount_per_day
    FROM (
        SELECT 
            DATE(transaction_date) AS transaction_day,
            COUNT(*) AS total_transactions,
            SUM(total_amount) AS total_amount_per_day,
            AVG(COUNT(*)) OVER () AS avg_transactions,
            AVG(SUM(total_amount)) OVER () AS avg_amount
        FROM transactions
        GROUP BY DATE(transaction_date)
    ) t
    WHERE total_transactions < avg_transactions
    ORDER BY transaction_day;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows