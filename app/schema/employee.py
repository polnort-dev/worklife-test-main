from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
import re

from .checks import (
    EMPLOYEE_NAME_MIN_LENGTH,
    EMPLOYEE_NAME_MAX_LENGTH,
    EMPLOYEE_AUTHORIZED_CHARACTERS,
)


class EmployeeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: str
    team_name: Optional[str]

    @field_validator("first_name", "last_name")
    def check_employee_name(cls, value, field):
        # Performs the checks
        if len(value) < EMPLOYEE_NAME_MIN_LENGTH:
            raise ValueError(
                f"{field.name!r} doit comporter au moins {EMPLOYEE_NAME_MIN_LENGTH} caractères"
            )
        if len(value) > EMPLOYEE_NAME_MAX_LENGTH:
            raise ValueError(
                f"{field.name!r} ne doit pas dépasser {EMPLOYEE_NAME_MAX_LENGTH} caractères"
            )
        invalid_chars = set(re.findall(f"[^{EMPLOYEE_AUTHORIZED_CHARACTERS}]", value))
        if invalid_chars:
            raise ValueError(
                f'{field.name!r} contient des caractères invalides : {"".join(invalid_chars)}'
            )
        return value
