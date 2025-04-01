from beanie import PydanticObjectId
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class RefreshRequest(BaseModel):
    refresh_token: str

class UserBase(BaseModel):
    username: str

class UserRead(UserBase):
    id: PydanticObjectId

class UserRegister(BaseModel):
    username: str
    password: str
