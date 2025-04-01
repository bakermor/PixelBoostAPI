from pydantic import BaseModel
from beanie import PydanticObjectId

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    username: str

class UserRead(UserBase):
    id: PydanticObjectId

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    password: str

class UserLoginResponse(BaseModel):
    user: UserRead
    token: Token
