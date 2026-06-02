import json
import os

USERS_FILE = "users.json"

class Score:
    def get_high_score(self, username: str) -> int:
        """UC11: Đọc điểm cao nhất của người chơi."""
        if not os.path.exists(USERS_FILE):
            return 0
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
        return data.get("users", {}).get(username, {}).get("high_score", 0)

    def save_if_high_score(self, username: str, score: int) -> bool:
        """UC11: Lưu điểm nếu cao hơn kỷ lục cũ. Trả về True nếu là kỷ lục mới."""
        if not os.path.exists(USERS_FILE):
            return False
        with open(USERS_FILE, "r") as f:
            data = json.load(f)

        users = data.get("users", {})

        """thuyvy sua ham khoi tao tk tam cho player 2"""
        if username not in users:
            users[username] = {"password": "", "high_score": 0}
        # ----------------------------------------------------------------

        current_best = users.get(username, {}).get("high_score", 0)

        if score > current_best:
            users[username]["high_score"] = score
            data["users"] = users
            with open(USERS_FILE, "w") as f:
                json.dump(data, f, indent=2)
            return True
        return False
