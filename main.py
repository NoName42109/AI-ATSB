# main.py
import streamlit as st
import sys
import os
import requests
from datetime import datetime

# Thêm path để import - SỬA LẠI
sys.path.append('.')

# Import components - SỬA LẠI
from components.header import render_header

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="AI Psychology Mentor - Gemini",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Áp dụng CSS - SỬA LẠI
def load_css():
    """Load CSS files với xử lý lỗi"""
    css_files = ['./styles/main.css', './styles/animations.css']
    
    for css_file in css_files:
        try:
            if os.path.exists(css_file):
                with open(css_file, 'r', encoding='utf-8') as f:
                    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Lỗi CSS {css_file}: {e}")

# Khởi tạo session state - SỬA LẠI
def init_session_state():
    if 'rag_system' not in st.session_state:
        from rag_system import PsychologyRAGSystem  # Import tại đây
        st.session_state.rag_system = PsychologyRAGSystem()
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'documents_processed' not in st.session_state:
        st.session_state.documents_processed = False

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
                from rag_system import PsychologyRAGSystem  # Import tại đây
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
        from components.chat_interface import render_chat_interface
        render_chat_interface()

if __name__ == "__main__":
    main()
