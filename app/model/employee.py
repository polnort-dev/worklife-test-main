from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .custom_uuid import CustomUUID

if TYPE_CHECKING:
    from .team import TeamModel
    from .vacation import VacationModel


class EmployeeModel(BaseModel):
    __tablename__ = "employee"
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    team_id: Mapped[CustomUUID] = mapped_column(CustomUUID, ForeignKey("team.id"))

    team: Mapped["TeamModel"] = relationship("TeamModel", back_populates="employees")
    vacations: Mapped[list["VacationModel"]] = relationship(
        "VacationModel", back_populates="employee"
    )


if __name__ == "__main__":
    a = EmployeeModel(
        {
            "first_name": "John",
            "last_name": "Doe",
            "team_id": "123e4567-e89b-12d3-a456-426614174000",
        }
    )
