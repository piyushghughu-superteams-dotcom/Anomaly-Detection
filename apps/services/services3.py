from typing import Dict, Any
from case3_spam_transaction import detect_spam_transactions
from models.nlq_translator import translate_spam_transactions_to_nlq

class SpamTransactionService:
# case 3
    
    def __init__(self):
        pass
    
    def get_spam_transactions_nlq(self) -> str:
        try:
            spam_data = detect_spam_transactions()
            if not spam_data:
                return "No spam transactions detected in the system."
            nlq_result = translate_spam_transactions_to_nlq(spam_data)
            return nlq_result
        except Exception as e:
            return f"Error occurred while processing spam transactions: {str(e)}"
    
    def get_spam_transactions_json(self) -> list:
        try:
            return detect_spam_transactions()
        except Exception as e:
            return [{"error": f"Error occurred while fetching spam transactions: {str(e)}"}]

spam_transaction_service = SpamTransactionService()
