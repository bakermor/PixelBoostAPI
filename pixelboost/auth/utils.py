from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt
from fastapi import HTTPException, status, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param

from ..config import (JWT_ALG, JWT_EXP, JWT_SECRET, JWT_REFRESH_ALG,
                      JWT_REFRESH_SECRET, JWT_REFRESH_EXP)

class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        return param


def hash_password(password: str):
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(pw, salt)
    return hash_bytes.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    if not password or not hashed:
        return False
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def create_access_token(username: str):
    expire = datetime.now(timezone.utc) + timedelta(seconds=JWT_EXP)
    data = {
        "exp": expire,
        "sub": username,
    }
    encoded_jwt = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALG)
    return encoded_jwt

def create_refresh_token(username: str):
    expire = datetime.now(timezone.utc) + timedelta(seconds=JWT_REFRESH_EXP)
    data = {
        "exp": expire,
        "sub": username,
    }
    encoded_jwt = jwt.encode(data, JWT_REFRESH_SECRET, algorithm=JWT_REFRESH_ALG)
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

def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, JWT_REFRESH_SECRET, algorithms=[JWT_REFRESH_ALG])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except jwt.PyJWTError:
        return None
