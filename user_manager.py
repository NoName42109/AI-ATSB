# user_manager.py
import uuid
from datetime import datetime

class UserManager:
    def __init__(self):
        self.users = {}
    
    def generate_user_id(self):
        """Tạo ID người dùng duy nhất"""
        return str(uuid.uuid4())[:8]
    
    def register_user(self, user_info):
        """Đăng ký người dùng mới"""
        user_id = self.generate_user_id()
        user_info['user_id'] = user_id
        user_info['created_at'] = datetime.now().isoformat()
        self.users[user_id] = user_info
        return user_id
    
    def get_user_info(self, user_id):
        """Lấy thông tin người dùng"""
        return self.users.get(user_id)
