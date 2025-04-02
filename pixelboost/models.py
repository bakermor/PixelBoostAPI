from datetime import date

from beanie import Document
from pydantic import BaseModel, EmailStr, field_validator, Field


class Stat(BaseModel):
    current_level: float
    last_updated: date | None = None
    equation: list[float]

    @field_validator("current_level")
    def constrain_values(cls, value: float) -> float:
        return max(0.0, min(100.0, value))

class Health(BaseModel):
    hunger: Stat
    thirst: Stat
    energy: Stat
    social: Stat
    fun: Stat
    hygiene: Stat

# MongoDB
class User(Document):
    username: str
    name: str
    email: EmailStr
    is_verified: bool = False
    password: str

    health: Health

    class Settings:
        name = "users"
