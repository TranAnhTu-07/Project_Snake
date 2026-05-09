import json
import os
import hashlib

USERS_FILE = "users.json"

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def _load_data() -> dict:
    if not os.path.exists(USERS_FILE):
        return {"users": {}}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def _save_data(data: dict):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)

class Auth:
    def register(self, username: str, password: str) -> tuple[bool, str]:
        """UC1: Đăng ký tài khoản mới."""
        if not username or not password:
            return False, "Tên đăng nhập và mật khẩu không được để trống!"
        if len(username) < 3:
            return False, "Tên đăng nhập phải có ít nhất 3 ký tự!"
        if len(password) < 4:
            return False, "Mật khẩu phải có ít nhất 4 ký tự!"

        data = _load_data()
        if username in data["users"]:
            return False, f"Tên đăng nhập '{username}' đã tồn tại!"

        data["users"][username] = {
            "password": _hash_password(password),
            "high_score": 0
        }
        _save_data(data)
        return True, f"Đăng ký thành công! Chào mừng {username}!"

    def login(self, username: str, password: str) -> tuple[bool, str]:
        """UC2: Đăng nhập."""
        if not username or not password:
            return False, "Vui lòng nhập tên đăng nhập và mật khẩu!"

        data = _load_data()
        if username not in data["users"]:
            return False, "Tài khoản không tồn tại!"

        stored_hash = data["users"][username]["password"]
        if stored_hash != _hash_password(password):
            return False, "Mật khẩu không đúng!"

        return True, f"Đăng nhập thành công! Chào {username}!"
