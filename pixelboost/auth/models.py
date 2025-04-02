from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator

from ..enums import Stats
from ..models import Health, Stat


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class RefreshRequest(BaseModel):
    refresh_token: str

class UserBase(BaseModel):
    username: str
    email: EmailStr
    name: str

class UserRead(UserBase):
    id: PydanticObjectId

    health: Health

class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=36)
    email: EmailStr
    password: str
    name: str

    health: Health = Health(hunger=Stat(current_level=0, equation=[1, 1]),
                            thirst=Stat(current_level=0, equation=[1, 1]),
                            energy=Stat(current_level=0, equation=[1, 1]),
                            social=Stat(current_level=0, equation=[1, 1]),
                            fun=Stat(current_level=0, equation=[1, 1]),
                            hygiene=Stat(current_level=0, equation=[1, 1]))

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

class UserUpdate(BaseModel):
    name: str | None = None

class UserUpdateEmail(BaseModel):
    email: EmailStr

class UserUpdateUsername(BaseModel):
    username: str = Field(min_length=3, max_length=36)

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
