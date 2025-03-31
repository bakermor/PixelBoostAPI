from beanie import PydanticObjectId
from typing import Optional
from .models import UserRead

async def get_all() -> list[UserRead]:
    users = await UserRead.find_all().to_list()
    return users

async def get(userID: PydanticObjectId) -> Optional[UserRead]:
    user = await UserRead.get(userID)
    return user
