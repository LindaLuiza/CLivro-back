from datetime import datetime
from pydantic import BaseModel, UUID7

from clubs.schemas import ClubOut
from users.schemas import UserOut


class MemberOut(BaseModel):
    id: UUID7
    club_id: UUID7
    user_id: UUID7
    registered_at: datetime
    clubs: None | ClubOut
    users: None | UserOut
