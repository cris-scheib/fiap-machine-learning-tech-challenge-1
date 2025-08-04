from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import cast, Float
from app.entities.book_entity import Book
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
        book = db.query(Book).filter(book_id == Book.id).first()
        
        if not book:
            raise BookNotFoundException(book_id)
            
        return book
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error accessing the database: {str(e)}"
        )

def get_top_rated_books(db: Session, limit: int = 10) -> List[Book]:
    try:
        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }

        books = db.query(Book).all()
        books_sorted = sorted(
            books,
            key=lambda b: rating_map.get(b.rating, 0),
            reverse=True
        )
        return books_sorted[:limit]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching top-rated books: {str(e)}")

def get_books_by_price_range(db: Session, min_price: float, max_price: float) -> List[Book]:
    try:
        books = db.query(Book).filter(
            cast(Book.price, Float) >= min_price,
            cast(Book.price, Float) <= max_price
        ).all()
        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books found in the specified price range.")
        return books
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching books by price range: {str(e)}")