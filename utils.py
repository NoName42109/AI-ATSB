# utils.py
import streamlit as st
import requests

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
            return f"Lỗi Gemini API: {response.status_code}"
    except Exception as e:
        return f"Lỗi kết nối: {str(e)}"

def generate_ai_response(user_message, user_info):
    """Tạo phản hồi từ Gemini với context người dùng"""
    
    # Context chuyên môn tâm lý học đường
    psychology_context = """
KIẾN THỨC CHUYÊN MÔN TÂM LÝ HỌC ĐƯỜNG:

1. TÂM LÝ LỨA TUỔI HỌC SINH:
- Tuổi dậy thì: Thay đổi tâm sinh lý, hình thành nhân cách
- Khủng hoảng tuổi teen: Tìm kiếm bản sắc, áp lực bạn bè
- Phát triển nhận thức: Tư duy trừu tượng, khả năng phê phán

2. VẤN ĐỀ THƯỜNG GẶP:
- Áp lực học tập, thi cử
- Mâu thuẫn gia đình, bạn bè
- Định hướng tương lai, nghề nghiệp
- Rối loạn cảm xúc, stress, lo âu
- Vấn đề tự tin, tự trọng

3. PHƯƠNG PHÁP HỖ TRỢ:
- Lắng nghe tích cực, đồng cảm
- Kỹ năng giải quyết vấn đề
- Quản lý cảm xúc, stress
- Xây dựng mục tiêu, kế hoạch
- Kỹ năng giao tiếp, xã hội

4. NGUYÊN TẮC TƯ VẤN:
- Không phán xét, không chỉ trích
- Tôn trọng quyết định của học sinh
- Bảo mật thông tin
- Hướng dẫn tự giải quyết vấn đề
- Kết nối với chuyên gia khi cần
"""

    # Lấy lịch sử gần đây
    recent_history = get_recent_history()
    
    # Tạo prompt với context người dùng
    prompt = f"""
BẠN LÀ CHUYÊN GIA TÂM LÝ HỌC ĐƯỜNG được đào tạo bài bản.

THÔNG TIN NGƯỜI DÙNG:
- Họ tên: {user_info['full_name']}
- Tuổi: {user_info['age']}
- Giới tính: {user_info['gender']}
- Lớp: {user_info['grade']}
- Trường: {user_info.get('school', 'Chưa cung cấp')}
- Vấn đề quan tâm: {user_info['concern']}
- Thông tin bổ sung: {user_info.get('additional_info', 'Không có')}

{psychology_context}

LỊCH SỬ TRÒ CHUYỆN GẦN ĐÂY:
{recent_history}

TIN NHẮN HIỆN TẠI:
"{user_message}"

HÃY TRÒ CHUYỆN VỚI TƯ CÁCH:
- Người bạn lớn tin cậy, thấu hiểu
- Chuyên gia tâm lý đồng cảm, không phán xét
- Người hướng dẫn tận tâm, hỗ trợ

NGUYÊN TẮC PHẢN HỒI:
1. LẮNG NGHE & ĐỒNG CẢM: Thể hiện sự thấu hiểu cảm xúc
2. PHÂN TÍCH & ĐỊNH HƯỚNG: Giúp học sinh tự nhận thức vấn đề
3. GỢI Ý GIẢI PHÁP: Đưa ra phương án thực tế, khả thi
4. ĐỘNG VIÊN & TRAO QUYỀN: Khuyến khích tự quyết định
5. AN TOÀN & BẢO MẬT: Đảm bảo thông tin riêng tư

LƯU Ý QUAN TRỌNG:
- KHÔNG chẩn đoán bệnh lý tâm thần
- KHÔNG thay thế bác sĩ tâm lý khi cần thiết
- KHÔNG đưa lời khuyên y tế
- LIÊN HỆ NGAY với người lớn tin cậy trong trường hợp khẩn cấp

Trả lời bằng tiếng Việt tự nhiên, gần gũi, phù hợp với lứa tuổi học sinh.
"""

    return call_gemini_api(prompt)

def get_recent_history():
    """Lấy lịch sử gần đây"""
    if 'conversation_history' not in st.session_state:
        return "Chưa có lịch sử trò chuyện"
    
    if not st.session_state.conversation_history:
        return "Chưa có lịch sử trò chuyện"
    
    recent = st.session_state.conversation_history[-6:]  # Lấy 6 tin nhắn gần nhất
    history_text = ""
    for msg in recent:
        speaker = "Học sinh" if msg["role"] == "user" else "Chuyên gia"
        history_text += f"{speaker}: {msg['message']}\n"
    return history_text
