# utils.py
import streamlit as st
import requests
from datetime import datetime

def call_gemini_api(prompt):
    """Gọi Gemini API"""
    GEMINI_API_KEY = "AIzaSyCZXmiLRMjSc26rWcjD7CB2Voszk3HJTeU"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ Lỗi Gemini API: {response.status_code}"
    except Exception as e:
        return f"❌ Lỗi kết nối: {str(e)}"

def generate_ai_response(user_message):
    """Tạo phản hồi từ Gemini với RAG"""
    # Kiểm tra session state
    if 'rag_system' not in st.session_state:
        return "❌ Hệ thống chưa được khởi tạo. Vui lòng reload trang."
    
    # Tìm thông tin liên quan
    relevant_info = st.session_state.rag_system.search_similar(user_message, top_k=3)
    context = "\n".join(relevant_info) if relevant_info else "Không tìm thấy thông tin liên quan trong tài liệu."
    
    # Lấy lịch sử gần đây
    recent_history = get_recent_history()
    
    # Tạo prompt
    prompt = f"""
BẠN LÀ CHUYÊN GIA TÂM LÝ HỌC ĐƯỜNG được đào tạo bài bản.

KIẾN THỨC CHUYÊN MÔN TỪ TÀI LIỆU:
{context}

LỊCH SỬ TRÒ CHUYỆN GẦN ĐÂY:
{recent_history}

TIN NHẮN HIỆN TẠI TỪ HỌC SINH:
"{user_message}"

HÃY TRÒ CHUYỆN:
- Như một người bạn thân thiết, đồng cảm
- Sử dụng kiến thức chuyên môn từ tài liệu để tư vấn
- Đưa ra lời khuyên thiết thực, cụ thể
- Không giáo điều, không phán xét
- Giữ cuộc trò chuyện tự nhiên, tiếp diễn
- Luôn tích cực và động viên

Trả lời bằng tiếng Việt tự nhiên, gần gũi với học sinh.
"""
    
    return call_gemini_api(prompt)

def get_recent_history():
    """Lấy lịch sử gần đây"""
    if 'conversation_history' not in st.session_state:
        return "Chưa có lịch sử trò chuyện"
    
    if not st.session_state.conversation_history:
        return "Chưa có lịch sử trò chuyện"
    
    recent = st.session_state.conversation_history[-4:]
    history_text = ""
    for msg in recent:
        speaker = "Học sinh" if msg["role"] == "user" else "Chuyên gia"
        history_text += f"{speaker}: {msg['message']}\n"
    return history_text
