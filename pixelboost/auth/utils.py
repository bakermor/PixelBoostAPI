from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from pixelboost.config import JWT_ALG, JWT_EXP, JWT_SECRET


def hash_password(password: str):
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)

def verify_password(password: str, hashed: bytes) -> bool:
    if not password or not hashed:
        return False
    return bcrypt.checkpw(password.encode("utf-8"), hashed)

def create_access_token(username: str):
    expire = datetime.now(timezone.utc) + timedelta(seconds=JWT_EXP)
    data = {
        "exp": expire,
        "username": username,
    }
    encoded_jwt = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALG)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except jwt.PyJWTError:
        return None
