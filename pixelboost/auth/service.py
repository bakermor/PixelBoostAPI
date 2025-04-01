from typing import Annotated

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from pixelboost.models import User
from .models import UserRegister, Token
from .utils import hash_password, create_access_token, verify_token

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
    token = Token(access_token=access_token, token_type="bearer")
    return token
    # return UserLoginResponse(user=UserRead(**user_in.model_dump()), token=token)

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
