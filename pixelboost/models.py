from datetime import date

from beanie import Document
from pydantic import BaseModel, EmailStr, field_validator, Field


class Stat(BaseModel):
    current_level: float
    last_updated: float | None = None
    equation: list[float]

    @field_validator("current_level")
    def constrain_values(cls, value: float) -> float:
        return max(0.0, min(100.0, value))

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "current_level": 50.0,
                    "last_updated": 1743654156.04459,
                    "equation": []
                }]}}

class Health(BaseModel):
    hunger: Stat
    thirst: Stat
    energy: Stat
    social: Stat
    fun: Stat
    hygiene: Stat

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
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
                    }}]}}

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

class Activity(Document):
    name: str

    class Settings:
        name = "activities"
