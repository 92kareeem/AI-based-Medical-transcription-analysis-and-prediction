import streamlit as st
from utils.api import MedAPI
from utils.components import styled_header, medical_card, soap_display

def analysis_page():
    # Initialize API client
    api = MedAPI()
    
    # Add styled header
    styled_header("Clinical Conversation Analyzer")
    
    # Input Section
    with st.container():
        transcript = st.text_area(
            "Physician-Patient Conversation",
            height=300,
            placeholder="Paste conversation transcript here..."
        )
        
        # Analyze button
        if st.button("Analyze Conversation", use_container_width=True):
            if transcript.strip():
                with st.spinner("Analyzing medical content..."):
                    # Call the API and store results in session state
                    st.session_state.result = api.analyze_text(transcript)
            else:
                st.warning("Please enter a conversation transcript")

    # Results Display
    if "result" in st.session_state and st.session_state.result:
        result = st.session_state.result
        
        # Top Metrics Row
        col1, col2, col3 = st.columns(3)
        with col1:
            medical_card(
                "Primary Diagnosis",
                result["summary"]["diagnosis"],
                color="#2D9CDB"  # Blue
            )
        with col2:
            medical_card(
                "Patient Sentiment",
                result["sentiment"]["label"],
                color="#27AE60"  # Green
            )
        with col3:
            medical_card(
                "Key Treatments",
                ", ".join(result["entities"]["treatment"]) if result["entities"]["treatment"] else "None",
                color="#E74C3C"  # Red
            )

        # Detailed Medical Entities
        with st.expander("Detailed Medical Entities", expanded=True):
            cols = st.columns(2)
            with cols[0]:
                st.write("**Symptoms:**")
                st.write(", ".join(result["entities"]["symptoms"]) if result["entities"]["symptoms"] else "None")
            with cols[1]:
                st.write("**Medications:**")
                st.write(", ".join(result["entities"]["drugs"]) if result["entities"]["drugs"] else "None")

        # SOAP Notes Display
        soap_display(result["soap"])

        # Raw JSON Viewer
        with st.expander("Raw Analysis Data"):
            st.json(result)