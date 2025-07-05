from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.book_model import Book
from fastapi import HTTPException, status
from typing import List

def get_all_categories(db: Session) -> List[CategorySchema]:
    categories = db.query(Book.category).all().distinct().all()
    return categories