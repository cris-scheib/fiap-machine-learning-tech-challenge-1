from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.entities.book_entity import Book
from fastapi import HTTPException, status
from typing import List

def get_all_categories(db: Session) -> List[str]:
    try:
        categories = db.query(Book.category).distinct().all()
        return categories
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error accessing the database: {str(e)}"
        )