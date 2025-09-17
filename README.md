# Real-Time Fraud & Anomaly Detection Platform 🛡️

A powerful backend application built with **FastAPI** and **MySQL** to monitor e-commerce transactions in real-time. This system leverages a **Large Language Model (LLM)** to detect and report on various anomalies, providing clear, human-readable insights through a live, auto-updating dashboard.

---

## 📋 Table of Contents

- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Setup and Installation](#-setup-and-installation)
- [Running the Application](#️-running-the-application)
- [API Endpoints & Sample Outputs](#-api-endpoints--sample-outputs)

---

## ✨ Key Features

This system is designed to detect four critical types of anomalies:

* **Price Anomaly Detection:** Flags transactions where products are sold at suspiciously high or low prices.
* **Sales Volume Anomaly Detection:** Identifies days with unusually low transaction counts or revenue.
* **Spam/Fraud Detection:** Detects rapid, repeated transactions from a single user, indicating bot activity.
* **Failed Transaction Monitoring:** Tracks and reports all failed payment attempts.
* **Real-Time Dashboard:** A WebSocket-powered frontend (`index.html`) that displays live updates from all monitors.

---

## ⚙️ Technology Stack

* **Backend:** Python, FastAPI
* **Database:** MySQL
* **Real-Time Communication:** WebSockets
* **Natural Language Insights:** Groq / OpenAI LLMs
* **Python Libraries:** `uvicorn`, `mysql-connector-python`, `python-dotenv`, `requests`

---

## 🔧 Setup and Installation

Follow these steps in order to get the project running on your local machine.

### **Step 1: Prerequisites**
- Python 3.10+
- MySQL Server

### **Step 2: Clone the Repository**
```bash
git clone <your-repository-url>
cd <your-repository-name>
```

### **Step 3: Create and Activate a Virtual Environment**

* **For Linux/macOS:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
* **For Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

### **Step 4: Install Dependencies**
Install all the required Python packages from the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### **Step 5: Configure Environment Variables**
Create a file named `.env` in the root of the project folder and add your credentials.

**`.env` file contents:**
```ini
MYSQL_HOST=localhost
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=anology_superteams

# Your API Key from Groq or another LLM provider
AI_API_KEY="gsk_YourSecretKeyGoesHere"
```

### **Step 6: Set Up the Database**
First, make sure your MySQL server is running. Then, run the provided SQL script to create all the necessary tables and insert sample data.

<details>
<summary>Click to view the complete `setup.sql` script</summary>

```sql
-- Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS anology_superteams;

-- Switch to the new database
USE anology_superteams;

-- =============================================
-- STEP 1: CREATE THE TABLES
-- =============================================

-- Table: customers
-- Stores information about each unique customer.
CREATE TABLE IF NOT EXISTS `customers` (
  `customer_id` bigint NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(255) NOT NULL,
  `mobile_number` varchar(20) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `pincode` varchar(20) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `mobile_number` (`mobile_number`)
);

-- Table: products
-- Stores the product catalog with their standard prices.
CREATE TABLE IF NOT EXISTS `products` (
  `product_id` varchar(20) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `product_price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`product_id`)
);

-- Table: transactions
-- The main table that records every transaction event.
CREATE TABLE IF NOT EXISTS `transactions` (
  `transaction_id` bigint NOT NULL AUTO_INCREMENT,
  `customer_id` bigint NOT NULL,
  `transaction_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` enum('SUCCESS','FAILED') DEFAULT 'SUCCESS',
  `total_amount` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`transaction_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
);

-- Table: transaction_items
-- A child table that lists the specific products included in each transaction.
CREATE TABLE IF NOT EXISTS `transaction_items` (
  `item_id` bigint NOT NULL AUTO_INCREMENT,
  `transaction_id` bigint NOT NULL,
  `product_id` varchar(20) NOT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `product_price` decimal(10,2) DEFAULT NULL,
  `quantity` int DEFAULT '1',
  PRIMARY KEY (`item_id`),
  KEY `transaction_id` (`transaction_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `transaction_items_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `transactions` (`transaction_id`),
  CONSTRAINT `transaction_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
);


-- =============================================
-- STEP 2: INSERT SAMPLE DATA
-- =============================================

-- Insert data into customers table
INSERT INTO `customers` (`customer_id`, `customer_name`, `mobile_number`, `email`, `city`, `state`, `pincode`, `country`) VALUES
(1, 'Alice Johnson', '9876543210', 'alice.j@example.com', 'Mumbai', 'Maharashtra', '400001', 'India'),
(2, 'Bob Smith', '9876543211', 'bob.s@example.com', 'Delhi', 'Delhi', '110001', 'India'),
(3, 'Charlie Brown', '9876543212', 'charlie.b@example.com', 'Bangalore', 'Karnataka', '560001', 'India'),
(4, 'David Williams', '9876543213', 'david.w@example.com', 'Kolkata', 'West Bengal', '700001', 'India');

-- Insert data into products table
INSERT INTO `products` (`product_id`, `product_name`, `product_price`) VALUES
('prod1001', 'Laptop', 50000.00),
('prod1002', 'Smartphone', 20000.00),
('prod1003', 'Headphones', 2000.00),
('prod1004', 'Keyboard', 1000.00),
('prod1005', 'Mouse', 500.00);

-- Insert a successful single-item transaction for Alice Johnson
INSERT INTO `transactions` (customer_id, status, total_amount) VALUES (1, 'SUCCESS', 50000.00);
SET @last_txn_id = LAST_INSERT_ID();
INSERT INTO `transaction_items` (transaction_id, product_id, product_name, product_price, quantity)
VALUES (@last_txn_id, 'prod1001', 'Laptop', 50000.00, 1);

-- Insert a successful multi-item transaction for Bob Smith
INSERT INTO `transactions` (customer_id, status, total_amount) VALUES (2, 'SUCCESS', 1500.00);
SET @last_txn_id = LAST_INSERT_ID();
INSERT INTO `transaction_items` (transaction_id, product_id, product_name, product_price, quantity)
VALUES 
  (@last_txn_id, 'prod1004', 'Keyboard', 1000.00, 1),
  (@last_txn_id, 'prod1005', 'Mouse', 500.00, 1);

-- Insert a failed transaction for Charlie Brown
INSERT INTO `transactions` (customer_id, status, total_amount) VALUES (3, 'FAILED', 20000.00);
SET @last_txn_id = LAST_INSERT_ID();
INSERT INTO `transaction_items` (transaction_id, product_id, product_name, product_price, quantity)
VALUES (@last_txn_id, 'prod1002', 'Smartphone', 20000.00, 1);

SELECT 'Tables created and sample data inserted successfully.' AS status;
```
</details>

To run the script, save it as `setup.sql` and use the MySQL command line:
```bash
mysql -u your_mysql_username -p < setup.sql
```

---

## ▶️ Running the Application

### **1. Start the FastAPI Server**
Run the following command in your terminal from the project's root directory.
```bash
uvicorn main:app --reload
```
### **2. View the Live Dashboard**
Open the `index.html` file in your web browser. The dashboard will automatically connect to the server and start displaying live data.

---

## 📡 API Endpoints & Sample Outputs

Here are the primary API endpoints and examples of the natural language summaries they produce.

### **Price Anomaly Detection**
`GET /price_anomalies` - Detects transactions with unusual sale prices.

<details>
<summary>Click to see sample output</summary>

```text
Transaction ID 921: Customer Alice Johnson (ID: 1) purchased Laptop on September 16, 2025. The product has an actual catalog price of ₹50000.00 but was sold for ₹500.00, resulting in a 99.0% discount. This represents a CRITICAL price anomaly - significant revenue loss.
Transaction ID 923: Customer Charlie Brown (ID: 3) purchased Headphones on September 16, 2025. The product has an actual catalog price of ₹2000.00 but was sold for ₹2500.00, resulting in a 25.0% markup. This represents a HIGH price anomaly - customer overcharged.
Transaction ID 924: Customer David Williams (ID: 4) purchased Keyboard, Webcam on September 16, 2025. The products have actual catalog prices of ₹1000.00, ₹1200.00 but were sold for ₹100.00, ₹120.00, resulting in a 90.0%, 90.0% discount. This represents a CRITICAL price anomaly - significant revenue loss.
```
</details>

### **Sales Volume Anomaly Detection**
`GET /less-sale-nlq` - Identifies days with below-average sales volume.

<details>
<summary>Click to see sample output</summary>

```text
September 3, 2025: 78 transactions, ₹870,400 sales - low performance
September 6, 2025: 52 transactions, ₹446,900 sales - low performance
September 10, 2025: 60 transactions, ₹663,900 sales - low performance
```
</details>

### **Spam Transaction Detection**
`GET /spam-transactions-nlq` - Detects rapid transactions from a single user.

<details>
<summary>Click to see sample output</summary>

```text
Customer Quentin Fox (ID: 17) made 6 transactions on September 16, 2025 at 16:31 - suspicious activity detected
Customer Rachel Stone (ID: 18) made 6 transactions on September 16, 2025 at 16:41 - suspicious activity detected
```
</details>

### **Failed Transaction Reporting**
`GET /failed-transactions-nlq` - Reports all failed transactions.

<details>
<summary>Click to see sample output</summary>

<p><strong>This blog was written in collaboration with <a href="https://www.superteams.ai">Superteams.ai</a></strong></p>

```text
Transaction Failed: 2025-09-16 17:00:49 - Customer: Ian Clark (ID: 9) - Product: Monitor
Transaction Failed: 2025-09-16 16:57:35 - Customer: Eva Green (ID: 5) - Product: Printer
```
</details>
