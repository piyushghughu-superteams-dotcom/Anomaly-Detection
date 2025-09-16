# case1_price_anomalies.py
from db import get_connection

def check_price_anomalies():
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
        ti.product_id,
        ti.product_name,
        ti.product_price AS transaction_price,
        p.product_price AS actual_price,
        ti.quantity
    FROM transactions t
    JOIN customers c ON t.customer_id = c.customer_id
    JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
    JOIN products p ON ti.product_id = p.product_id
    WHERE ti.product_price < (p.product_price * 0.75)
    OR ti.product_price > (p.product_price * 1.05)
    ORDER BY t.transaction_id;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Group results by transaction
    result = {}
    for row in rows:
        tid = row["transaction_id"]
        if tid not in result:
            result[tid] = {
                "transaction_id": row["transaction_id"],
                "customer_id": row["customer_id"],
                "customer_name": row["customer_name"],
                "transaction_date": row["transaction_date"].isoformat() if row["transaction_date"] else None,
                "status": row["status"],
                "total_amount": float(row["total_amount"]),
                "products": [],
                "product_details": []
            }

        result[tid]["products"].append(row["product_name"])
        # include actual_price for clarity
        result[tid]["product_details"].append(
            f"{row['product_name']} ({row['quantity']} x {row['transaction_price']:.2f}, actual {row['actual_price']:.2f})"
        )

    # Format final output
    output = []
    for val in result.values():
        val["products"] = ", ".join(val["products"])
        val["product_details"] = ", ".join(val["product_details"])
        output.append(val)

    return output
