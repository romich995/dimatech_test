import bcrypt

from settings import SALT

def hash_password(password: str)-> str:
    #return bcrypt.hashpw(password.encode(), SALT.encode()).decode()
    return password