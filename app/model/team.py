from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .employee import EmployeeModel


class TeamModel(BaseModel):
    __tablename__ = "team"
    team_name: Mapped[str] = mapped_column(String(30), nullable=False)
    employees: Mapped[list["EmployeeModel"]] = relationship(
        "EmployeeModel", back_populates="team"
    )
