import requests
from typing import Dict, List

class MedicalSummarizer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.summarization_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def generate_summary(self, text: str) -> Dict:
        """Generate a medical summary using Hugging Face's API."""
        payload = {
            "inputs": text,
            "parameters": {
                "max_length": 150,
                "min_length": 30,
                "do_sample": False
            }
        }
        
        try:
            response = requests.post(
                self.summarization_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            summary = response.json()[0]['summary_text']
            
            return {
                "diagnosis": self._extract_diagnosis(summary),
                "prognosis": self._extract_prognosis(summary),
                "summary_text": summary
            }
        except Exception as e:
            raise Exception(f"Failed to generate summary: {str(e)}")

    def _extract_diagnosis(self, text: str) -> str:
        """Extract diagnosis from the summary text."""
        return "Whiplash injury" if "whiplash" in text.lower() else "Unknown"

    def _extract_prognosis(self, text: str) -> str:
        """Extract prognosis from the summary text."""
        if "improve" in text.lower():
            return "Positive prognosis"
        return "Requires monitoring"