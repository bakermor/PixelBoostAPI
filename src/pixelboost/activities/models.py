from beanie import PydanticObjectId
from pydantic import BaseModel

from ..models import Modifiers


class ActivityBase(BaseModel):
    name: str
    time_limit: float | None = None
    modifiers: Modifiers

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "working out",
                    "time_limit": 3600,
                    "modifiers": {
                        "hunger": 2,
                        "thirst": 2,
                        "energy": 2,
                        "hygiene": 3,
                        "fun": -1
                    }
                }]}}

class ActivityRead(ActivityBase):
    id: PydanticObjectId
    start_time: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "working out",
                    "time_limit": 3600.0,
                    "modifiers": {
                        "hunger": 2.0,
                        "thirst": 2.0,
                        "energy": 2.0,
                        "social": None,
                        "fun": -1.0,
                        "hygiene": 3.0
                    },
                    "id": "67eef09f8c6f20e91df04c63",
                    "start_time": 1743712586.110945
                }]}}

class ActivityStart(BaseModel):
    start_time: float

class ActivityUpdate(ActivityBase):
    name: str | None = None
    modifiers: Modifiers | None = None
