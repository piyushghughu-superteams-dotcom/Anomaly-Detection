from db import get_connection

def get_transaction_report():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        t.transaction_id,
        t.customer_id,
        c.customer_name,
        t.transaction_date,
        t.status,
        t.total_amount,
        GROUP_CONCAT(ti.product_name SEPARATOR ', ') AS products,
        GROUP_CONCAT(CONCAT(ti.product_name, ' (', ti.quantity, ' x ', ti.product_price, ')') SEPARATOR ', ') AS product_details
    FROM transactions t
    JOIN customers c ON t.customer_id = c.customer_id
    JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
    GROUP BY 
        t.transaction_id, 
        t.customer_id, 
        c.customer_name, 
        t.transaction_date, 
        t.status, 
        t.total_amount
    ORDER BY t.transaction_id;
    """

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    return result
