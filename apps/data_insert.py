# # generate_transactions.py
# import random
# from datetime import datetime, timedelta
# from db import get_connection

# # Config
# NUM_DAYS = 7        # previous 7 days
# MIN_TRANS = 50      # min transactions per day
# MAX_TRANS = 200     # max transactions per day
# MIN_PROD = 1        # min products per transaction
# MAX_PROD = 3        # max products per transaction
# MIN_QTY = 1         # min quantity per product
# MAX_QTY = 5         # max quantity per product

# def get_customers(cursor):
#     cursor.execute("SELECT customer_id FROM customers")
#     return [row['customer_id'] for row in cursor.fetchall()]

# def get_products(cursor):
#     cursor.execute("SELECT product_id, product_name, product_price FROM products")
#     return cursor.fetchall()

# def main():
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)

#     customers = get_customers(cursor)
#     products = get_products(cursor)

#     today = datetime.now()

#     for day_offset in range(1, NUM_DAYS + 1):
#         trans_date = today - timedelta(days=day_offset)
#         num_transactions = random.randint(MIN_TRANS, MAX_TRANS)

#         for _ in range(num_transactions):
#             customer_id = random.choice(customers)

#             # Insert transaction
#             cursor.execute("INSERT INTO transactions (customer_id, transaction_date, status) VALUES (%s, %s, 'SUCCESS')",
#                            (customer_id, trans_date))
#             conn.commit()
#             transaction_id = cursor.lastrowid

#             # Choose random products for this transaction
#             num_products = random.randint(MIN_PROD, MAX_PROD)
#             chosen_products = random.sample(products, num_products)

#             total_amount = 0
#             for prod in chosen_products:
#                 quantity = random.randint(MIN_QTY, MAX_QTY)
#                 total = prod['product_price'] * quantity
#                 total_amount += total

#                 cursor.execute("""
#                     INSERT INTO transaction_items 
#                     (transaction_id, product_id, product_name, product_price, quantity) 
#                     VALUES (%s, %s, %s, %s, %s)
#                 """, (transaction_id, prod['product_id'], prod['product_name'], prod['product_price'], quantity))

#             # Update total_amount in transactions table
#             cursor.execute("UPDATE transactions SET total_amount = %s WHERE transaction_id = %s", (total_amount, transaction_id))
#             conn.commit()

#     cursor.close()
#     conn.close()
#     print("Random transactions generated for the past week!")

# if __name__ == "__main__":
#     main()


# # generate_yearly_data.py

# import os
# import random
# from datetime import datetime, timedelta, date
# import mysql.connector
# from dotenv import load_dotenv

# load_dotenv()

# # --- Database Connection ---
# try:
#     db = mysql.connector.connect(
#         host=os.getenv("MYSQL_HOST"),
#         user=os.getenv("MYSQL_USER"),
#         password=os.getenv("MYSQL_PASSWORD"),
#         database=os.getenv("MYSQL_DB")
#     )
#     cursor = db.cursor(dictionary=True)
#     print("✅ Successfully connected to the database.")
# except mysql.connector.Error as err:
#     print(f"❌ Error connecting to database: {err}")
#     exit()

# def get_random_timestamp_for_day(day: date) -> datetime:
#     """Generates a random timestamp within a given day."""
#     return datetime.combine(day, datetime.min.time()) + timedelta(seconds=random.randint(32400, 72000)) # Business hours

# # --- Main Data Generation Logic ---
# def generate_yearly_data():
#     try:
#         cursor.execute("SELECT customer_id FROM customers")
#         customers = cursor.fetchall()
#         cursor.execute("SELECT product_id, product_name, product_price FROM products")
#         products = cursor.fetchall()

#         if not customers or not products:
#             print("❌ Cannot generate data. Add customers and products first.")
#             return

#         print("Preparing to generate data for the past year...")

#         # --- Define the Anomalies ---
#         # 1. Select 6 random days in the last year to have low sales
#         today = date.today()
#         days_in_year = [today - timedelta(days=i) for i in range(365)]
#         low_sale_days = set(random.sample(days_in_year, 6))
#         print(f"Selected {len(low_sale_days)} low-performance days.")

#         # 2. Select 1 random day for a spam attack
#         # Ensure it's not the same as a low_sale_day
#         available_days_for_spam = [d for d in days_in_year if d not in low_sale_days]
#         spam_day = random.choice(available_days_for_spam)
#         print(f"A spam transaction event will occur on: {spam_day}")

#         # --- Generate Data Day by Day ---
#         for current_day in reversed(days_in_year): # Go from past to present
#             if current_day in low_sale_days:
#                 num_transactions = random.randint(1, 5) # LOW volume
#                 print(f"-- Generating LOW sales for {current_day} ({num_transactions} transactions) --")
#             else:
#                 num_transactions = random.randint(50, 150) # NORMAL high volume
#                 if (len(days_in_year) - days_in_year.index(current_day)) % 30 == 0:
#                      print(f"-- Generating normal sales for {current_day} ({num_transactions} transactions) --")


#             # Generate the transactions for the current day
#             for _ in range(num_transactions):
#                 customer = random.choice(customers)
#                 product = random.choice(products)
#                 transaction_time = get_random_timestamp_for_day(current_day)
                
