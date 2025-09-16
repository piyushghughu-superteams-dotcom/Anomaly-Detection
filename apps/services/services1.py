from typing import Dict, Any
from case1_price_anomalies import check_price_anomalies
from models.nlq_translator import translate_price_anomalies_to_nlq

class PriceAnomalyService:
#    case 1
    
    def __init__(self):
        pass
    
    def get_price_anomalies_nlq(self) -> str:
        try:
            anomalies_data = check_price_anomalies()
            if not anomalies_data:
                return "No price anomalies detected in the system."
            nlq_result = translate_price_anomalies_to_nlq(anomalies_data)
            return nlq_result
        except Exception as e:
            return f"Error occurred while processing price anomalies: {str(e)}"
    
    def get_price_anomalies_json(self) -> list:
        """Get price anomalies in JSON format"""
        try:
            return check_price_anomalies()
        except Exception as e:
            return [{"error": f"Error occurred while fetching price anomalies: {str(e)}"}]

# Create a singleton instance for easy import
price_anomaly_service = PriceAnomalyService()