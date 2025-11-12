# main.py
import streamlit as st
import sys
import os
import requests
from datetime import datetime

# Thêm path để import
sys.path.append('.')

# Import components
from utils import generate_ai_response
from user_manager import UserManager
from data_logger import DataLogger

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="AI Tâm Lý Học Đường - Gemini",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Áp dụng CSS
def load_css():
    """Load CSS files"""
    try:
        if os.path.exists('./styles/main.css'):
            with open('./styles/main.css', 'r', encoding='utf-8') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Lỗi CSS: {e}")

# Khởi tạo session state
def init_session_state():
    if 'user_manager' not in st.session_state:
        st.session_state.user_manager = UserManager()
    if 'data_logger' not in st.session_state:
        st.session_state.data_logger = DataLogger()
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    if 'user_authenticated' not in st.session_state:
        st.session_state.user_authenticated = False

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
    
    # Kiểm tra đăng nhập
    if not st.session_state.user_authenticated:
        render_login_screen()
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="neon-text">👤 THÔNG TIN NGƯỜI DÙNG</h3>', unsafe_allow_html=True)
        
        # Hiển thị thông tin user
        if st.session_state.user_info:
            user_info = st.session_state.user_info
            st.markdown(f"""
            <div style="background: rgba(72, 219, 251, 0.2); padding: 15px; border-radius: 10px; margin: 10px 0;">
                <p><strong>Họ tên:</strong> {user_info['full_name']}</p>
                <p><strong>Tuổi:</strong> {user_info['age']}</p>
                <p><strong>Giới tính:</strong> {user_info['gender']}</p>
                <p><strong>Lớp:</strong> {user_info['grade']}</p>
                <p><strong>Vấn đề quan tâm:</strong> {user_info['concern']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Thông tin hệ thống
        st.markdown("---")
        st.markdown('<h4 class="neon-text">📊 THỐNG KÊ</h4>', unsafe_allow_html=True)
        st.write(f"💬 Tin nhắn: {len(st.session_state.conversation_history)}")
        st.write(f"👥 User ID: {st.session_state.user_info['user_id']}")
        
        # Nút đăng xuất
        if st.button("🚪 ĐĂNG XUẤT", use_container_width=True, type="secondary"):
            st.session_state.user_authenticated = False
            st.session_state.user_info = None
            st.session_state.conversation_history = []
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([1, 3])
    
    with col1:
        render_header()
    
    with col2:
        render_chat_interface()

def render_login_screen():
    """Màn hình đăng nhập"""
    st.markdown("""
    <div class="login-container">
        <div class="login-card">
            <h1 class="neon-text">🧠 AI TÂM LÝ HỌC ĐƯỜNG</h1>
            <p class="login-subtitle">Hệ thống hỗ trợ tâm lý học đường thông minh</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.subheader("📝 THÔNG TIN CÁ NHÂN")
        
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Họ và tên*", placeholder="Nguyễn Văn A")
            age = st.number_input("Tuổi*", min_value=10, max_value=25, value=15)
            gender = st.selectbox("Giới tính*", ["Nam", "Nữ", "Khác"])
        
        with col2:
            grade = st.text_input("Lớp*", placeholder="10A1")
            school = st.text_input("Trường", placeholder="THPT ABC")
            concern = st.selectbox("Vấn đề quan tâm*", [
                "Học tập & Thi cử",
                "Mối quan hệ bạn bè", 
                "Gia đình & Phụ huynh",
                "Định hướng tương lai",
                "Cảm xúc & Tâm lý",
                "Sức khỏe tinh thần",
                "Khác"
            ])
        
        additional_info = st.text_area("Thông tin bổ sung (nếu có)", 
                                     placeholder="Hãy chia sẻ thêm về bản thân để AI hỗ trợ tốt hơn...",
                                     height=100)
        
        agree_terms = st.checkbox("Tôi đồng ý với các điều khoản sử dụng và chính sách bảo mật*")
        
        if st.form_submit_button("🚀 BẮT ĐẦU TRÒ CHUYỆN", type="primary"):
            if not all([full_name, age, gender, grade, concern]) or not agree_terms:
                st.error("Vui lòng điền đầy đủ thông tin bắt buộc (*) và đồng ý điều khoản!")
            else:
                # Lưu thông tin user
                user_info = {
                    'user_id': st.session_state.user_manager.generate_user_id(),
                    'full_name': full_name,
                    'age': age,
                    'gender': gender,
                    'grade': grade,
                    'school': school,
                    'concern': concern,
                    'additional_info': additional_info,
                    'login_time': datetime.now().isoformat()
                }
                
                st.session_state.user_info = user_info
                st.session_state.user_authenticated = True
                
                # Gửi dữ liệu đăng nhập về server
                st.session_state.data_logger.log_user_login(user_info)
                
                st.success("✅ Đăng nhập thành công! Hãy bắt đầu trò chuyện với AI.")
                st.rerun()

def render_header():
    """Header component"""
    st.markdown("""
    <div class="cyber-card">
        <h1 class="neon-text">🧠 AI TÂM LÝ HỌC ĐƯỜNG</h1>
        
        <p class="neon-subtitle">Powered by Google Gemini</p>
        
        <p class="description">Hệ thống hỗ trợ tâm lý học đường thông minh</p>
        
        <!-- Features Section -->
        <div class="feature-card">
            <h4 class="feature-title">ĐẶC ĐIỂM NỔI BẬT</h4>
            <ul class="feature-list">
                <li>Trí tuệ nhân tạo Google Gemini</li>
                <li>Hiểu sâu vấn đề tâm lý học đường</li>
                <li>Trò chuyện tự nhiên, đồng cảm</li>
                <li>Bảo mật & Riêng tư tuyệt đối</li>
                <li>Hỗ trợ 24/7 miễn phí</li>
            </ul>
        </div>
        
        <!-- Quick Guide Section -->
        <div class="guide-card">
            <h4 class="guide-title">HƯỚNG DẪN SỬ DỤNG</h4>
            <ol class="guide-list">
                <li>Chia sẻ vấn đề của bạn</li>
                <li>AI sẽ lắng nghe và phân tích</li>
                <li>Nhận tư vấn phù hợp</li>
            </ol>
        </div>
        
        <!-- Tip Section -->
        <div class="tip-card">
            <p class="tip-text">
                Hãy chia sẻ tự nhiên như nói chuyện với người bạn đáng tin cậy. 
                Mọi thông tin đều được bảo mật!
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_chat_interface():
    """Giao diện chat"""
    st.markdown('<div class="cyber-container">', unsafe_allow_html=True)
    
    # Header chat
    st.markdown('<h2 class="neon-text" style="text-align: center; margin-bottom: 20px;">PHÒNG TÂM SỰ HỌC ĐƯỜNG</h2>', unsafe_allow_html=True)
    
    # Chat container
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    # Hiển thị lịch sử chat
    if not st.session_state.conversation_history:
        st.markdown('''
        <div class="welcome-message">
            <h3>Xin chào!</h3>
            <p>Hãy bắt đầu cuộc trò chuyện bằng cách nhập tin nhắn bên dưới.</p>
            <p>Tôi ở đây để lắng nghe và hỗ trợ bạn!</p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        for msg in st.session_state.conversation_history:
            if msg["role"] == "user":
                st.markdown(f'''
                <div class="chat-message user-message">
                    <strong>Bạn:</strong><br>
                    {msg["message"]}
                    <div class="message-time">{msg["time"]}</div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="chat-message bot-message">
                    <strong>Chuyên gia AI:</strong><br>
                    {msg["message"]}
                    <div class="message-time">{msg["time"]}</div>
                </div>
                ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Nhập tin nhắn...",
            placeholder="Hãy chia sẻ với tôi...",
            key="user_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("GỬI", use_container_width=True, type="primary")
    
    # Xử lý tin nhắn
    if send_button and user_input:
        # Thêm tin nhắn user
        user_msg = {
            "role": "user",
            "message": user_input,
            "time": datetime.now().strftime("%H:%M:%S")
        }
        st.session_state.conversation_history.append(user_msg)
        
        # Gửi dữ liệu chat về server
        chat_data = {
            'user_id': st.session_state.user_info['user_id'],
            'message': user_input,
            'timestamp': datetime.now().isoformat()
        }
        st.session_state.data_logger.log_chat_message(chat_data)
        
        # Tạo phản hồi AI
        with st.spinner("Đang phân tích và trả lời..."):
            try:
                response = generate_ai_response(user_input, st.session_state.user_info)
                
                bot_msg = {
                    "role": "bot",
                    "message": response,
                    "time": datetime.now().strftime("%H:%M:%S")
                }
                st.session_state.conversation_history.append(bot_msg)
                
                # Gửi phản hồi AI về server
                bot_data = {
                    'user_id': st.session_state.user_info['user_id'],
                    'message': response,
                    'timestamp': datetime.now().isoformat()
                }
                st.session_state.data_logger.log_chat_message(bot_data)
                
                # Refresh để hiển thị tin nhắn mới
                st.rerun()
                
            except Exception as e:
                st.error(f"Lỗi: {e}")
    
    # Hiển thị trạng thái hệ thống
    st.markdown("---")
    status_col1, status_col2 = st.columns(2)
    
    with status_col1:
        st.metric("Tin nhắn", len(st.session_state.conversation_history))
    
    with status_col2:
        st.metric("Trạng thái", "Đang hoạt động")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
