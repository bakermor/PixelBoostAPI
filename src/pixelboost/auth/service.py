import time
from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends, Response, Request

from .models import UserRegister, UserUpdate, UserUpdateEmail, UserUpdatePassword
from .utils import (OAuth2PasswordBearerWithCookie, create_access_token, create_refresh_token, hash_password,
                    verify_token, verify_refresh_token)
from ..config import JWT_EXP, JWT_REFRESH_EXP
from ..exceptions import BAD_TOKEN, USER_NOT_FOUND
from ..models import User, Health, Stat

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")

async def get(user_id: PydanticObjectId) -> User:
    user = await User.get(user_id, fetch_links=True)
    return user

async def get_by_username(username: str) -> User:
    user = await User.find_one({'username': username}, fetch_links=True)
    return user

async def create(user_in: UserRegister) -> User:
    user_in.password = hash_password(user_in.password)
    user_data = user_in.model_dump()
    user_data["health"] = Health(hunger=Stat(current_level=0, equation=[0.0014815]),
                                 thirst=Stat(current_level=0, equation=[0.0014815]),
                                 energy=Stat(current_level=0, equation=[0.0011575]),
                                 social=Stat(current_level=0, equation=[0.0005555]),
                                 fun=Stat(current_level=0, equation=[0.0011575]),
                                 hygiene=Stat(current_level=0, equation=[0.0006945]))
    user = await User.insert_one(User(**user_data))
    return user

async def login(user_in: User, response: Response):
    access_token = create_access_token(user_in.username)
    refresh_token = create_refresh_token(user_in.username)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=JWT_EXP)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=JWT_REFRESH_EXP)
    return

async def refresh(request: Request, response: Response):
    refresh_token: str = request.cookies.get("refresh_token")
    if not refresh:
        raise BAD_TOKEN

    username = verify_refresh_token(refresh_token)
    if not username:
        raise BAD_TOKEN
    user = await get_by_username(username)
    if not user:
        raise BAD_TOKEN

    access_token = create_access_token(username)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, max_age=JWT_EXP)
    return

async def validate_user(user_id: PydanticObjectId, current_user: User):
    user = await get(user_id)
    if not user:
        raise USER_NOT_FOUND
    if user.id != current_user.id:
        raise BAD_TOKEN
    return user

async def update(user_id: PydanticObjectId, user_in: UserUpdate):
    update_data = user_in.model_dump(exclude_unset=True)
    await User.find_one(User.id == user_id).update({"$set": update_data})
    user = await User.get(user_id, fetch_links=True)
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

async def delete(user: User):
    await user.delete()

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    username = verify_token(token)
    if not username:
        raise BAD_TOKEN
    user = await get_by_username(username)
    if not user:
        raise BAD_TOKEN
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
