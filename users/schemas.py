from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID7


class UserIn(BaseModel):
    name: str
    email: EmailStr
    username: str
    password: str


class UserUpdate(BaseModel):
    name: str | None
    email: EmailStr | None
    username: str | None


class UserOut(BaseModel):
    id: UUID7
    name: str
    email: EmailStr
    username: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime | None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None
