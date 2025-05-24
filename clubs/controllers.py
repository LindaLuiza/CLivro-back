from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid_extensions import uuid7
from uuid import UUID

from clivro.database import get_db

from users.models import User as UserModel
from users.utils import get_current_user

from .models import Club as ClubModel
from .schemas import ClubIn, ClubOut

router = APIRouter()


@router.get('', response_model=list[ClubOut], status_code=status.HTTP_200_OK)
def list_clubs(db: Session = Depends(get_db)):
    clubs = db.query(ClubModel).all()
    return clubs


@router.post('', response_model=ClubOut, status_code=status.HTTP_201_CREATED)
def create_club(club: ClubIn, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        club = ClubModel(id=uuid7(), name=club.name, description=club.description, owner_id=str(user.id))
        db.add(club)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "name" in str(e.orig):
            detail = "Club already exists"
        else:
            detail = "Could not create receiver"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    return club


@router.get('/owner', response_model=list[ClubOut], status_code=status.HTTP_200_OK)
def get_club_by_owner_id(user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    clubs = db.query(ClubModel).filter(ClubModel.owner_id == str(user.id)).all()
    return clubs


@router.get('/{club_id}', response_model=ClubOut, status_code=status.HTTP_200_OK)
def get_club(club_id: UUID, db: Session = Depends(get_db)):
    club = db.query(ClubModel).filter(ClubModel.id == club_id).first()
    if club is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str('Club does not exist'))
    return club


@router.put('/{club_id}', response_model=ClubOut, status_code=status.HTTP_200_OK)
def update_club(club_id: UUID, data: ClubIn, db: Session = Depends(get_db)):
    club = db.query(ClubModel).filter(ClubModel.id == club_id).first()
    if club is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str('Club does not exist'))
    club.name = data.name
    club.description = data.description
    club.updated_at = datetime.utcnow()
    db.commit()
    return club


@router.delete('/{club_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_club(club_id: UUID, db: Session = Depends(get_db)):
    club = db.query(ClubModel).filter(ClubModel.id == club_id).first()
    if club is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str('Club does not exist'))
    db.delete(club)
    db.commit()
    return club
