import streamlit as st
from streamlit_webrtc import webrtc_streamer
import assemblyai as aai
import spacy
from transformers import pipeline
import time
import os
import plotly.graph_objects as go

# Set AssemblyAI API key
aai.settings.api_key = "your_assemblyai_api_key"  # Replace with your AssemblyAI API key

# Load spaCy model
nlp = spacy.load("en_core_sci_sm")  # Using SciSpacy as an alternative

# Load Hugging Face sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

# Custom CSS for Vision UI-inspired styling
st.markdown(
    """
    <style>
    /* Main container styling */
    .main {
        background-color: #f8f9fa;
        padding: 20px;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(195deg, rgb(73, 163, 241), rgb(26, 115, 232));
        color: white;
        padding: 20px;
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(195deg, #49a3f1, #1a73e8);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
    }
    
    /* Progress bar styling */
    .stProgress>div>div>div {
        background: linear-gradient(90deg, #49a3f1, #1a73e8);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "soap_note" not in st.session_state:
    st.session_state.soap_note = {}

# Sidebar
with st.sidebar:
    st.markdown("## Settings")
    st.selectbox("Theme", ["Light", "Dark"])
    st.slider("Font Size", 12, 24, 16)
    st.markdown("---")
    st.markdown("## User Profile")
    st.image("https://via.placeholder.com/80", width=80)  # Placeholder avatar
    st.markdown("**Dr. John Smith**  \nNeurologist")

# Main dashboard
st.title("Medical Transcription Dashboard")
st.markdown("### Real-Time Patient Analysis")

# Audio recording section
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="card"><h3>Patient Recording</h3></div>', unsafe_allow_html=True)
    webrtc_ctx = webrtc_streamer(key="audio-recorder", audio_receiver_size=1024)

# Real-time transcription and analysis
if webrtc_ctx.audio_receiver:
    with st.spinner("Analyzing in real-time..."):
        audio_frames = []
        for frame in webrtc_ctx.audio_receiver:
            audio_frames.append(frame)
        
        # Save audio to a file
        audio_file = "recorded_audio.wav"
        with open(audio_file, "wb") as f:
            for frame in audio_frames:
                f.write(frame.to_ndarray().tobytes())
        
        # Transcribe audio
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file).text
        st.session_state.transcript = transcript

        # Update UI dynamically
        with col1:
            st.markdown('<div class="card"><h3>Live Transcript</h3></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card">{st.session_state.transcript}</div>', unsafe_allow_html=True)

        # NLP Analysis Cards
        doc = nlp(st.session_state.transcript)
        symptoms = [ent.text for ent in doc.ents if ent.label_ == "DISEASE"]
        diagnosis = [ent.text for ent in doc.ents if ent.label_ == "CHEMICAL"]
        
        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="card"><h3>📋 Symptoms Detected</h3></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card">{"<br>".join(symptoms)}</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="card"><h3>🩺 Diagnosis</h3></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card">{"<br>".join(diagnosis)}</div>', unsafe_allow_html=True)

        # Sentiment Analysis Gauge
        sentiment = sentiment_analyzer(st.session_state.transcript)[0]
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=sentiment["score"],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Sentiment: {sentiment['label']}"},
            gauge={'axis': {'range': [0, 1]}},
        ))
        st.markdown('<div class="card"><h3>📈 Sentiment Analysis</h3></div>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)

# SOAP Note Generation
st.markdown("## SOAP Note Generator")
if st.button("Generate SOAP Note"):
    doc = nlp(st.session_state.transcript)
    symptoms = [ent.text for ent in doc.ents if ent.label_ == "DISEASE"]
    diagnosis = [ent.text for ent in doc.ents if ent.label_ == "CHEMICAL"]
    
    soap_note = {
        "Subjective": {"Symptoms": symptoms},
        "Objective": {"Observations": "Normal vitals"},
        "Assessment": {"Diagnosis": diagnosis},
        "Plan": {"Treatment": "Follow-up in 2 weeks"}
    }
    
    st.markdown("### Structured SOAP Note")
    for section, content in soap_note.items():
        with st.expander(f"🔍 {section}"):
            st.json(content)