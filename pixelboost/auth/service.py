from pixelboost.models import User
from .utils import hash_password


async def get_by_username(username: str) -> User:
    user = await User.find_one({'username': username})
    return user

async def create(user_in: User) -> User:
    user_in.password = hash_password(user_in.password)

    user = await User.insert_one(user_in)
    return user
