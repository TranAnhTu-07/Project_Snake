import json
import os

USERS_FILE = "users.json"

class Leaderboard:
    def get_top(self, n: int = 10) -> list[tuple[str, int]]:
        """UC7: Trả về top-N người chơi theo điểm cao nhất."""
        if not os.path.exists(USERS_FILE):
            return []
        with open(USERS_FILE, "r") as f:
            data = json.load(f)

        users = data.get("users", {})
        scores = [
            (username, info.get("high_score", 0))
            for username, info in users.items()
        ]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:n]
