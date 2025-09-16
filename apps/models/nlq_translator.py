import json
import requests
import os
from dotenv import load_dotenv
from .prompt import CASE_1_PROMPT, CASE_2_PROMPT, CASE_3_PROMPT, CASE_4_PROMPT

load_dotenv()

def get_nlq_response(data, case_prompt, case_name):

    if not data:
        return f"No {case_name} detected in the system."
    
    try:
        api_key = os.getenv("AI_API_KEY")
        prompt = f"{case_prompt}\n\nData: {json.dumps(data, default=str)}"
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 2048
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"API Error {response.status_code}: {response.text}. Found {len(data)} {case_name}."
        
    except Exception as e:
        return f"Error: {str(e)}. Found {len(data)} {case_name}."

# Simple functions for each case
def translate_price_anomalies_to_nlq(anomalies):
    return get_nlq_response(anomalies, CASE_1_PROMPT, "price anomalies")

def translate_less_sale_days_to_nlq(sales_data):
    return get_nlq_response(sales_data, CASE_2_PROMPT, "less sale days")

def translate_spam_transactions_to_nlq(spam_data):
    return get_nlq_response(spam_data, CASE_3_PROMPT, "spam transactions")

# --- (CHANGE 2: Added the new function for Case 4) ---
def translate_failed_transactions_to_nlq(failed_data):
    """Handles the conversion for failed transactions."""
    return get_nlq_response(failed_data, CASE_4_PROMPT, "failed transactions")