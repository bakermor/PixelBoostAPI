from pydantic import BaseModel, field_validator, model_validator


class StatUpdate(BaseModel):
    current_level: float
    last_updated: float

    @field_validator("current_level")
    def constrain_values(cls, value: float) -> float:
        return max(0.0, min(100.0, value))

class HealthUpdate(BaseModel):
    hunger: StatUpdate
    thirst: StatUpdate
    energy: StatUpdate
    social: StatUpdate
    fun: StatUpdate
    hygiene: StatUpdate

class EquationUpdate(BaseModel):
    hunger: float
    thirst: float
    energy: float
    social: float
    fun: float
    hygiene: float
