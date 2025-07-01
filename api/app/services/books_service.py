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