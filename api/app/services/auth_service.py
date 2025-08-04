from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.token_schema import Token, RefreshTokenRequest
from app.core.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    refresh_access_token
)


def login_for_access_token(
    db: Session,
    username: str,
    password: str
) -> Token:
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User or password incorrect"
        )

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


def refresh_token_service(
    refresh_token: str,
    db: Session
) -> Token:
    tokens = refresh_access_token(refresh_token, db)
    return Token(**tokens)
