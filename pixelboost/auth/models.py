from beanie import PydanticObjectId, Link
from pydantic import BaseModel, EmailStr, Field, field_validator

from ..models import Health, Activity


class UserBase(BaseModel):
    username: str
    email: EmailStr
    name: str

class UserRead(UserBase):
    id: PydanticObjectId
    current_activity: Link[Activity] | None

    health: Health

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "67ee079d43f1a19fe37afe79",
                    "username": "rosieTheCat",
                    "email": "giveMeFood@gmail.com",
                    "name": "Rosie Cat",
                    
                    "health": {
                        "hunger": {
                            "current_level": 50.0,
                            "last_updated": 1743654156.04459,
                            "equation": []
                        },
                        "thirst": {
                            "current_level": 72.0,
                            "last_updated": 1743654156.04459,
                            "equation": []
                        },
                        "energy": {
                            "current_level": 13.0,
                            "last_updated": 1743654156.04459,
                            "equation": []
                        },
                        "social": {
                            "current_level": 45.0,
                            "last_updated": 1743654156.04459,
                            "equation": []
                        },
                        "fun": {
                            "current_level": 90.0,
                            "last_updated": 1743654178.2973874,
                            "equation": []
                        },
                        "hygiene": {
                            "current_level": 67.0,
                            "last_updated": 1743654156.04459,
                            "equation": []
                        }}}]}}

class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=24, pattern=r"^[a-zA-Z0-9_.-]+$",
                          description="Username must be 3-24 chars: letters, numbers, underscores, dots, or hyphens")
    email: EmailStr
    password: str
    name: str

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

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "rosieTheCat",
                    "email": "giveMeFood@gmail.com",
                    "password": "I4m$uperCool",
                    "name": "Rosie Cat"
                }]}}

class UserUpdate(BaseModel):
    name: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Rosie Cat"
                }]}}

class UserUpdateEmail(BaseModel):
    email: EmailStr

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "giveMeFood@gmail.com",
                }]}}

class UserUpdateUsername(BaseModel):
    username: str = Field(min_length=3, max_length=24, pattern=r"^[a-zA-Z0-9_.-]+$")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "rosieTheCat",
                }]}}

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

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "current_password": "I4m$uperCool",
                    "new_password": "Cut3$tCat1nT0wn"
                }]}}
