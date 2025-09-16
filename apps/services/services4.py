# services/services4.py

from typing import List, Dict, Any
from case4_payment_fail import get_failed_transactions
from models.nlq_translator import translate_failed_transactions_to_nlq

class FailedTransactionService:
    def __init__(self):
        pass
    
    def get_failed_transactions_nlq(self) -> str:
        try:
            failed_data = get_failed_transactions()
            if not failed_data:
                return "No failed transactions found in the system."

            nlq_result = translate_failed_transactions_to_nlq(failed_data)
            return nlq_result
        except Exception as e:
            return f"Error occurred while processing failed transactions: {str(e)}"
    
    def get_failed_transactions_json(self) -> List[Dict[str, Any]]:
        try:
            return get_failed_transactions()
        except Exception as e:
            return [{"error": f"Error occurred while fetching failed transactions: {str(e)}"}]

failed_transaction_service = FailedTransactionService()