from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.book_model import Book
from fastapi import HTTPException, status
from typing import List

def get_all_books(db: Session) -> List[Book]:
    try:
        books = db.query(Book).all()

        if not books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum livro encontrado na base de dados."
            )

        return books

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao acessar o banco de dados: {str(e)}"
        )
    
def get_books_by_title_and_category(db: Session, title: str = None, category: str = None) -> List[Book]:
    try:
        query = db.query(Book)
        
        if title:
            query = query.filter(Book.title == title)
        if category:
            query = query.filter(Book.category == category)

        books = query.all()
        if not books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum livro encontrado na base de dados."
            )

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao acessar o banco de dados: {str(e)}"
        )