# components/chat_interface.py
import streamlit as st
from datetime import datetime
from utils import generate_ai_response

def render_chat_interface():
    st.markdown('<div class="cyber-container">', unsafe_allow_html=True)
    
    # Header chat
    st.markdown('<h2 class="neon-text" style="text-align: center; margin-bottom: 20px;">💬 PHÒNG TÂM SỰ HỌC ĐƯỜNG</h2>', unsafe_allow_html=True)
    
    # Chat container
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    # Hiển thị lịch sử chat
    if not st.session_state.conversation_history:
        st.markdown('''
        <div class="welcome-message">
            <h3>👋 Chào bạn!</h3>
            <p>Hãy bắt đầu cuộc trò chuyện bằng cách nhập tin nhắn bên dưới.</p>
            <p>Tôi ở đây để lắng nghe và hỗ trợ bạn! 💙</p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        for msg in st.session_state.conversation_history:
            if msg["role"] == "user":
                st.markdown(f'''
                <div class="chat-message user-message">
                    <strong>👤 Bạn:</strong><br>
                    {msg["message"]}
                    <div class="message-time">{msg["time"]}</div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="chat-message bot-message">
                    <strong>🤖 Mentor:</strong>
                    <span class="ai-badge">GEMINI</span><br>
                    {msg["message"]}
                    <div class="message-time">{msg["time"]}</div>
                </div>
                ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area
    col1, col2, col3 = st.columns([4, 1, 1])
    
    with col1:
        user_input = st.text_input(
            "💬 Nhập tin nhắn...",
            placeholder="Hãy chia sẻ với tôi...",
            key="user_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("🚀 GỬI", use_container_width=True, type="primary")
    
    with col3:
        if st.session_state.conversation_history:
            clear_button = st.button("🗑️", use_container_width=True, help="Xóa lịch sử chat")
        else:
            clear_button = False
    
    # Xử lý tin nhắn
    if send_button and user_input:
        if not st.session_state.documents_processed:
            st.warning("⚠️ Hãy upload và xử lý tài liệu trước khi chat!")
        else:
            # Thêm tin nhắn user
            user_msg = {
                "role": "user",
                "message": user_input,
                "time": datetime.now().strftime("%H:%M:%S")
            }
            st.session_state.conversation_history.append(user_msg)
            
            # Tạo phản hồi AI
            with st.spinner("🤔 Đang phân tích và trả lời..."):
                try:
                    response = generate_ai_response(user_input)
                    
                    bot_msg = {
                        "role": "bot",
                        "message": response,
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "ai_used": "gemini"
                    }
                    st.session_state.conversation_history.append(bot_msg)
                    
                    # Refresh để hiển thị tin nhắn mới
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Lỗi: {e}")
    
    # Xóa lịch sử chat
    if clear_button:
        st.session_state.conversation_history = []
        st.rerun()
    
    # Hiển thị trạng thái hệ thống
    st.markdown("---")
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        status = "✅ Đã sẵn sàng" if st.session_state.documents_processed else "⏳ Chờ tài liệu"
        st.metric("Trạng thái", status)
    
    with status_col2:
        st.metric("Tin nhắn", len(st.session_state.conversation_history))
    
    with status_col3:
        chunks = len(st.session_state.rag_system.knowledge_base)
        st.metric("Chunks", chunks)
    
    st.markdown('</div>', unsafe_allow_html=True)