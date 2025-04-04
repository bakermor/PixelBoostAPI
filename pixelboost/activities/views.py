from beanie import PydanticObjectId
from fastapi import APIRouter, status

from .models import ActivityBase, ActivityRead, ActivityStart, ActivityUpdate
from .service import create, delete, get, get_all, start, stop, update
from ..auth.service import CurrentUser
from ..exceptions import Responses

router = APIRouter(tags=["Activities"])

@router.post("/",
             response_model=ActivityRead,
             responses={status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401})
async def create_activity(activity: ActivityBase, current_user: CurrentUser):
    """
    Create Activity and add it to the current user's collection
    """
    activity_out = await create(activity, current_user)
    return activity_out

@router.get("/",
            response_model=list[ActivityRead],
            responses={status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401})
async def get_all_activities(current_user: CurrentUser):
    """
    Get all activities owned by the current user
    """
    activities = await get_all(current_user)
    return activities

@router.get("/{activity_id}",
            response_model=ActivityRead,
            responses={status.HTTP_401_UNAUTHORIZED: Responses.ACTIVITY_401,
                       status.HTTP_404_NOT_FOUND: Responses.ACTIVITY_404})
async def get_activity(activity_id: PydanticObjectId, current_user: CurrentUser):
    """
    Get activity with the given activity_id if it belongs to the current user
    """
    activity = await get(activity_id, current_user)
    return activity

@router.post("/{activity_id}/start",
             status_code=status.HTTP_204_NO_CONTENT,
             responses={status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401,
                        status.HTTP_404_NOT_FOUND: Responses.ACTIVITY_404,
                        status.HTTP_409_CONFLICT: Responses.ACTIVITY_409})
async def start_activity(activity_id: PydanticObjectId, time: ActivityStart, current_user: CurrentUser):
    await start(activity_id, time.start_time, current_user)

@router.post("/{activity_id}/stop",
             status_code=status.HTTP_204_NO_CONTENT,
             responses={status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401,
                        status.HTTP_404_NOT_FOUND: Responses.ACTIVITY_404})
async def stop_activity(activity_id: PydanticObjectId, current_user: CurrentUser):
    await stop(activity_id, current_user)

@router.patch("/{activity_id}",
              response_model=ActivityRead,
              responses={status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401,
                         status.HTTP_404_NOT_FOUND: Responses.ACTIVITY_404,
                         status.HTTP_409_CONFLICT: Responses.ACTIVITY_409})
async def update_activity(activity_id: PydanticObjectId, updated_data: ActivityUpdate, current_user: CurrentUser):
    activity = await update(activity_id, updated_data, current_user)
    return activity

@router.delete("/{activity_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               responses={status.HTTP_401_UNAUTHORIZED: Responses.TOKEN_401,
                          status.HTTP_404_NOT_FOUND: Responses.ACTIVITY_404})
async def delete_activity(activity_id: PydanticObjectId, current_user: CurrentUser):
    await delete(activity_id, current_user)
