from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from db import get_connection
from report import get_transaction_report
from case1_price_anomalies import check_price_anomalies
from case2_less_sale import less_sale_days
from case3_spam_transaction import detect_spam_transactions
from services.services1 import price_anomaly_service
from services.services2 import less_sale_days_service
from services.services3 import spam_transaction_service
from services.services4 import failed_transaction_service 

app = FastAPI()
@app.get("/")
def home():
    return "Hello, World!"

@app.get("/report")
def transaction_report():
    return get_transaction_report()


# @app.get("/price_anomalies")
# def price_anomalies():
#     return check_price_anomalies()


# @app.get("/less-sale")
# def get_less_sale():
#     result = less_sale_days()
#     return result

# @app.get("/price_anomalies_json")
# def price_anomalies_json():
#     """Get price anomalies in JSON format"""
#     return price_anomaly_service.get_price_anomalies_json()


# @app.get("/spam-transactions")
# def spam_transactions():
#     return detect_spam_transactions()

@app.get("/price_anomalies", response_class=PlainTextResponse)
def price_anomalies_nlq():
    """Get price anomalies in natural language format"""
    return price_anomaly_service.get_price_anomalies_nlq()


@app.get("/less-sale-nlq", response_class=PlainTextResponse)
def get_less_sale_nlq():
    """Get less sale days in natural language format"""
    return less_sale_days_service.get_less_sale_days_nlq()


@app.get("/spam-transactions-nlq", response_class=PlainTextResponse)
def spam_transactions_nlq():
    """Get spam transactions in natural language format"""
    return spam_transaction_service.get_spam_transactions_nlq()

@app.get("/failed-transactions-nlq", response_class=PlainTextResponse)
def failed_transactions_nlq():
    """Get failed transactions in natural language format"""
    return failed_transaction_service.get_failed_transactions_nlq()


