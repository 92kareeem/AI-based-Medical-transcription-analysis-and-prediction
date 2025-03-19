import requests
from typing import Dict, List

class ClinicalNER:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.ner_url = "https://api-inference.huggingface.co/models/dslim/bert-base-NER"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract medical entities using Hugging Face's NER API."""
        payload = {"inputs": text}
        
        try:
            # Send request to Hugging Face API
            response = requests.post(
                self.ner_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()  # Raise an error for bad status codes
            entities = response.json()
            
            # Map Hugging Face entities to medical categories
            result = {
                "symptoms": [],
                "diagnosis": [],
                "treatment": [],
                "drugs": []
            }
            
            for entity in entities:
                if entity['entity_group'] == "PER":
                    continue  # Skip person names
                elif entity['entity_group'] == "ORG":
                    result["treatment"].append(entity['word'])
                elif entity['entity_group'] == "MISC":
                    result["drugs"].append(entity['word'])
                else:
                    result["symptoms"].append(entity['word'])
            
            return result
        except Exception as e:
            raise Exception(f"Failed to extract entities: {str(e)}")