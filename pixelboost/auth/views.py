from fastapi import APIRouter, HTTPException, status

from pixelboost.models import User
from .models import UserRead
from .service import get_by_username, create

router = APIRouter()

@router.post("/register", response_model=UserRead)
async def register_user(user_in: User):
    user = await get_by_username(user_in.username)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Username in use')
    user = await create(user_in)
    return user
