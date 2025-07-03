from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.core.database import get_db
from app.models.book_model import Book
from app.schemas.book_schema import BookSchema
from app.services import books_service

router = APIRouter()

@router.get("/", response_model=List[BookSchema])
def list_books(db: Session = Depends(get_db)):
    return books_service.get_all_books(db)

@router.get("/search", response_model=List[BookSchema])
def list_books_by_title_and_category(title: str, category: str, db: Session = Depends(get_db)):
    try:
        books = books_service.get_books_by_title_and_category(db, title, category)
        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        return books
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))