from datetime import date
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from uuid import UUID
from enum import Enum

from .employee import EmployeeBase


class VacationType(Enum):
    UNPAID_LEAVE = "Unpaid leave"
    PAID_LEAVE = "Paid leave"


class VacationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    type: VacationType
    start_date: date
    end_date: date
    employee_id: Optional[UUID] = None

    @field_validator("start_date", "end_date")
    def check_vacation_dates(cls, value, field):
        # Performs the checks
        if not value:
            raise ValueError(f"{field.name!r} ne peut pas être vide")
        return value

    # @field_validator("type")
    # def validate_type(cls, value):
    #     if isinstance(value, VacationType):
    #         return value.value
    #     raise ValueError("Invalid type value")


class VacationEmployeeBase(VacationBase):
    employee_name: Optional[EmployeeBase]
