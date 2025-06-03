


import json
import os

SESSION_FILE = "utils/.session.json"

def set_current_user(user_id: int):
    with open(SESSION_FILE, "w") as f:
        json.dump({"user_id": user_id}, f)

def get_current_user():
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r") as f:
        data = json.load(f)
        return data.get("user_id")

def clear_current_user():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)