import uuid
from sqlalchemy.dialects import postgresql


class CustomUUID(postgresql.UUID):
    python_type = uuid.UUID
