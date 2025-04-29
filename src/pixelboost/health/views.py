from beanie import PydanticObjectId
from fastapi import APIRouter, status

from .service import update, update_one
from .models import StatUpdate, HealthUpdate
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

@router.patch("",
              response_model=Health,
              responses={status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401})
async def update_health(updated_health: HealthUpdate, current_user: CurrentUser):
    """
    Update all health stats for user.
    """
    user_out = await update(current_user, updated_health)
    return user_out.health

@router.patch("/equations", response_model=Health)
async def update_equations():
    pass

@router.patch("/{stat}",
              response_model=Health,
              responses={status.HTTP_400_BAD_REQUEST: Responses.STAT_400,
                         status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401})
async def update_stat(stat: str, updated_stat: StatUpdate, current_user: CurrentUser):
    """
    Update one health stat for user.
    """
    if stat not in Stats:
        raise BAD_STAT
    user_out = await update_one(current_user, stat, updated_stat)
    return user_out.health
