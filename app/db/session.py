from functools import lru_cache
from typing import Iterator

from fastapi_utils.session import FastAPISessionMaker
from sqlalchemy.orm import Session

from app.core.config import settings


def get_db() -> Iterator[Session]:
    """FastAPI dependency that provides a sqlalchemy session"""
    yield from _get_fastapi_sessionmaker().get_db()


@lru_cache()
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    """This function could be replaced with a global variable if preferred"""
    if settings.SQLALCHEMY_DATABASE_URI is None:
        raise ValueError("SQLALCHEMY_DATABASE_URI is not set in the configuration")
    return FastAPISessionMaker(settings.SQLALCHEMY_DATABASE_URI.unicode_string())
