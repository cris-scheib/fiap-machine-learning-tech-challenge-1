from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.book_model import Book
from app.schemas.book_schema import BookSchema
from app.services import books_service
from app.core.auth import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=List[BookSchema])
def list_books(
        db: Session = Depends(get_db)
): return books_service.get_all_books(db)

@router.get("/search", response_model=List[BookSchema])
def list_books_by_title_and_category(
        title: Optional[str] = None,
        category: Optional[str] = None,
        db: Session = Depends(get_db)
):  return books_service.get_books_by_title_and_category(db, title, category)

