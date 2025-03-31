from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from .models import UserRead
from .service import get, get_all

router = APIRouter()

# TEST
@router.get("/", response_model=list[UserRead])
async def get_users():
    users = await get_all()
    return users

@router.get("/{userID}", response_model=UserRead)
async def get_user(userID: PydanticObjectId):
    user = await get(userID)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} not found"
        )
    return user
