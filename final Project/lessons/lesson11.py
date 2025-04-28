# lessons/lesson11.py
import bcrypt

# Simulated in-memory user database
user_list = [
    {
        "userid": 1,
        "username": "admin",
        "password": bcrypt.hashpw(b"admin123", bcrypt.gensalt())
    },
    {
        "userid": 2,
        "username": "test",
        "password": bcrypt.hashpw(b"test123", bcrypt.gensalt())
    }
]

def get_user_by_username(username):
    return next((u for u in user_list if u['username'] == username), None)

def add_user(username, password):
    new_user = {
        "userid": len(user_list) + 1,
        "username": username,
        "password": bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    }
    user_list.append(new_user)
