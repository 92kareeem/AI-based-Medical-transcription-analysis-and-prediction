import requests
from typing import Dict

class ClinicalSentimentAnalyzer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.sentiment_url = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def analyze(self, text: str) -> Dict:
        """Analyze sentiment using Hugging Face's API."""
        payload = {"inputs": text}
        
        try:
            response = requests.post(
                self.sentiment_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            sentiment_data = response.json()[0]
            
            # Extract the highest confidence sentiment
            sentiment = max(sentiment_data, key=lambda x: x['score'])
            return {
                "label": sentiment['label'],
                "score": sentiment['score']
            }
        except Exception as e:
            raise Exception(f"Failed to analyze sentiment: {str(e)}")