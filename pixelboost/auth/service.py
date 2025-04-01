from typing import Annotated

from beanie import PydanticObjectId
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from pixelboost.models import User
from .models import UserRegister, UserUpdate, UserUpdateEmail, UserUpdatePassword, Token
from .utils import hash_password, create_access_token, create_refresh_token, verify_token, verify_refresh_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get(user_id: PydanticObjectId) -> User:
    user = await User.get(user_id)
    return user

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

async def validate_user(user_id: PydanticObjectId, current_user: User):
    user = await get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='A user with this id does not exist')
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    return user

async def update(user_id: PydanticObjectId, user_in: UserUpdate):
    update_data = user_in.model_dump(exclude_unset=True)
    await User.find_one(User.id == user_id).update({"$set": update_data})
    user = await User.get(user_id)
    return user

async def update_username(user: User, username: str):
    user.username = username
    await user.save()
    return user

async def update_email(user: User, user_in: UserUpdateEmail):
    user.email = user_in.email
    user.is_verified = False
    await user.save()
    return user

async def set_password(user_in: User, password: UserUpdatePassword) -> User:
    user_in.password = hash_password(password.new_password)
    await user_in.save()
    return user_in

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
