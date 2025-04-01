from fastapi import APIRouter, HTTPException, status

from pixelboost.models import User
from .models import UserRead, UserRegister, UserLogin, UserLoginResponse
from .service import get_by_username, create, login
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

@router.post("/login", response_model=UserLoginResponse)
async def login_user(user_in: UserLogin):
    user = await get_by_username(user_in.username)

    if not user or not verify_password(user_in.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid username and password')

    response = login(user)
