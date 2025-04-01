from pixelboost.models import User
from .utils import hash_password, create_access_token
from .models import UserRegister, UserLoginResponse, Token, UserRead

async def get_by_username(username: str) -> User:
    user = await User.find_one({'username': username})
    return user

async def create(user_in: UserRegister) -> User:
    user_in.password = hash_password(user_in.password)
    user = await User.insert_one(User(**user_in.model_dump()))
    return user

async def login(user_in: User) -> UserLoginResponse:
    access_token = create_access_token(user_in.username)
    print(access_token)
    token = Token(access_token=access_token, token_type="bearer")

    return UserLoginResponse(user=UserRead(**user_in.model_dump()), token=token)
