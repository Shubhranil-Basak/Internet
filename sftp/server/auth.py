from .config import USERS

def authenticate(username, password):
    return USERS.get(username) == password
