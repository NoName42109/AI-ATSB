# main.py
import streamlit as st
import sys
import os
import requests
import json
from datetime import datetime

# Thêm path để import utils
sys.path.append('./utils')
sys.path.append('./components')

# Import components - LOẠI BỎ import chat_interface ở đây
from rag_system import PsychologyRAGSystem
from header import render_header

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="AI Psychology Mentor - Gemini",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Áp dụng CSS
def load_css():
    try:
        with open('./main.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        pass
    try:
        with open('./styles/animations.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        pass

# Khởi tạo session state
def init_session_state():
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = PsychologyRAGSystem()
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'documents_processed' not in st.session_state:
        st.session_state.documents_processed = False

# Hàm gọi Gemini API
def call_gemini_api(prompt):
    """Gọi Gemini API"""
    GEMINI_API_KEY = "AIzaSyCZXmiLRMjSc26rWcjD7CB2Voszk3HJTeU"  # Thay key thật
    
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

# Hàm tạo phản hồi - DI CHUYỂN HÀM NÀY SANG utils.py
def generate_ai_response(user_message):
    """Tạo phản hồi từ Gemini với RAG"""
    # Tìm thông tin liên quan
    relevant_info = st.session_state.rag_system.search_similar(user_message, top_k=3)
    context = "\n".join(relevant_info) if relevant_info else "Không tìm thấy thông tin liên quan trong tài liệu."
    
    # Tạo prompt
    prompt = f"""
BẠN LÀ CHUYÊN GIA TÂM LÝ HỌC ĐƯỜNG được đào tạo bài bản.

KIẾN THỨC CHUYÊN MÔN TỪ TÀI LIỆU:
{context}

LỊCH SỬ TRÒ CHUYỆN GẦN ĐÂY:
{get_recent_history()}

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
    if not st.session_state.conversation_history:
        return "Chưa có lịch sử trò chuyện"
    
    recent = st.session_state.conversation_history[-4:]
    history_text = ""
    for msg in recent:
        speaker = "Học sinh" if msg["role"] == "user" else "Chuyên gia"
        history_text += f"{speaker}: {msg['message']}\n"
    return history_text

# Main App
def main():
    # Load CSS và khởi tạo
    load_css()
    init_session_state()
    
    # Render floating shapes animation
    st.markdown("""
    <div class="floating-shapes">
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
    </div>
    <div class="cyber-grid"></div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="neon-text">⚙️ CÀI ĐẶT</h3>', unsafe_allow_html=True)
        
        # Hiển thị AI đang dùng
        st.markdown('<div style="background: rgba(72, 219, 251, 0.2); padding: 10px; border-radius: 10px; margin: 10px 0;">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #48dbfb; text-align: center;">🤖 GOOGLE GEMINI</h4>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Upload documents
        st.markdown("---")
        st.markdown('<h4 class="neon-text">📚 UPLOAD TÀI LIỆU</h4>', unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader(
            "Chọn file (PDF/TXT/DOCX)",
            type=['pdf', 'txt', 'docx'],
            accept_multiple_files=True,
            key="file_uploader"
        )
        
        if uploaded_files and not st.session_state.documents_processed:
            if st.button("🔧 XỬ LÝ TÀI LIỆU", use_container_width=True, type="primary"):
                with st.spinner("🔄 Đang xử lý tài liệu..."):
                    try:
                        st.session_state.rag_system.process_uploaded_files(uploaded_files)
                        st.session_state.documents_processed = True
                        st.success("✅ Đã xử lý xong tài liệu!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Lỗi xử lý: {e}")
        
        # Thông tin hệ thống
        st.markdown("---")
        st.markdown('<h4 class="neon-text">📊 THỐNG KÊ</h4>', unsafe_allow_html=True)
        st.write(f"📄 Chunks: {len(st.session_state.rag_system.knowledge_base)}")
        st.write(f"💬 Tin nhắn: {len(st.session_state.conversation_history)}")
        st.write(f"🔗 Vectors: {st.session_state.rag_system.index.ntotal if st.session_state.rag_system.index else 0}")
        
        # Nút xóa dữ liệu
        if st.session_state.documents_processed:
            if st.button("🗑️ XÓA DỮ LIỆU", use_container_width=True):
                st.session_state.rag_system = PsychologyRAGSystem()
                st.session_state.documents_processed = False
                st.session_state.conversation_history = []
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([1, 3])
    
    with col1:
        render_header()
    
    with col2:
        # IMPORT CỤC BỘ để tránh circular import
        from chat_interface import render_chat_interface
        render_chat_interface()

if __name__ == "__main__":
    main()

