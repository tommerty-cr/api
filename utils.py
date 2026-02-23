import os
import json


def get_user(id):
    users = load_users()
    for user in users:
        if user["id"] == id:
            return user


def load_users(filepath="users.json"):
    try:
        f = open(filepath)
        data = json.load(f)
        return data
    except:
        return []


def save_user(user, existing=[]):
    existing.append(user)
    with open("users.json", "w") as f:
        json.dump(existing, f)


def delete_user(id):
    users = load_users()
    users = [u for u in users if u["id"] != id]
    f = open("users.json", "w")
    json.dump(users, f)


password = os.getenv("PASSWORD", "admin123")
