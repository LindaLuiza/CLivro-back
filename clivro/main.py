from typing import Annotated

from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from clivro.database import engine, Base, get_db

# from users.models import User as UserModel
# from users.schemas import UserOut
# from users.utils import get_current_user

from clubs.controllers import router as clubs_router
from members.controllers import router as members_router
from users.controllers import router as users_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(clubs_router, prefix="/clubs", tags=["clubs"])
app.include_router(members_router, prefix="/clubs/{club_id}/members", tags=["members"])


# @app.get("/", response_model=UserOut, status_code=status.HTTP_200_OK)
# async def get_user(user: Annotated[UserModel, Depends(get_current_user)]):
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
#     return user
