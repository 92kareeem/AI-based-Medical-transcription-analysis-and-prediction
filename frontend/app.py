import streamlit as st
from utils.components import styled_header, medical_card, soap_display
from utils.api import analyze_text
import json

def main():
    st.set_page_config(page_title="MedAI Dashboard", layout="wide")
    # Example usage
    result = analyze_text("Sample conversation text")
    if result:
        st.json(result)
    # Inject custom CSS
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    styled_header("Medical Conversation Analyzer")
    
    # Input Section
    with st.expander("Input Conversation", expanded=True):
        transcript = st.text_area("Paste conversation:", height=300)
        
        col1, col2 = st.columns([5,1])
        with col2:
            if st.button("Analyze", key="analyze_btn", use_container_width=True):
                if transcript.strip():
                    with st.spinner("Processing..."):
                        st.session_state.result = analyze_text(transcript)
                else:
                    st.warning("Please input conversation text")

    # Display Results
    if "result" in st.session_state:
        result = st.session_state.result
        
        # Main Analytics Row
        col1, col2, col3 = st.columns([2,2,2])
        with col1:
            medical_card("🩺 Diagnosis", result["summary"]["diagnosis"])
        with col2:
            medical_card("📈 Prognosis", result["summary"]["prognosis"])
        with col3:
            medical_card("😃 Sentiment", result["sentiment"]["label"])
        
        # Detailed Analysis
        with st.container():
            tabs = st.tabs(["Entities", "SOAP Notes", "Keywords", "Raw Data"])
            
            with tabs[0]:
                cols = st.columns(2)
                cols[0].metric("Symptoms", len(result["entities"]["symptoms"]))
                cols[1].metric("Treatments", len(result["entities"]["treatment"]))
                st.write("### Detailed Entities")
                st.json(result["entities"])
            
            with tabs[1]:
                soap_display(result["soap"])
            
            with tabs[2]:
                st.write("### Key Medical Terms")
                st.write(", ".join(result["keywords"]))
            
            with tabs[3]:
                st.json(result)
            
if __name__ == "__main__":
    main()