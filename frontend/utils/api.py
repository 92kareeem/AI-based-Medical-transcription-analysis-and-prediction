import requests
from typing import Optional, Dict
import streamlit as st

class MedAPI:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
    
    def analyze_text(self, text: str) -> Optional[Dict]:
        """Send conversation text to backend NLP pipeline"""
        try:
            response = requests.post(
                f"{self.base_url}/analyze",
                json={"text": text},
                timeout=30
            )
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.exceptions.ConnectionError:
            raise Exception("Failed to connect to the backend. Ensure the backend is running.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Error: {str(e)}")

# Create a global instance for easy access
api_client = MedAPI()

# Expose the analyze_text function
def analyze_text(text: str) -> Optional[Dict]:
    """Wrapper function for analyzing text"""
    return api_client.analyze_text(text)