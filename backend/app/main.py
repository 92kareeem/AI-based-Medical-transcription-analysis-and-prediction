from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.nlp.clinical_ner import ClinicalNER
from app.nlp.summarizer import MedicalSummarizer
from app.nlp.sentiment import ClinicalSentimentAnalyzer
from utils.config import settings

app = FastAPI(title="MedNLP Engine", version="1.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models at startup
ner = ClinicalNER(api_key="your_hugging_face_api_key")
summarizer = MedicalSummarizer(api_key="your_hugging_face_api_key")
sentiment_analyzer = ClinicalSentimentAnalyzer(api_key="your_hugging_face_api_key")

class AnalysisRequest(BaseModel):
    text: str
    detailed: bool = False

@app.post("/analyze")
async def analyze_text(request: AnalysisRequest):
    try:
        # Process with all components
        entities = ner.extract_entities(request.text)
        summary = summarizer.generate_summary(request.text)
        sentiment = sentiment_analyzer.analyze(request.text)
        
        return {
            "entities": entities,
            "summary": summary,
            "sentiment": sentiment,
            "soap": generate_soap(entities, summary)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_soap(entities, summary):
    return {
        "Subjective": {"symptoms": entities["symptoms"]},
        "Objective": {"diagnosis": summary["diagnosis"]},
        "Assessment": {"prognosis": summary["prognosis"]},
        "Plan": {"treatment": entities["treatment"]}
    }
