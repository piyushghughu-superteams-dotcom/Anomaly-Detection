from typing import Dict, Any
from case2_less_sale import less_sale_days
from models.nlq_translator import translate_less_sale_days_to_nlq

class LessSaleDaysService:
# case 2
    def __init__(self):
        pass
    
    def get_less_sale_days_nlq(self) -> str:
        try:
            sales_data = less_sale_days()
            if not sales_data:
                return "No less transactions detected in the system."
            nlq_result = translate_less_sale_days_to_nlq(sales_data)
            return nlq_result
        except Exception as e:
            return f"Error occurred while processing less sale days: {str(e)}"
    
    def get_less_sale_days_json(self) -> list:
        try:
            return less_sale_days()
        except Exception as e:
            return [{"error": f"Error occurred while fetching less sale days: {str(e)}"}]
less_sale_days_service = LessSaleDaysService()
