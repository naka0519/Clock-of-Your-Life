from datetime import date
from pydantic import BaseModel, field_validator


class Config(BaseModel):
    birthday: date
    target_age: int
    theme: str = "default"

    @field_validator("target_age")
    @classmethod
    def validate_target_age(cls, v: int) -> int:
        if not (1 <= v <= 150):
            raise ValueError("target_age must be between 1 and 150")
        return v
