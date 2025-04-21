from pydantic import BaseModel, field_validator, model_validator


class StatUpdate(BaseModel):
    current_level: float | None = None
    last_updated: float | None = None
    equation: list[float] | None = None

    @field_validator("current_level")
    def constrain_values(cls, value: float) -> float:
        return max(0.0, min(100.0, value))

    @model_validator(mode="after")
    def check_new_level_has_time(self) -> "StatUpdate":
        if (self.last_updated and not self.current_level) or (self.current_level and not self.last_updated):
            raise ValueError("To update 'current_level', both 'current_level' and 'last_updated' must be set")
        return self
