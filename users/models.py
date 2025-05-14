from datetime import datetime

from clivro.database import Base
from sqlalchemy import UUID, Column, String, DateTime
from uuid_extensions import uuid7


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True, default=uuid7())
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime)
