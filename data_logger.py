# data_logger.py
import requests
import json
from datetime import datetime
import os

class DataLogger:
    def __init__(self):
        self.server_url = "http://192.168.102.22:5000"  # Địa chỉ máy chủ
        self.data_dir = "./user_data"
        
        # Tạo thư mục lưu trữ nếu chưa tồn tại
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def log_user_login(self, user_info):
        """Ghi log đăng nhập người dùng"""
        try:
            # Gửi về server
            data = {
                'type': 'user_login',
                'timestamp': datetime.now().isoformat(),
                'user_info': user_info
            }
            self._send_to_server(data)
            
            # Lưu file local theo user_id
            user_id = user_info['user_id']
            filename = f"{self.data_dir}/user_{user_id}_login.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Lỗi ghi log đăng nhập: {e}")
    
    def log_chat_message(self, message_data):
        """Ghi log tin nhắn chat"""
        try:
            # Gửi về server
            data = {
                'type': 'chat_message',
                'timestamp': datetime.now().isoformat(),
                'message_data': message_data
            }
            self._send_to_server(data)
            
            # Lưu file local theo user_id và thời gian
            user_id = message_data['user_id']
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.data_dir}/user_{user_id}_chat_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Lỗi ghi log chat: {e}")
    
    def _send_to_server(self, data):
        """Gửi dữ liệu về máy chủ"""
        try:
            response = requests.post(
                f"{self.server_url}/api/log",
                json=data,
                timeout=5
            )
            if response.status_code == 200:
                print("✅ Đã gửi dữ liệu về server")
            else:
                print(f"❌ Lỗi gửi server: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Không thể kết nối server: {e}")
    
    def export_user_data(self, user_id):
        """Xuất toàn bộ dữ liệu người dùng"""
        user_files = []
        for filename in os.listdir(self.data_dir):
            if f"user_{user_id}" in filename:
                user_files.append(filename)
        
        return {
            'user_id': user_id,
            'total_files': len(user_files),
            'files': user_files
        }
