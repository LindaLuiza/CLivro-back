from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from uuid_extensions import uuid7
from uuid import UUID

from clivro.database import get_db

from users.models import User as UserModel
from users.utils import get_current_user

from .models import Member as MemberModel
from .schemas import MemberOut

router = APIRouter()


@router.get('', response_model=list[MemberOut], status_code=status.HTTP_200_OK)
def list_members(club_id: UUID, db: Session = Depends(get_db)):
    members = (db
               .query(MemberModel)
               .options(joinedload(MemberModel.users), joinedload(MemberModel.clubs))
               .filter(MemberModel.club_id == club_id)
               .all()
               )
    return members


@router.post('', response_model=MemberOut, status_code=status.HTTP_201_CREATED)
def create_member(club_id: UUID, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    member = MemberModel(club_id=club_id, user_id=user.id)
    db.add(member)
    db.commit()
    return member


@router.get('/user', response_model=MemberOut, status_code=status.HTTP_200_OK)
def get_member(club_id: UUID, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    member = db.query(MemberModel).filter(MemberModel.club_id == club_id, MemberModel.user_id == user.id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return member


@router.delete('/{member_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_member(club_id: UUID, member_id: UUID, db: Session = Depends(get_db)):
    member = db.query(MemberModel).filter(MemberModel.club_id == club_id, MemberModel.id == member_id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(member)
    db.commit()
    return
