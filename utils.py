# utils.py
import streamlit as st
from rag_system import PsychologyRAGSystem

# Khởi tạo RAG system (nếu cần)
@st.cache_resource
def get_rag_system():
    return PsychologyRAGSystem()

def generate_a1_response(user_input, chat_history):
    """
    Hàm xử lý và tạo phản hồi cho người dùng
    """
    try:
        # Lấy RAG system
        rag_system = get_rag_system()
        
        # Tạo phản hồi sử dụng RAG system
        response = rag_system.generate_response(user_input, chat_history)
        
        return response
    except Exception as e:
        return f"Xin lỗi, đã có lỗi xảy ra: {str(e)}"