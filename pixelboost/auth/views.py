from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .models import UserRead, UserRegister, Token
from .service import get_by_username, create, login, CurrentUser
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

    response = await login(user)
    return response

@router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUser):
    return current_user
