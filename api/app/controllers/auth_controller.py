from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.token_schema import Token, RefreshTokenRequest
from app.core.database import get_db
from app.services.auth_service import (
    login_for_access_token,
    refresh_token_service
)

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    return login_for_access_token(db, form_data.username, form_data.password)

@router.post("/refresh", response_model=Token)
async def refresh(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    return refresh_token_service(request.refresh_token, db)
