from datetime import datetime

from clivro.database import Base
from sqlalchemy import UUID, Column, String, DateTime
from uuid_extensions import uuid7


class Club(Base):
    __tablename__ = 'clubs'

    id = Column(UUID, primary_key=True, default=uuid7())
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    owner_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime)
