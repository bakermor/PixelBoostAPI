from pydantic import BaseModel
from beanie import PydanticObjectId

class UserRead(BaseModel):
    id: PydanticObjectId
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str
