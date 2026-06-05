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
            return False, "Username and password cannot be empty!"
        if len(username) < 3:
            return False, "Username must be at least 3 characters!"
        if len(password) < 4:
            return False, "Password must be at least 4 characters!"

        data = _load_data()
        if username in data["users"]:
            return False, f"Username '{username}' already exists!"

        data["users"][username] = {
            "password": _hash_password(password),
            "high_score": 0
        }
        _save_data(data)
        return True, f"Registration successful! Welcome {username}!"

    def login(self, username: str, password: str) -> tuple[bool, str]:
        """UC2: Đăng nhập."""
        if not username or not password:
            return False, "Please enter username and password!"

        data = _load_data()
        if username not in data["users"]:
            return False, "Account does not exist!"

        stored_hash = data["users"][username]["password"]
        if stored_hash != _hash_password(password):
            return False, "Incorrect password!"

        return True, f"Login successful! Welcome {username}!"
