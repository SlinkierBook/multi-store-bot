import bcrypt
from datetime import datetime
from bank import add_user, get_user_by_email, get_user_by_id
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())


def register_user(email, password):
    if get_user_by_email(email):
        return None
    
    password_hash = hash_password(password)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    add_user(email, password_hash, created_at)
    
    return get_user_by_email(email)


def authenticate(email, password):
    user = get_user_by_email(email)
    
    if not user:
        return None
    
    if check_password(password, user[2]):
        return User(user[0], user[1])
    
    return None


def load_user(user_id):
    user = get_user_by_id(int(user_id))
    
    if user:
        return User(user[0], user[1])
    
    return None