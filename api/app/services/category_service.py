from app.schemas.category_schema import CategorySchema
from sqlalchemy.orm import Session
from app.models.book_model import Book
from typing import List

def get_all_categories(db: Session) -> List[str]:
    categories = db.query(Book.category).distinct().all()
    return categories