from typing import Dict  # Add this import
import streamlit as st
import plotly.express as px

def styled_header(title: str):
    """Custom header component with Vision UI styling"""
    st.markdown(f"""
    <div class="header-container">
        <h1 class="main-header">{title}</h1>
    </div>
    """, unsafe_allow_html=True)

def medical_card(title: str, content, color: str = "#2D9CDB"):
    """Reusable medical information card"""
    st.markdown(f"""
    <div class="medical-card" style="border-left: 4px solid {color};">
        <h3 class="card-title">{title}</h3>
        <div class="card-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)

def soap_display(soap_data: Dict):
    """Interactive SOAP notes display component"""
    with st.expander("SOAP Notes Details", expanded=True):
        cols = st.columns(4)
        sections = {
            "Subjective": ("👤", "#2D9CDB"),
            "Objective": ("📊", "#27AE60"),
            "Assessment": ("📝", "#F39C12"),
            "Plan": ("📅", "#E74C3C")
        }
        
        for idx, (section, (icon, color)) in enumerate(sections.items()):
            cols[idx].markdown(f"""
            <div class="soap-section" style="border-color: {color};">
                <div class="soap-header">
                    <span class="soap-icon">{icon}</span>
                    <h4>{section}</h4>
                </div>
                <p>{soap_data.get(section.lower(), 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)