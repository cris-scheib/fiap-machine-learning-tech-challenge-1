from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserOut
from app.core.database import get_db
from app.services import user_service
from app.core.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_current_user,
    refresh_access_token
)

router = APIRouter()

@router.post("/", response_model=UserCreate)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=409, detail="Usuário já existe.")
    user_service.create_user(db, user)
    return user

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user
