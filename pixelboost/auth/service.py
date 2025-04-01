from typing import Annotated

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from pixelboost.models import User
from .models import UserRegister, Token
from .utils import hash_password, create_access_token, create_refresh_token, verify_token, verify_refresh_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_by_username(username: str) -> User:
    user = await User.find_one({'username': username})
    return user

async def create(user_in: UserRegister) -> User:
    user_in.password = hash_password(user_in.password)
    user = await User.insert_one(User(**user_in.model_dump()))
    return user

async def login(user_in: User) -> Token:
    access_token = create_access_token(user_in.username)
    refresh_token = create_refresh_token(user_in.username)
    token = Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)
    return token

async def refresh(refresh_token: str) -> Token:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_refresh_token(refresh_token)
    if not username:
        raise credentials_exception
    user = await get_by_username(username)
    if not user:
        raise credentials_exception

    access_token = create_access_token(username)
    token = Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)
    return token

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_token(token)
    if not username:
        raise credentials_exception
    user = await get_by_username(username)
    if not user:
        raise credentials_exception
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
