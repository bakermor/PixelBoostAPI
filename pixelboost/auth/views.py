from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .models import (RefreshRequest, Token, UserRead, UserRegister, UserUpdate, UserUpdateEmail, UserUpdatePassword,
                     UserUpdateUsername)
from .service import (create, delete, get_by_username, login, refresh, set_password, update, update_email,
                      update_username, validate_user, CurrentUser)
from .utils import verify_password

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def register_user(user_in: UserRegister):
    user = await get_by_username(user_in.username)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Username in use')
    user = await create(user_in)
    return user

@router.post("/login", response_model=Token)
async def login_user(user_in: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await get_by_username(user_in.username)

    if not user or not verify_password(user_in.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid username or password',
                            headers={"WWW-Authenticate": "Bearer"})

    token = await login(user)
    return token

@router.post("/refresh", response_model=Token)
async def refresh_user(refresh_token: RefreshRequest):
    token = await refresh(refresh_token.refresh_token)
    return token

@router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUser):
    return current_user

@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: PydanticObjectId, user_in: UserUpdate, current_user: CurrentUser):
    await validate_user(user_id, current_user)
    user = await update(user_id, user_in)
    return user

@router.post("/{user_id}/change-username", response_model=UserRead)
async def change_username(user_id: PydanticObjectId, username_update: UserUpdateUsername, current_user: CurrentUser):
    user = await validate_user(user_id, current_user)
    user_in = await get_by_username(username_update.username)
    if user_in:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Username in use')
    user_out = await update_username(user, username_update.username)
    return user_out

@router.post("/{user_id}/change-email", response_model=UserRead)
async def change_username(user_id: PydanticObjectId, email_update: UserUpdateEmail, current_user: CurrentUser):
    user = await validate_user(user_id, current_user)
    user_out = await update_email(user, email_update)
    return user_out


@router.post("/{user_id}/change-password", response_model=UserRead)
async def change_password(user_id: PydanticObjectId, password_update: UserUpdatePassword, current_user: CurrentUser):
    user = await validate_user(user_id, current_user)
    if not verify_password(password_update.current_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid current password")
    user_out = await set_password(user, password_update)
    return user_out

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: PydanticObjectId, current_user: CurrentUser):
    user = await validate_user(user_id, current_user)
    await delete(user)
