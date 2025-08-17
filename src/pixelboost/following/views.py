from typing import Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Query

from .service import get_followers, get_following, follow, unfollow, remove, search
from ..auth.models import UserRead
from ..auth.service import CurrentUser

router = APIRouter(tags=["Users", "Following"])

@router.get("/search", response_model=list[UserRead])
async def search_users(search_term: str):
    users = await search(search_term)
    return users

@router.get("/followers/{user_id}", response_model=list[UserRead])
async def get_user_followers(user_id: PydanticObjectId, search_term: Optional[str] = Query(None, min_length=1)):
    users = await get_followers(user_id, search_term)
    return users

@router.get("/following/{user_id}", response_model=list[UserRead])
async def get_user_following(user_id: PydanticObjectId, search_term: Optional[str] = Query(None, min_length=1)):
    users = await get_following(user_id, search_term)
    return users

@router.post("/follow/remove/{user_id}", response_model=UserRead)
async def remove_follower(user_id: PydanticObjectId, current_user: CurrentUser):
    user = await remove(user_id, current_user)
    return user

@router.post("/follow/{user_id}", response_model=UserRead)
async def follow_user(user_id: PydanticObjectId, current_user: CurrentUser):
    user = await follow(user_id, current_user)
    return user

@router.post("/unfollow/{user_id}", response_model=UserRead)
async def unfollow_user(user_id: PydanticObjectId, current_user: CurrentUser):
    user = await unfollow(user_id, current_user)
    return user
