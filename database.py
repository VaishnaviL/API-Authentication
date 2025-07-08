from models import UserInDB
import os
from passlib.context import CryptContext
import json
DB_FILE = "db_users.json"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _read_users():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as file:
        return json.load(file)

def _write_users(users):
    with open(DB_FILE, "w") as file:
        json.dump(users, file, indent=4)

def get_user(username: str):
    all_users_dict = _read_users()
    # print(users)
    for usern, user_data in all_users_dict[0].items():
        # print(usern, user_data)
        if username == usern:
            # print(username)
            return UserInDB(**user_data)
    return None

def update_user_password(user_data: dict, new_pass: str):
    db_users = _read_users()
    db_user_dict = db_users[0]

    username = user_data.get("username")
    hashed_password = pwd_context.hash(new_pass)

    if username in db_user_dict:
        db_user_dict[username]["hashed_password"] = hashed_password
        _write_users([db_user_dict])
    else:
        raise ValueError("User not found.")

def save_user(user: UserInDB):
    users = _read_users()
    user_dict = user.dict()
    users[0].update({user.username:user_dict})
    _write_users(users)