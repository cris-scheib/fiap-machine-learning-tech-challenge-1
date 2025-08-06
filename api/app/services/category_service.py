from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.entities.book_entity import Book
from app.exceptions.custom_exceptions import DatabaseException
from typing import List

def get_all_categories(db: Session) -> List[str]:
    try:
        categories = db.query(Book.category).distinct().all()
        return categories
    except SQLAlchemyError as e:
        raise DatabaseException(original_error=e)