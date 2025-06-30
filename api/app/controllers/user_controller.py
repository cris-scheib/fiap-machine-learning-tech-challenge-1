from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from api.app.schemas.user_schema import UserCreate, UserOut, Token
from api.app.core.database import get_db
from api.app.services import user_service
from api.app.core.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
)

router = APIRouter()

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    user_obj = user_service.create_user(db, user)
    return user_obj


@router.post("/token", response_model=Token)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="User or password incorrect")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def read_users_me(current_user=Depends(get_current_user)):
    return current_user
