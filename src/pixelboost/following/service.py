import re
from typing import Optional

from beanie import PydanticObjectId

from ..auth.service import get
from ..exceptions import USER_NOT_FOUND
from ..models import User


async def search(search_term: str) -> list[User]:
    regex = {"$regex": f"^{re.escape(search_term)}", "$options": "i"}
    users = await User.find(
        {
            "$or": [
                {"username": regex},
                {"name": regex},
            ]
        }
    ).to_list()
    return users

async def get_followers(user_id: PydanticObjectId, search_term: Optional[str] = None) -> list[User]:
    user = await get(user_id)
    if not user:
        raise USER_NOT_FOUND

    query = {"_id": {"$in": user.followers}}

    if search_term:
        regex = {"$regex": f"^{re.escape(search_term)}", "$options": "i"}
        query["$or"] = [
            {"username": regex},
            {"name": regex}
        ]

    users = await User.find(query).to_list()
    return users


async def get_following(user_id: PydanticObjectId, search_term: Optional[str] = None) -> list[User]:
    user = await get(user_id)
    if not user:
        raise USER_NOT_FOUND

    query = {"_id": {"$in": user.following}}

    if search_term:
        regex = {"$regex": f"^{re.escape(search_term)}", "$options": "i"}
        query["$or"] = [
            {"username": regex},
            {"name": regex}
        ]

    users = await User.find(query).to_list()
    return users

async def follow(user_id: PydanticObjectId, current_user: User) -> User:
    user = await get(user_id)
    if not user:
        raise USER_NOT_FOUND

    if current_user.id not in user.followers and current_user.id != user.id:
        user.followers.append(current_user.id)
        current_user.following.append(user_id)

        await user.save()
        await current_user.save()

    return current_user

async def unfollow(user_id: PydanticObjectId, current_user: User) -> User:
    user = await get(user_id)
    if not user:
        raise USER_NOT_FOUND

    if current_user.id in user.followers:
        user.followers.remove(current_user.id)
        current_user.following.remove(user_id)

        await user.save()
        await current_user.save()

    return current_user

async def remove(user_id: PydanticObjectId, current_user: User) -> User:
    user = await get(user_id)
    if not user:
        raise USER_NOT_FOUND

    await unfollow(current_user.id, user)

    return await get(current_user.id)
