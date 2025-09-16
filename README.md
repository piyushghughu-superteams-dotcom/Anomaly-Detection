# Real-Time E-commerce Anomaly Detection System 🚀

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

Follow these steps to get the project running on your local machine.

### **1. Clone the Repository**
```bash
git clone <your-repository-url>
cd <your-repository-name>
```

### **2. Create and Activate a Virtual Environment**

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

### **3. Install Dependencies**
Install all the required Python packages from the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### **4. Set Up the Database**
Make sure your MySQL server is running and create a new database for the project.
```sql
CREATE DATABASE anology_superteams;
```
After creating the database, import the schema and any initial data from the provided `.sql` files.

### **5. Configure Environment Variables**
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

---

## ▶️ Running the Application

### **Start the FastAPI Server**
Run the following command in your terminal from the project's root directory.
```bash
uvicorn main:app --reload
```

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

```text
Transaction Failed: 2025-09-16 17:00:49 - Customer: Ian Clark (ID: 9) - Product: Monitor
Transaction Failed: 2025-09-16 16:57:35 - Customer: Eva Green (ID: 5) - Product: Printer
```
</details>
