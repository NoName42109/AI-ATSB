# components/header.py
import streamlit as st

def render_header():
    st.markdown("""
    <div class="cyber-card">
        <h1 class="neon-text">🧠 AI PSYCHOLOGY MENTOR</h1>
        
        <p class="neon-subtitle">Powered by Google Gemini</p>
        
        <p class="description">Trợ lý Tâm lý Học đường Thế hệ mới</p>
        
        <!-- Features Section -->
        <div class="feature-card">
            <h4 class="feature-title">🎯 TÍNH NĂNG NỔI BẬT</h4>
            <ul class="feature-list">
                <li>🤖 Google Gemini AI tiên tiến</li>
                <li>📚 Hiểu sâu tài liệu chuyên môn</li>
                <li>💬 Trò chuyện tự nhiên, đồng cảm</li>
                <li>🔒 Bảo mật & Riêng tư tuyệt đối</li>
                <li>⚡ Tốc độ cao & Ổn định</li>
            </ul>
        </div>
        
        <!-- Quick Guide Section -->
        <div class="guide-card">
            <h4 class="guide-title">🚀 HƯỚNG DẪN NHANH</h4>
            <ol class="guide-list">
                <li>Upload tài liệu tâm lý (bên trái)</li>
                <li>Click "XỬ LÝ TÀI LIỆU"</li>
                <li>Bắt đầu trò chuyện!</li>
            </ol>
        </div>
        
        <!-- Tip Section -->
        <div class="tip-card">
            <p class="tip-text">
                💡 <strong>Mẹo:</strong> Hãy chia sẻ tự nhiên như nói chuyện với bạn thân. AI sẽ thấu hiểu và hỗ trợ bạn!
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)