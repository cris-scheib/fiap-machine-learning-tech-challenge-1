from sqlalchemy.orm import Session
from app.entities.book_entity import Book
from typing import List

def get_all_categories(db: Session) -> List[str]:
    categories = db.query(Book.category).distinct().all()
    return categories