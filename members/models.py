from datetime import datetime
from sqlalchemy import UUID, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from uuid_extensions import uuid7

from clivro.database import Base



class Member(Base):
    __tablename__ = 'members'

    id = Column(UUID, primary_key=True, default=uuid7)
    club_id = Column(UUID, ForeignKey("clubs.id"), nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    registered_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    users = relationship("User", back_populates="members")
    clubs = relationship("Club", back_populates="members")
