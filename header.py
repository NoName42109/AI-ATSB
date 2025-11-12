# components/header.py
import streamlit as st

def render_header():
    st.markdown("""
    <div class="cyber-card" style="
        background: rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(72, 219, 251, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 20px rgba(72, 219, 251, 0.2);
    ">
        <h1 class="neon-text" style="
            color: #48dbfb;
            text-shadow: 0 0 10px #48dbfb, 0 0 20px #48dbfb;
            text-align: center;
            margin-bottom: 10px;
            font-size: 1.8em;
        ">🧠 AI PSYCHOLOGY MENTOR</h1>
        
        <p style="color: #48dbfb; margin-bottom: 15px; font-weight: bold; text-align: center;">
            Powered by Google Gemini
        </p>
        
        <p style="color: #ccc; margin-bottom: 25px; text-align: center;">
            Trợ lý Tâm lý Học đường Thế hệ mới
        </p>
        
        <!-- Features Section -->
        <div style="
            background: rgba(72, 219, 251, 0.1); 
            padding: 15px; 
            border-radius: 10px; 
            margin: 15px 0; 
            border: 1px solid rgba(72, 219, 251, 0.3);
        ">
            <h4 style="color: #48dbfb; margin-top: 0; margin-bottom: 10px;">🎯 TÍNH NĂNG NỔI BẬT</h4>
            <ul style="color: #ccc; margin-left: 20px; margin-bottom: 0;">
                <li>🤖 Google Gemini AI tiên tiến</li>
                <li>📚 Hiểu sâu tài liệu chuyên môn</li>
                <li>💬 Trò chuyện tự nhiên, đồng cảm</li>
                <li>🔒 Bảo mật & Riêng tư tuyệt đối</li>
                <li>⚡ Tốc độ cao & Ổn định</li>
            </ul>
        </div>
        
        <!-- Quick Guide Section -->
        <div style="
            background: rgba(254, 202, 87, 0.1); 
            padding: 15px; 
            border-radius: 10px; 
            margin: 15px 0;
            border: 1px solid rgba(254, 202, 87, 0.3);
        ">
            <h4 style="color: #feca57; margin-top: 0; margin-bottom: 10px;">🚀 HƯỚNG DẪN NHANH</h4>
            <ol style="color: #ccc; margin-left: 20px; margin-bottom: 0;">
                <li>Upload tài liệu tâm lý (bên trái)</li>
                <li>Click "XỬ LÝ TÀI LIỆU"</li>
                <li>Bắt đầu trò chuyện!</li>
            </ol>
        </div>
        
        <!-- Tip Section -->
        <div style="
            margin-top: 20px; 
            padding: 15px; 
            background: rgba(255, 107, 107, 0.1); 
            border-radius: 10px;
            border: 1px solid rgba(255, 107, 107, 0.3);
        ">
            <p style="color: #ff6b6b; font-size: 0.9em; margin: 0;">
                💡 <strong>Mẹo:</strong> Hãy chia sẻ tự nhiên như nói chuyện với bạn thân. AI sẽ thấu hiểu và hỗ trợ bạn!
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