#                 cursor.execute("INSERT INTO transactions (customer_id, transaction_date, total_amount) VALUES (%s, %s, %s)",
#                                (customer['customer_id'], transaction_time, product['product_price']))
#                 transaction_id = cursor.lastrowid
                
#                 cursor.execute("""INSERT INTO transaction_items (transaction_id, product_id, product_name, product_price, quantity) 
#                                   VALUES (%s, %s, %s, %s, %s)""",
#                                (transaction_id, product['product_id'], product['product_name'], product['product_price'], 1))

#             # Inject the spam transaction event on the specified day
#             if current_day == spam_day:
#                 print(f"\n>>> Injecting SPAM transaction burst for {current_day}...")
#                 spam_customer = random.choice(customers)
#                 spam_product = random.choice(products)
#                 base_time = get_random_timestamp_for_day(current_day)
#                 for j in range(7): # Burst of 7 transactions
#                     spam_time = base_time + timedelta(seconds=j * 5)
#                     cursor.execute("INSERT INTO transactions (customer_id, transaction_date, total_amount) VALUES (%s, %s, %s)",
#                                    (spam_customer['customer_id'], spam_time, spam_product['product_price']))
#                     transaction_id = cursor.lastrowid
#                     cursor.execute("""INSERT INTO transaction_items (transaction_id, product_id, product_name, product_price, quantity) 
#                                       VALUES (%s, %s, %s, %s, %s)""",
#                                    (transaction_id, spam_product['product_id'], spam_product['product_name'], spam_product['product_price'], 1))
#                 print(">>> Spam burst created successfully.\n")

#         db.commit()
#         print("\n✅ Successfully generated one year of realistic transaction data.")

#     except mysql.connector.Error as err:
#         print(f"❌ A database error occurred: {err}")
#         db.rollback()
#     finally:
#         if db.is_connected():
#             cursor.close()
#             db.close()
#             print("Database connection closed.")


# if __name__ == "__main__":
#     generate_yearly_data()

# generate_spam.py

# import os
# import random
# from datetime import datetime, timedelta
# import mysql.connector
# from dotenv import load_dotenv

# load_dotenv()

# # --- Database Connection ---
# try:
#     db = mysql.connector.connect(
#         host=os.getenv("MYSQL_HOST"),
#         user=os.getenv("MYSQL_USER"),
#         password=os.getenv("MYSQL_PASSWORD"),
#         database=os.getenv("MYSQL_DB")
#     )
#     cursor = db.cursor(dictionary=True)
#     print("✅ Successfully connected to the database.")
# except mysql.connector.Error as err:
#     print(f"❌ Error connecting to database: {err}")
#     exit()

# def create_spam_burst(customer: dict, product: dict, num_transactions: int, base_time: datetime):
#     """Inserts a burst of transactions for a single customer."""
#     print(f"\n>>> Creating a spam burst of {num_transactions} transactions for customer ID {customer['customer_id']}...")
#     for i in range(num_transactions):
#         # Each transaction is 8 seconds apart, ensuring they are within one minute
#         spam_time = base_time + timedelta(seconds=i * 8)
        
#         # Insert the main transaction record
#         cursor.execute(
#             "INSERT INTO transactions (customer_id, transaction_date, total_amount) VALUES (%s, %s, %s)",
#             (customer['customer_id'], spam_time, product['product_price'])
#         )
#         transaction_id = cursor.lastrowid

#         # Insert the corresponding item record
#         cursor.execute(
#             """INSERT INTO transaction_items 
#                (transaction_id, product_id, product_name, product_price, quantity) 
#                VALUES (%s, %s, %s, %s, %s)""",
#             (transaction_id, product['product_id'], product['product_name'], product['product_price'], 1)
#         )
#     print(f">>> Spam burst created successfully.")


# # --- Main Logic ---
# def generate_spam_events():
#     try:
#         # 1. Fetch all available customers and products to choose from
#         cursor.execute("SELECT customer_id FROM customers")
#         customers = cursor.fetchall()
        
#         cursor.execute("SELECT product_id, product_name, product_price FROM products")
#         products = cursor.fetchall()

#         if len(customers) < 2 or not products:
#             print("❌ Cannot generate data. You need at least 2 customers and 1 product in your database.")
#             return

#         # 2. Select two DIFFERENT customers randomly
#         spam_customers = random.sample(customers, 2)
        
#         # --- Create Spam Event 1 ---
#         customer1 = spam_customers[0]
#         product1 = random.choice(products)
#         create_spam_burst(customer=customer1, product=product1, num_transactions=6, base_time=datetime.now())
        
#         # --- Create Spam Event 2 ---
#         customer2 = spam_customers[1]
#         product2 = random.choice(products)
#         # Use a slightly different time for the second event
#         event2_time = datetime.now() - timedelta(minutes=10)
#         create_spam_burst(customer=customer2, product=product2, num_transactions=7, base_time=event2_time)
        
#         db.commit() # Save all changes to the database
#         print("\n✅ Successfully generated and inserted 2 spam events.")

#     except mysql.connector.Error as err:
#         print(f"❌ A database error occurred: {err}")
#         db.rollback()
#     finally:
#         if db.is_connected():
#             cursor.close()
#             db.close()
#             print("Database connection closed.")


# # Run the function
# if __name__ == "__main__":
#     generate_spam_events()