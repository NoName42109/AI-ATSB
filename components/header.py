# components/header.py
import streamlit as st

def render_header():
    st.markdown("""
    <div style="background: rgba(0,0,0,0.6); padding: 20px; border-radius: 15px; border: 1px solid #48dbfb;">
        <h1 style="color: #48dbfb; text-align: center;">AI PSYCHOLOGY MENTOR</h1>
        <p style="color: #48dbfb; text-align: center; font-weight: bold;">Powered by Google Gemini</p>
        <p style="color: #ccc; text-align: center;">Tro ly Tam ly Hoc duong</p>
    </div>
    """, unsafe_allow_html=True)
