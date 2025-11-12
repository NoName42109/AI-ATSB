import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid
import os
import sqlite3
from typing import Dict, List, Optional
import time

# ==================== CẤU HÌNH ỨNG DỤNG ====================

class AppConfig:
    def __init__(self):
        self.DEEPSEEK_API_KEY = "sk-023cfb5c02a244d990ebcf76d789985e"  # Thay bằng API key thật
        self.DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
        self.DATA_FOLDER = "user_data"
        self.DB_PATH = "mental_health.db"
        
        # Tạo thư mục lưu dữ liệu
        os.makedirs(self.DATA_FOLDER, exist_ok=True)

# ==================== HỆ THỐNG AI VỚI DEEPSEEK ====================

class DeepSeekMentalHealthAI:
    def __init__(self, config: AppConfig):
        self.config = config
        self.system_prompt = """Bạn là một chuyên gia tâm lý học đường thân thiện, đồng cảm và luôn lắng nghe. 
Hãy trò chuyện với học sinh cấp 2, cấp 3 theo cách:

🎯 **PHONG CÁCH GIAO TIẾP:**
- Luôn bắt đầu bằng sự thấu hiểu và đồng cảm
- Sử dụng ngôn ngữ gần gũi, dễ hiểu, như một người bạn lớn
- Khen ngợi sự dũng cảm khi họ chia sẻ
- Không phán xét, không chỉ trích
- Luôn tạo cảm giác an toàn và được lắng nghe

❤️ **KỸ NĂNG ĐỒNG CẢM:**
- "Tôi hiểu cảm giác của bạn..." 
- "Điều đó chắc hẳn rất khó khăn..."
- "Bạn thật dũng cảm khi chia sẻ điều này..."
- "Cảm xúc của bạn là hoàn toàn bình thường..."
- "Tôi ở đây để lắng nghe bạn..."

🎨 **CÁCH THỨC HỖ TRỢ:**
1. LẮNG NGHE CHỦ ĐỘNG: Ghi nhận cảm xúc và tâm sự
2. ĐẶT CÂU HỎI MỞ: Khuyến khích họ chia sẻ sâu hơn
3. CHUẨN HOÁ CẢM XÚC: Giúp họ hiểu cảm xúc là bình thường
4. ĐỀ XUẤT NHẸ NHÀNG: Đưa ra gợi ý nhưng không áp đặt
5. KẾT NỐI TÀI NGUYÊN: Giới thiệu chuyên gia khi cần

🚨 **XỬ LÝ TÌNH HUỐNG NGUY CƠ CAO:**
- Khi phát hiện ý định tự làm hại: Khẩn trương nhưng bình tĩnh
- Cung cấp ngay đường dây nóng
- Khuyến khích tìm người lớn tin cậy
- Nhấn mạnh sự quan trọng của việc được giúp đỡ

Hãy trả lời một cách tự nhiên, ấm áp và chân thành như một người bạn đáng tin cậy."""

    def analyze_emotion(self, text: str) -> Dict:
        """Phân tích cảm xúc từ văn bản"""
        emotions = {
            'buồn bã': ['buồn', 'chán', 'tuyệt vọng', 'khóc', 'muốn khóc', 'thất vọng'],
            'lo âu': ['lo', 'sợ', 'hồi hộp', 'bồn chồn', 'hoảng', 'căng thẳng'],
            'tức giận': ['tức', 'giận', 'bực', 'khó chịu', 'tức giận', 'tức tối'],
            'vui vẻ': ['vui', 'hạnh phúc', 'tốt', 'ổn', 'hào hứng', 'phấn khởi'],
            'sợ hãi': ['sợ', 'hoảng sợ', 'khiếp sợ', 'run sợ', 'hãi'],
            'trung tính': ['bình thường', 'ok', 'ổn', 'tạm được']
        }
        
        text_lower = text.lower()
        emotion_scores = {emotion: 0 for emotion in emotions.keys()}
        
        for emotion, keywords in emotions.items():
            for keyword in keywords:
                if keyword in text_lower:
                    emotion_scores[emotion] += 1
        
        # Tìm cảm xúc chiếm ưu thế
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])
        
        return {
            'emotions': emotion_scores,
            'dominant_emotion': dominant_emotion[0] if dominant_emotion[1] > 0 else 'trung tính',
            'confidence': dominant_emotion[1] / len(emotions[dominant_emotion[0]]) if dominant_emotion[1] > 0 else 0
        }

    def assess_risk_level(self, text: str, emotion_analysis: Dict) -> int:
        """Đánh giá mức độ nguy cơ"""
        text_lower = text.lower()
        
        risk_keywords = {
            1: ['ổn', 'tốt', 'vui', 'bình thường', 'ok', 'khá', 'tạm'],
            2: ['buồn', 'chán', 'mệt', 'căng thẳng', 'lo', 'hơi lo', 'chút áp lực'],
            3: ['lo lắng', 'sợ hãi', 'hoảng', 'khó ngủ', 'bắt nạt', 'cô đơn', 'lạc lõng'],
            4: ['tự làm hại', 'trầm cảm', 'tuyệt vọng', 'bỏ học', 'không muốn sống', 'mệt mỏi'],
            5: ['tự tử', 'chết', 'kết thúc', 'không muốn sống nữa', 'kết liễu']
        }
        
        # Đánh giá dựa trên từ khóa
        base_risk = 1
        for level, keywords in risk_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                base_risk = max(base_risk, level)
        
        # Điều chỉnh dựa trên cảm xúc
        emotion_risk = {
            'buồn bã': 3,
            'lo âu': 3,
            'tức giận': 2,
            'sợ hãi': 3,
            'vui vẻ': 1,
            'trung tính': 1
        }
        
        emotion_adjustment = emotion_risk.get(emotion_analysis['dominant_emotion'], 1)
        final_risk = max(base_risk, emotion_adjustment)
        
        # Tăng risk nếu có nhiều từ khóa nguy hiểm
        danger_words = ['tự tử', 'chết', 'kết thúc', 'không muốn sống']
        danger_count = sum(1 for word in danger_words if word in text_lower)
        if danger_count >= 2:
            final_risk = max(final_risk, 4)
        
        return min(5, final_risk)

    def get_ai_response(self, user_message: str, conversation_history: List[Dict]) -> Dict:
        """Lấy phản hồi từ DeepSeek API"""
        
        # Chuẩn bị lịch sử hội thoại
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Thêm lịch sử hội thoại (tối đa 10 tin nhắn gần nhất)
        for chat in conversation_history[-10:]:
            role = "user" if chat["role"] == "user" else "assistant"
            messages.append({"role": role, "content": chat["message"]})
        
        # Thêm tin nhắn hiện tại
        messages.append({"role": "user", "content": user_message})
        
        try:
            headers = {
                "Authorization": f"Bearer {self.config.DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000,
                "stream": False
            }
            
            response = requests.post(self.config.DEEPSEEK_API_URL, 
                                   headers=headers, 
                                   json=payload, 
                                   timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"]
                
                # Phân tích cảm xúc và risk
                emotion_analysis = self.analyze_emotion(user_message)
                risk_level = self.assess_risk_level(user_message, emotion_analysis)
                
                return {
                    "response": ai_response,
                    "risk_level": risk_level,
                    "emotion": emotion_analysis['dominant_emotion'],
                    "emotion_confidence": emotion_analysis['confidence'],
                    "success": True
                }
            else:
                return {
                    "response": "Xin lỗi, tôi đang gặp chút trục trặc kỹ thuật. Bạn có thể thử lại sau không?",
                    "risk_level": 1,
                    "emotion": "trung tính",
                    "success": False
                }
                
        except Exception as e:
            return {
                "response": f"Hiện tại tôi không thể kết nối. Nhưng tôi vẫn muốn lắng nghe bạn! Hãy chia sẻ thêm nhé. Lỗi: {str(e)}",
                "risk_level": 1,
                "emotion": "trung tính", 
                "success": False
            }

# ==================== QUẢN LÝ DỮ LIỆU NGƯỜI DÙNG ====================

class UserDataManager:
    def __init__(self, config: AppConfig):
        self.config = config
        self.init_database()
    
    def init_database(self):
        """Khởi tạo database SQLite"""
        conn = sqlite3.connect(self.config.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                age INTEGER,
                grade TEXT,
                gender TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                role TEXT,
                message TEXT,
                emotion TEXT,
                risk_level INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_analytics (
                user_id TEXT,
                date DATE,
                avg_risk_level REAL,
                dominant_emotion TEXT,
                message_count INTEGER,
                PRIMARY KEY (user_id, date)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_conversation(self, user_id: str, role: str, message: str, 
                         emotion: str, risk_level: int):
        """Lưu cuộc trò chuyện vào database"""
        conn = sqlite3.connect(self.config.DB_PATH)
        cursor = conn.cursor()
        
        # Cập nhật thời gian hoạt động cuối
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, last_active)
            VALUES (?, CURRENT_TIMESTAMP)
        ''', (user_id,))
        
        # Lưu tin nhắn
        cursor.execute('''
            INSERT INTO conversations (user_id, role, message, emotion, risk_level)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, role, message, emotion, risk_level))
        
        conn.commit()
        conn.close()
    
    def get_conversation_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Lấy lịch sử hội thoại của người dùng"""
        conn = sqlite3.connect(self.config.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT role, message, emotion, risk_level, timestamp
            FROM conversations 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (user_id, limit))
        
        history = []
        for row in cursor.fetchall():
            history.append({
                "role": row[0],
                "message": row[1],
                "emotion": row[2],
                "risk_level": row[3],
                "timestamp": row[4]
            })
        
        conn.close()
        return list(reversed(history))  # Đảo ngược để có thứ tự thời gian
    
    def get_user_analytics(self, user_id: str) -> Dict:
        """Lấy phân tích dữ liệu người dùng"""
        conn = sqlite3.connect(self.config.DB_PATH)
        cursor = conn.cursor()
        
        # Thống kê cơ bản
        cursor.execute('''
            SELECT COUNT(*), AVG(risk_level), MAX(risk_level)
            FROM conversations 
            WHERE user_id = ?
        ''', (user_id,))
        
        count, avg_risk, max_risk = cursor.fetchone()
        
        # Cảm xúc thường gặp
        cursor.execute('''
            SELECT emotion, COUNT(*) as count
            FROM conversations 
            WHERE user_id = ? AND role = 'user'
            GROUP BY emotion 
            ORDER BY count DESC
            LIMIT 1
        ''', (user_id,))
        
        result = cursor.fetchone()
        dominant_emotion = result[0] if result else "chưa có"
        
        # Xu hướng risk 7 ngày gần nhất
        cursor.execute('''
            SELECT DATE(timestamp), AVG(risk_level)
            FROM conversations 
            WHERE user_id = ? AND timestamp >= DATE('now', '-7 days')
            GROUP BY DATE(timestamp)
            ORDER BY DATE(timestamp)
        ''', (user_id,))
        
        risk_trend = cursor.fetchall()
        
        conn.close()
        
        return {
            "total_conversations": count or 0,
            "average_risk": round(avg_risk or 0, 2),
            "max_risk": max_risk or 0,
            "dominant_emotion": dominant_emotion,
            "risk_trend": risk_trend
        }

# ==================== GIAO DIỆN STREAMLIT ====================

class MentalHealthWebApp:
    def __init__(self):
        self.config = AppConfig()
        self.ai_engine = DeepSeekMentalHealthAI(self.config)
        self.data_manager = UserDataManager(self.config)
        self.setup_page()
    
    def setup_page(self):
        """Cấu hình trang Streamlit"""
        st.set_page_config(
            page_title="🌷 AI Tâm Sự Học Đường",
            page_icon="🌷",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # CSS tùy chỉnh với màu sắc dễ thương
        st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            color: #FF6B9D;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .sub-header {
            color: #5D7BD5;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        .chat-container {
            background: linear-gradient(135deg, #E3F2FD, #F3E5F5);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 20px;
            max-height: 500px;
            overflow-y: auto;
            border: 2px solid #E1BEE7;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }
        .user-message {
            background: linear-gradient(135deg, #FFD1DC, #FFB6C1);
            padding: 15px;
            border-radius: 18px 18px 5px 18px;
            margin: 10px 0;
            text-align: right;
            max-width: 80%;
            margin-left: auto;
            border: 1px solid #FF9EB5;
        }
        .ai-message {
            background: linear-gradient(135deg, #E8F5E8, #C8E6C9);
            padding: 15px;
            border-radius: 18px 18px 18px 5px;
            margin: 10px 0;
            text-align: left;
            max-width: 80%;
            border: 1px solid #A5D6A7;
        }
        .risk-high {
            color: #FF4444;
            font-weight: bold;
            background: #FFE5E5;
            padding: 5px 10px;
            border-radius: 10px;
            display: inline-block;
        }
        .risk-medium {
            color: #FF8800;
            font-weight: bold;
            background: #FFF3E0;
            padding: 5px 10px;
            border-radius: 10px;
            display: inline-block;
        }
        .risk-low {
            color: #00C851;
            font-weight: bold;
            background: #E8F5E8;
            padding: 5px 10px;
            border-radius: 10px;
            display: inline-block;
        }
        .emotion-badge {
            background: linear-gradient(135deg, #BB86FC, #985EFF);
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            display: inline-block;
            margin: 5px 0;
        }
        .emergency-alert {
            background: linear-gradient(135deg, #FF5252, #FF1744);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            text-align: center;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        .stButton button {
            background: linear-gradient(135deg, #FF6B9D, #FF8E53);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 10px 25px;
            font-weight: bold;
        }
        .stButton button:hover {
            background: linear-gradient(135deg, #FF8E53, #FF6B9D);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        </style>
        """, unsafe_allow_html=True)
    
    def init_session_state(self):
        """Khởi tạo session state"""
        if 'user_id' not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())[:8]
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        if 'user_info' not in st.session_state:
            st.session_state.user_info = {
                'age': 15,
                'grade': 'Lớp 9',
                'gender': 'Không tiết lộ'
            }
        
        if 'show_emergency' not in st.session_state:
            st.session_state.show_emergency = False

    def render_sidebar(self):
        """Render sidebar"""
        with st.sidebar:
            st.markdown("🌷")
            st.markdown("<h1 style='text-align: center; color: #FF6B9D;'>🌷 AI Tâm Sự</h1>", 
                       unsafe_allow_html=True)
            
            # Thông tin người dùng
            st.subheader("👤 Thông tin của bạn")
            age = st.slider("Tuổi", 10, 18, 15)
            grade = st.selectbox("Khối lớp", 
                               ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", 
                                "Lớp 10", "Lớp 11", "Lớp 12"])
            gender = st.radio("Giới tính", ["Nam", "Nữ", "Không tiết lộ"])
            
            st.session_state.user_info = {
                'age': age,
                'grade': grade,
                'gender': gender
            }
            
            st.divider()
            
            # Điều hướng
            st.subheader("🧭 Điều hướng")
            page = st.radio("Chọn trang:", [
                "💬 Trò chuyện với AI", 
                "📊 Nhật ký cảm xúc",
                "🌻 Tài nguyên hỗ trợ"
            ])
            
            st.divider()
            
            # Thông tin khẩn cấp
            st.subheader("🆘 Hỗ trợ ngay")
            if st.button("🚨 Cần giúp đỡ khẩn cấp"):
                st.session_state.show_emergency = True
            
            st.markdown("""
            **Đường dây nóng:**
            - 📞 111: Tổng đài Quốc gia bảo vệ trẻ em
            - 📞 113: Công an
            - 📞 115: Cấp cứu Y tế
            """)
            
            return page

    def render_chat_interface(self):
        """Giao diện trò chuyện chính"""
        st.markdown('<div class="main-header">💬 AI Tâm Sự Học Đường</div>', 
                   unsafe_allow_html=True)
        
        # Hiển thị cảnh báo khẩn cấp nếu có
        if st.session_state.show_emergency:
            self.render_emergency_alert()
        
        # Container chat
        chat_container = st.container()
        
        # Hiển thị lịch sử chat
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            if not st.session_state.chat_history:
                st.markdown("""
                <div style='text-align: center; padding: 40px; color: #666;'>
                    <h3>🌷 Chào bạn! Mình là AI Tâm Sự</h3>
                    <p>Mình ở đây để lắng nghe và hỗ trợ bạn. Hãy chia sẻ bất cứ điều gì bạn muốn!</p>
                    <p>💝 Mọi cảm xúc của bạn đều quan trọng và đáng được tôn trọng</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                for chat in st.session_state.chat_history:
                    if chat["role"] == "user":
                        st.markdown(f'''
                        <div class="user-message">
                            <strong>Bạn:</strong> {chat["message"]}
                        </div>
                        ''', unsafe_allow_html=True)
                    else:
                        # Xác định class risk
                        risk_class = "risk-low"
                        if chat.get("risk_level", 1) >= 4:
                            risk_class = "risk-high"
                        elif chat.get("risk_level", 1) >= 3:
                            risk_class = "risk-medium"
                        
                        emotion = chat.get("emotion", "trung tính")
                        
                        st.markdown(f'''
                        <div class="ai-message">
                            <strong>AI Tâm Sự:</strong> {chat["message"]}
                            <br>
                            <div class="emotion-badge">🎭 {emotion}</div>
                            <div class="{risk_class}">📊 Mức độ quan tâm: {chat.get("risk_level", 1)}/5</div>
                        </div>
                        ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Input tin nhắn
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_area("💌 Nhập tin nhắn của bạn...", 
                                    height=100, 
                                    placeholder="Hôm nay bạn thế nào? Hãy chia sẻ với mình nhé...")
        with col2:
            st.write("")  # Căn chỉnh
            st.write("")
            send_button = st.button("Gửi 💝", use_container_width=True)
        
        # Xử lý tin nhắn
        if send_button and user_input.strip():
            self.process_user_message(user_input.strip())
            st.rerun()
        
        # Nút xóa lịch sử
        if st.session_state.chat_history:
            if st.button("🧹 Xóa lịch sử trò chuyện"):
                st.session_state.chat_history = []
                st.rerun()

    def process_user_message(self, message: str):
        """Xử lý tin nhắn người dùng"""
        # Thêm tin nhắn người dùng vào lịch sử
        user_chat = {
            "role": "user",
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        st.session_state.chat_history.append(user_chat)
        
        # Lưu vào database
        emotion_analysis = self.ai_engine.analyze_emotion(message)
        risk_level = self.ai_engine.assess_risk_level(message, emotion_analysis)
        
        self.data_manager.save_conversation(
            st.session_state.user_id, "user", message,
            emotion_analysis['dominant_emotion'], risk_level
        )
        
        # Hiển thị trạng thái đang xử lý
        with st.spinner("🔄 AI Tâm Sự đang suy nghĩ..."):
            # Lấy phản hồi từ AI
            ai_response = self.ai_engine.get_ai_response(
                message, 
                st.session_state.chat_history
            )
        
        # Thêm phản hồi AI vào lịch sử
        ai_chat = {
            "role": "assistant",
            "message": ai_response["response"],
            "risk_level": ai_response["risk_level"],
            "emotion": ai_response["emotion"],
            "timestamp": datetime.now().isoformat()
        }
        st.session_state.chat_history.append(ai_chat)
        
        # Lưu phản hồi AI vào database
        self.data_manager.save_conversation(
            st.session_state.user_id, "assistant", ai_response["response"],
            ai_response["emotion"], ai_response["risk_level"]
        )
        
        # Kiểm tra cảnh báo khẩn cấp
        if ai_response["risk_level"] >= 4:
            st.session_state.show_emergency = True

    def render_emergency_alert(self):
        """Hiển thị cảnh báo khẩn cấp"""
        st.markdown("""
        <div class="emergency-alert">
            <h2>🚨 CẦN HỖ TRỢ NGAY LẬP TỨC!</h2>
            <p>Chúng tôi nhận thấy bạn có thể đang gặp tình huống nguy hiểm.</p>
            <p><strong>Hãy liên hệ ngay:</strong></p>
            <p>📞 111 - Tổng đài Quốc gia bảo vệ trẻ em</p>
            <p>📞 113 - Công an</p>
            <p>📞 115 - Cấp cứu Y tế</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("👍 Tôi đã an toàn", key="safe_btn"):
            st.session_state.show_emergency = False
            st.rerun()

    def render_analytics_dashboard(self):
        """Dashboard phân tích cảm xúc"""
        st.markdown('<div class="main-header">📊 Nhật Ký Cảm Xúc</div>', 
                   unsafe_allow_html=True)
        
        # Lấy dữ liệu phân tích
        analytics = self.data_manager.get_user_analytics(st.session_state.user_id)
        conversation_history = self.data_manager.get_conversation_history(st.session_state.user_id)
        
        if not conversation_history:
            st.info("""
            🌈 Chưa có dữ liệu phân tích nào. 
            Hãy trò chuyện với AI Tâm Sự để bắt đầu hành trình chăm sóc sức khỏe tinh thần của bạn!
            """)
            return
        
        # Hiển thị thống kê tổng quan
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💬 Số cuộc trò chuyện", analytics["total_conversations"])
        
        with col2:
            st.metric("📈 Mức quan tâm TB", f"{analytics['average_risk']}/5")
        
        with col3:
            st.metric("🎭 Cảm xúc thường gặp", analytics["dominant_emotion"])
        
        with col4:
            st.metric("⚠️ Mức cao nhất", f"{analytics['max_risk']}/5")
        
        st.divider()
        
        # Biểu đồ cảm xúc
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Xu hướng cảm xúc")
            
            # Chuẩn bị dữ liệu cho biểu đồ
            if conversation_history:
                df_data = []
                for conv in conversation_history:
                    if conv["role"] == "user":
                        df_data.append({
                            "timestamp": datetime.fromisoformat(conv["timestamp"]),
                            "risk_level": conv["risk_level"],
                            "emotion": conv["emotion"]
                        })
                
                if df_data:
                    df = pd.DataFrame(df_data)
                    fig = px.line(df, x='timestamp', y='risk_level',
                                title='Diễn biến mức độ quan tâm theo thời gian',
                                labels={'risk_level': 'Mức quan tâm', 'timestamp': 'Thời gian'})
                    fig.update_layout(yaxis_range=[1, 5])
                    st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎭 Phân bố cảm xúc")
            
            if conversation_history:
                emotions = [conv["emotion"] for conv in conversation_history if conv["role"] == "user"]
                emotion_counts = pd.Series(emotions).value_counts()
                
                fig = px.pie(values=emotion_counts.values, 
                           names=emotion_counts.index,
                           title='Tỷ lệ các loại cảm xúc')
                st.plotly_chart(fig, use_container_width=True)
        
        # Lịch sử chi tiết
        st.subheader("📝 Lịch sử trò chuyện gần đây")
        recent_chats = conversation_history[-10:]  # 10 tin nhắn gần nhất
        
        for chat in recent_chats:
            if chat["role"] == "user":
                with st.expander(f"💬 {chat['message'][:50]}...", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Tin nhắn:** {chat['message']}")
                    with col2:
                        risk_class = "risk-low"
                        if chat["risk_level"] >= 4:
                            risk_class = "risk-high"
                        elif chat["risk_level"] >= 3:
                            risk_class = "risk-medium"
                        
                        st.write(f"**Mức quan tâm:** :{risk_class}[{chat['risk_level']}/5]")
                        st.write(f"**Cảm xúc:** {chat['emotion']}")
                        st.write(f"**Thời gian:** {chat['timestamp'][:16]}")

    def render_resources_page(self):
        """Trang tài nguyên hỗ trợ"""
        st.markdown('<div class="main-header">🌻 Tài Nguyên Hỗ Trợ</div>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👨‍⚕️ Chuyên gia tâm lý")
            
            specialists = {
                "Hà Nội": [
                    {"name": "TS. Nguyễn Văn A", "phone": "024-1234-5678", "specialty": "Trầm cảm tuổi teen"},
                    {"name": "ThS. Trần Thị B", "phone": "024-2345-6789", "specialty": "Lo âu học đường"}
                ],
                "TP.HCM": [
                    {"name": "BS. Lê Văn C", "phone": "028-9876-5432", "specialty": "Khủng hoảng tuổi dậy thì"},
                    {"name": "TS. Phạm Thị D", "phone": "028-8765-4321", "specialty": "Rối loạn cảm xúc"}
                ]
            }
            
            for city, specs in specialists.items():
                with st.expander(f"🏙️ {city}"):
                    for spec in specs:
                        st.write(f"**{spec['name']}**")
                        st.write(f"📞 {spec['phone']}")
                        st.write(f"🎯 {spec['specialty']}")
                        st.write("---")
        
        with col2:
            st.subheader("📚 Tài liệu tự giúp")
            
            resources = [
                {
                    "title": "Kỹ thuật thở 4-7-8", 
                    "content": "Hít vào 4 giây, giữ 7 giây, thở ra 8 giây. Lặp lại 4 lần."
                },
                {
                    "title": "Viết nhật ký cảm xúc", 
                    "content": "Viết ra những suy nghĩ và cảm xúc mỗi ngày giúp hiểu rõ bản thân hơn."
                },
                {
                    "title": "Thiền định 5 phút", 
                    "content": "Ngồi yên, tập trung vào hơi thở, để suy nghĩ đến và đi tự nhiên."
                },
                {
                    "title": "Liệu pháp âm nhạc", 
                    "content": "Nghe nhạc nhẹ nhàng, hát theo hoặc chơi nhạc cụ để giải tỏa cảm xúc."
                }
            ]
            
            for resource in resources:
                with st.expander(f"📖 {resource['title']}"):
                    st.write(resource['content'])
        
        st.divider()
        
        st.subheader("🎯 Kỹ năng đối phó với căng thẳng")
        
        coping_skills = [
            "💝 Chấp nhận cảm xúc: Mọi cảm xúc đều có lý do và đáng được tôn trọng",
            "🌱 Chia sẻ: Tìm người tin cậy để trò chuyện",
            "🎨 Sáng tạo: Vẽ, viết, hoặc chơi nhạc để thể hiện cảm xúc",
            "🏃 Vận động: Đi bộ, tập yoga hoặc chơi thể thao",
            "🌳 Kết nối với thiên nhiên: Dành thời gian ở ngoài trời",
            "📵 Nghỉ ngơi kỹ thuật số: Tạm ngưng sử dụng mạng xã hội",
            "🎯 Đặt mục tiêu nhỏ: Hoàn thành những việc nhỏ mỗi ngày",
            "🕒 Thực hành lòng trắc ẩn: Đối xử tử tế với chính mình"
        ]
        
        for skill in coping_skills:
            st.write(f"- {skill}")

    def run(self):
        """Chạy ứng dụng chính"""
        self.init_session_state()
        page = self.render_sidebar()
        
        # Render nội dung theo trang được chọn
        if page == "💬 Trò chuyện với AI":
            self.render_chat_interface()
        elif page == "📊 Nhật ký cảm xúc":
            self.render_analytics_dashboard()
        elif page == "🌻 Tài nguyên hỗ trợ":
            self.render_resources_page()

# ==================== CHẠY ỨNG DỤNG ====================

if __name__ == "__main__":
    app = MentalHealthWebApp()
    app.run()