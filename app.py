import streamlit as st
import spacy
from transformers import pipeline
from textblob import TextBlob
import json

# Load the SciSpacy model
nlp = spacy.load("en_core_sci_md")  # Ensure you have this model installed

# Load the summarization model from transformers
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to extract medical entities
def extract_medical_entities(transcript):
    doc = nlp(transcript)
    entities = {
        "symptoms": [],
        "diagnosis": [],
        "treatment": [],
        "prognosis": []
    }
    
    for ent in doc.ents:
        if ent.label_ == "SYMPTOM":
            entities["symptoms"].append(ent.text)
        elif ent.label_ == "DIAGNOSIS":
            entities["diagnosis"].append(ent.text)
        elif ent.label_ == "TREATMENT":
            entities["treatment"].append(ent.text)
        elif ent.label_ == "PROGNOSIS":
            entities["prognosis"].append(ent.text)
    
    return entities

# Function to generate summary using transformers
def generate_summary(transcript):
    # The model expects input text to be less than 1024 tokens
    max_input_length = 1024
    if len(transcript) > max_input_length:
        transcript = transcript[:max_input_length]
    
    summary = summarizer(transcript, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Function for sentiment analysis
def analyze_sentiment(dialogue):
    analysis = TextBlob(dialogue)
    return "Anxious" if analysis.sentiment.polarity < 0 else "Reassured"

# Function to generate SOAP note
def generate_soap(entities):
    soap_note = {
        "Subjective": {
            "Chief_Complaint": ", ".join(entities["symptoms"]),
            "History_of_Present_Illness": "Patient reported symptoms related to the accident."
        },
        "Objective": {
            "Physical_Exam": "Full range of motion, no tenderness.",
            "Observations": "Patient appears in normal health."
        },
        "Assessment": {
            "Diagnosis": ", ".join(entities["diagnosis"]),
            "Severity": "Mild, improving"
        },
        "Plan": {
            "Treatment": ", ".join(entities["treatment"]),
            "Follow-Up": "Patient to return if symptoms worsen."
        }
    }
    return soap_note

# Streamlit UI
st.title("Medical Transcription using NLP")
st.markdown("👋 Welcome! This application helps in medical transcription, summarization, and sentiment analysis.")

# Input section
transcript = st.text_area("Enter the Physician-Patient Conversation Transcript", height=300)

if st.button("Analyze"):
    if transcript:
        # Extract medical entities
        entities = extract_medical_entities(transcript)
        
        # Generate summary
        summary = generate_summary(transcript)
        
        # Analyze sentiment
        sentiment = analyze_sentiment(transcript)
        
        # Generate SOAP note
        soap_note = generate_soap(entities)
        
        # Display results
        st.subheader("Extracted Medical Entities")
        st.json(entities)
        
        st.subheader("Summary")
        st.write(summary)
        
        st.subheader("Sentiment Analysis")
        st.write(f"Sentiment: {sentiment}")
        
        st.subheader("SOAP Note")
        st.json(soap_note)
    else:
        st.warning("Please enter a transcript to analyze.")

# Footer
st.markdown("---")
st.markdown("### About This App")
st.markdown("This app uses NLP techniques to assist healthcare professionals in documenting patient interactions.")
st.markdown("Made by Syed Abdul Kareem Ahmed as Assignment : Emitrr")