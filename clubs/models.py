from datetime import datetime

from sqlalchemy.orm import relationship

from clivro.database import Base
from sqlalchemy import UUID, Column, String, DateTime
from uuid_extensions import uuid7

from members.models import Member


class Club(Base):
    __tablename__ = 'clubs'

    id = Column(UUID, primary_key=True, default=uuid7)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    owner_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime)

    members = relationship("Member", back_populates="clubs")
