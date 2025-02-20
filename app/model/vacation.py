from typing import TYPE_CHECKING
from sqlalchemy import Enum, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel
from .custom_uuid import CustomUUID

if TYPE_CHECKING:
    from .employee import EmployeeModel


class VacationModel(BaseModel):
    __tablename__ = "vacation"
    type: Mapped[str] = mapped_column(
        Enum("Unpaid leave", "Paid leave"), nullable=False
    )
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)

    # Define relationships and other fields as needed
    employee_id: Mapped[CustomUUID] = mapped_column(
        CustomUUID, ForeignKey("employee.id")
    )
    employee: Mapped["EmployeeModel"] = relationship(
        "EmployeeModel", back_populates="vacations"
    )
