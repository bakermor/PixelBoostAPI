from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class RefreshRequest(BaseModel):
    refresh_token: str

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserRead(UserBase):
    id: PydanticObjectId

class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=36)
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, v):
        if not v or len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        # Check for at least one number
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        # Check for at least one uppercase and one lowercase character
        if not (any(c.isupper() for c in v) and any(c.islower() for c in v)):
            raise ValueError("Password must contain both uppercase and lowercase characters")
        return v

class UserUpdatePassword(BaseModel):
    current_password: str
    new_password: str

    @field_validator("new_password")
    def validate_password(cls, v):
        if not v or len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        # Check for at least one number
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        # Check for at least one uppercase and one lowercase character
        if not (any(c.isupper() for c in v) and any(c.islower() for c in v)):
            raise ValueError("Password must contain both uppercase and lowercase characters")
        return v
