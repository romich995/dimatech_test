from hashlib import sha256

from settings import SALT

def hash_password(password: str)-> str:
    return sha256(f"{password}{SALT}".encode()).hexdigest()
