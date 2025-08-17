from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, status, Depends, Query, Response, Request
from fastapi.security import OAuth2PasswordRequestForm

from .models import CheckUsername, UserRead, UserRegister, UserUpdate, UserUpdateEmail, UserUpdatePassword, \
    UserUpdateUsername
from .service import (create, delete, get_by_username, login, refresh, set_password, update, update_email,
                      update_username, validate_user, CurrentUser)
from .utils import verify_password
from ..exceptions import Responses, USERNAME_CONFLICT, BAD_LOGIN, INCORRECT_PASSWORD, USER_NOT_FOUND

user_router = APIRouter(tags=["Users"])
auth_router = APIRouter(tags=["Auth"])

@auth_router.post("/token",
                  status_code=status.HTTP_204_NO_CONTENT,
                  responses={status.HTTP_401_UNAUTHORIZED: Responses.LOGIN_401})
async def login_user(response: Response, user_in: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Login with credentials to get JWT token cookie.
    """
    user = await get_by_username(user_in.username)

    if not user or not verify_password(user_in.password, user.password):
        raise BAD_LOGIN

    await login(user, response)

@auth_router.post("/refresh",
                  status_code=status.HTTP_204_NO_CONTENT,
                  responses={status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401})
async def refresh_user(request: Request, response: Response):
    """
    Use refresh token cookie to get a new JWT token cookie.
    """
    await refresh(request, response)

@auth_router.get("/me",
                 response_model=UserRead,
                 responses={status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401})
async def get_me(current_user: CurrentUser):
    """
    Returns the logged-in user's information.
    """
    return current_user

@user_router.get("/check-username", response_model=CheckUsername)
async def check_username(username: str = Query(min_length=3, max_length=24, pattern=r"^[a-zA-Z0-9_-]+$",
                                               description="Username must be 3-24 chars: letters, numbers, underscores,"
                                               " or hyphens")):
    """
    Check if username is in use. Status is false if username is unavailable
    """
    user = await get_by_username(username)
    if user:
        return {"status": False}
    else:
        return {"status": True}

@user_router.post("/register",
                  status_code=status.HTTP_201_CREATED,
                  response_model=UserRead,
                  responses={status.HTTP_409_CONFLICT: Responses.USERNAME_409})
async def register_user(user_in: UserRegister):
    """
    Register new user.
    """
    user = await get_by_username(user_in.username)
    if user:
        raise USERNAME_CONFLICT
    user = await create(user_in)
    return user

@user_router.get("/name/{username}", response_model=UserRead)
async def get_user_by_username(username: str):
    user = await get_by_username(username)
    if not user:
        raise USER_NOT_FOUND
    else:
        return user

@user_router.patch("/{user_id}",
                   response_model=UserRead,
                   responses={status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401,
                              status.HTTP_404_NOT_FOUND: Responses.USER_404})
async def update_user(user_id: PydanticObjectId, user_in: UserUpdate, current_user: CurrentUser):
    """
    Update user's general information.
    """
    await validate_user(user_id, current_user)
    user = await update(user_id, user_in)
    return user

@user_router.patch("/{user_id}/change-username",
                  response_model=UserRead,
                  responses={status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401,
                             status.HTTP_404_NOT_FOUND: Responses.USER_404,
                             status.HTTP_409_CONFLICT: Responses.USERNAME_409})
async def change_username(user_id: PydanticObjectId, username_update: UserUpdateUsername, current_user: CurrentUser):
    """
    Change user's username.
    """
    user = await validate_user(user_id, current_user)
    user_in = await get_by_username(username_update.username)
    if user_in:
        raise USERNAME_CONFLICT
    user_out = await update_username(user, username_update.username)
    return user_out

@user_router.patch("/{user_id}/change-email",
                  response_model=UserRead,
                  responses={status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401,
                             status.HTTP_404_NOT_FOUND: Responses.USER_404})
async def change_email(user_id: PydanticObjectId, email_update: UserUpdateEmail, current_user: CurrentUser):
    """
    Change user's email.
    """
    user = await validate_user(user_id, current_user)
    user_out = await update_email(user, email_update)
    return user_out


@user_router.patch("/{user_id}/change-password",
                  response_model=UserRead,
                  responses={status.HTTP_400_BAD_REQUEST: Responses.PASSWORD_400,
                             status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401,
                             status.HTTP_404_NOT_FOUND: Responses.USER_404})
async def change_password(user_id: PydanticObjectId, password_update: UserUpdatePassword, current_user: CurrentUser):
    """
    Change user's password.
    """
    user = await validate_user(user_id, current_user)
    if not verify_password(password_update.current_password, user.password):
        raise INCORRECT_PASSWORD
    user_out = await set_password(user, password_update)
    return user_out

@user_router.delete("/{user_id}",
                    status_code=status.HTTP_204_NO_CONTENT,
                    responses={status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401,
                               status.HTTP_404_NOT_FOUND: Responses.USER_404})
async def delete_user(user_id: PydanticObjectId, current_user: CurrentUser):
    """
    Delete user.
    """
    user = await validate_user(user_id, current_user)
    await delete(user)
