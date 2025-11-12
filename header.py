# components/header.py
import streamlit as st

def render_header():
    st.markdown("""
    <div class="cyber-card pulse-glow">
        <h1 class="neon-text">🧠 AI PSYCHOLOGY MENTOR</h1>
        <p style="color: #48dbfb; margin-bottom: 20px; font-weight: bold;">Powered by Google Gemini</p>
        <p style="color: #ccc; margin-bottom: 20px;">Trợ lý Tâm lý Học đường Thế hệ mới</p>
        
        <div style="background: rgba(72, 219, 251, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0; border: 1px solid rgba(72, 219, 251, 0.3);">
            <h4 style="color: #48dbfb;">🎯 TÍNH NĂNG NỔI BẬT</h4>
            <ul style="color: #ccc; margin-left: 20px;">
                <li>🤖 Google Gemini AI</li>
                <li>📚 Hiểu sâu tài liệu chuyên môn</li>
                <li>💬 Trò chuyện tự nhiên, đồng cảm</li>
                <li>🔒 Bảo mật & Riêng tư</li>
                <li>🚀 Tốc độ cao & Ổn định</li>
            </ul>
        </div>
        
        <div style="background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px;">
            <h4 style="color: #feca57;">🚀 HƯỚNG DẪN NHANH</h4>
            <ol style="color: #ccc; margin-left: 20px;">
                <li>Upload tài liệu tâm lý (bên trái)</li>
                <li>Click "XỬ LÝ TÀI LIỆU"</li>
                <li>Bắt đầu trò chuyện!</li>
            </ol>
        </div>
        
        <div style="margin-top: 20px; padding: 15px; background: rgba(255, 255, 255, 0.05); border-radius: 10px;">
            <p style="color: #ff6b6b; font-size: 0.9em;">
                💡 <strong>Mẹo:</strong> Hãy chia sẻ tự nhiên như nói chuyện với bạn thân. AI sẽ thấu hiểu và hỗ trợ bạn!
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)