from pixelboost.models import User
from .utils import hash_password
from .models import UserRegister, UserLoginResponse

async def get_by_username(username: str) -> User:
    user = await User.find_one({'username': username})
    return user

async def create(user_in: UserRegister) -> User:
    user_in.password = hash_password(user_in.password)
    user = await User.insert_one(User(**user_in.model_dump()))
    return user

async def login(user_in: User) -> UserLoginResponse:
    pass
