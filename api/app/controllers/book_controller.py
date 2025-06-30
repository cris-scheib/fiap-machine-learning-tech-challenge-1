from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from api.app.core.database import get_db
from api.app.models.book_model import Book
from api.app.schemas.book_schema import BookSchema

router = APIRouter()

@router.get("/", response_model=List[BookSchema])
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books