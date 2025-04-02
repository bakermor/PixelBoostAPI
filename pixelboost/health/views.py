from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from .service import update, update_one
from ..auth.service import validate_user, CurrentUser
from ..enums import Stats
from ..models import Health, Stat

router = APIRouter()

@router.get("/{user_id}", response_model=Health)
async def get_health(user_id: PydanticObjectId, current_user: CurrentUser):
    print(user_id)
    user = await validate_user(user_id, current_user)
    return user.health

@router.patch("/{user_id}", response_model=Health)
async def update_health(user_id: PydanticObjectId, updated_health: Health, current_user: CurrentUser):
    user = await validate_user(user_id, current_user)
    user_out = await update(user, updated_health)
    return user_out.health

@router.patch("/{user_id}/{stat}", response_model=Health)
async def update_stat(user_id: PydanticObjectId, stat: str, updated_stat: Stat, current_user: CurrentUser):
    user = await validate_user(user_id, current_user)
    if stat not in Stats:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid stat")
    user_out = await update_one(user, stat, updated_stat)
    return user_out.health
