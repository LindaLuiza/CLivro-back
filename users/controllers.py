from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid_extensions import uuid7

from clivro.database import get_db
from clivro.settings import settings
from .models import User as UserModel
from .schemas import UserIn, UserOut, Token, UserUpdate
from .utils import get_password_hash, authenticate_user, create_access_token, get_current_user

router = APIRouter()

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/token")


@router.post('/signup', response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_login(data: UserIn, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(data.password)
    try:
        user = UserModel(id=uuid7(), name=data.name, email=data.email, username=data.username,
                         hashed_password=hashed_password)
        db.add(user)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "username" in str(e.orig):
            detail = "Username already exists"
        elif "email" in str(e.orig):
            detail = "Email already exists"
        else:
            detail = "Could not create receiver"
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
    return user


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


@router.put("/me")
def update_user_info(data: UserUpdate, db: Session = Depends(get_db),
                     user: UserModel = Depends(get_current_user)):
    if data.name:
        user.name = data.name
    if data.email:
        user.email = data.email
    if data.username:
        user.username = data.username
    db.commit()
    return user


@router.post("/forgot-password")
def forgot_password(email: EmailStr, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token_data = {"sub": user.email, "exp": datetime.utcnow() + timedelta(hours=1)}
    reset_token = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {"token": reset_token}


@router.post("/reset-password")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = get_password_hash(new_password)
    db.commit()

    return {"msg": "Password updated successfully"}
