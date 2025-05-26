from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID7


class ClubIn(BaseModel):
    name: str
    description: str


class ClubOut(BaseModel):
    id: UUID7
    name: str
    description: str | None
    owner_id: UUID7
    created_at: datetime
    updated_at: datetime | None
