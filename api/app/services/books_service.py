from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.book_model import Book
from fastapi import HTTPException, status
from typing import List, Optional
from app.exceptions.BookNotFoundException import BookNotFoundException

def get_all_books(db: Session) -> List[Book]:
    try:
        books = db.query(Book).all()

        if not books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No books found in the database."
            )

        return books

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error accessing the database: {str(e)}"
        )
    
def get_books_by_title_and_category(db: Session, title: str = None, category: str = None) -> List[Book]:
    try:
        query = db.query(Book)
        
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%")) 
        if category:
            query = query.filter(Book.category.ilike(f"%{category}%"))

        books = query.all()
        if not books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No books found in the database."
            )
        
        return books

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error accessing the database: {str(e)}"
        )

def get_book_by_id(db: Session, book_id: int) -> Optional[Book]:
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        
        if not book:
            raise BookNotFoundException(book_id)
            
        return book
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error accessing the database: {str(e)}"
        )