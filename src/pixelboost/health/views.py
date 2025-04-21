from beanie import PydanticObjectId
from fastapi import APIRouter, status

from .service import update, update_one
from .models import StatUpdate
from ..auth.service import validate_user, CurrentUser
from ..enums import Stats
from ..exceptions import Responses, BAD_STAT
from ..models import Health

router = APIRouter(tags=["Health"])

@router.get("/{user_id}",
            response_model=Health,
            responses={status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401,
                       status.HTTP_404_NOT_FOUND: Responses.USER_404})
async def get_health(user_id: PydanticObjectId, current_user: CurrentUser):
    """
    Get health stats for user.
    """
    user = await validate_user(user_id, current_user)
    return user.health

@router.patch("/{user_id}",
              response_model=Health,
              responses={status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401,
                         status.HTTP_404_NOT_FOUND: Responses.USER_404})
async def update_health(user_id: PydanticObjectId, updated_health: Health, current_user: CurrentUser):
    """
    Update all health stats for user.
    """
    user = await validate_user(user_id, current_user)
    user_out = await update(user, updated_health)
    return user_out.health

@router.patch("/{user_id}/{stat}",
              response_model=Health,
              responses={status.HTTP_400_BAD_REQUEST: Responses.STAT_400,
                         status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401,
                         status.HTTP_404_NOT_FOUND: Responses.USER_404})
async def update_stat(user_id: PydanticObjectId, stat: str, updated_stat: StatUpdate, current_user: CurrentUser):
    """
    Update one health stat for user.
    """
    user = await validate_user(user_id, current_user)
    if stat not in Stats:
        raise BAD_STAT
    user_out = await update_one(user, stat, updated_stat)
    return user_out.health
