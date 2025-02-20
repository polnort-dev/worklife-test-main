from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import MetaData
from typing import Type
from uuid import uuid4

from .custom_uuid import CustomUUID

Base: Type = declarative_base(metadata=MetaData())


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[CustomUUID] = mapped_column(
        CustomUUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid4,
    )
