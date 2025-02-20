from pydantic import BaseModel, ConfigDict, field_validator
import re

from .checks import (
    TEAM_NAME_MIN_LENGTH,
    TEAM_NAME_MAX_LENGTH,
    TEAM_AUTHORIZED_CHARACTERS,
)


class TeamBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    team_name: str

    @field_validator("team_name")
    def check_employee_data(cls, value, field):
        # Performs the checks
        if len(value) < TEAM_NAME_MIN_LENGTH:
            raise ValueError(
                f"{field.name!r} doit comporter au moins {TEAM_NAME_MIN_LENGTH} caractères"
            )
        if len(value) > TEAM_NAME_MAX_LENGTH:
            raise ValueError(
                f"{field.name!r} ne doit pas dépasser {TEAM_NAME_MAX_LENGTH} caractères"
            )
        invalid_chars = set(re.findall(f"[^{TEAM_AUTHORIZED_CHARACTERS}]", value))
        if invalid_chars:
            raise ValueError(
                f'{field.name!r} contient des caractères invalides : {"".join(invalid_chars)}'
            )
        return value
