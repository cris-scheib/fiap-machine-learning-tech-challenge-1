import os
import sys
import pytest
from fastapi import HTTPException
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))
from app.entities.book_entity import Book
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.custom_exceptions import BookNotFoundException
from app.services.books_service import (
    get_all_books,
    get_books_by_title_and_category,
    get_book_by_id,
    get_top_rated_books,
    get_books_by_price_range
)


class TestBooksService:
    """Testes para o serviço de livros."""
    
    def test_get_all_books_success(self, db_session, multiple_books):
        """Testa a busca de todos os livros com sucesso."""
        books = get_all_books(db_session)
        
        assert len(books) == 3
        assert all(isinstance(book, Book) for book in books)
        assert books[0].title == "Python Programming"
    
    def test_get_all_books_empty_database(self, db_session):
        """Testa a busca de livros em banco vazio."""
        books = get_all_books(db_session)

        assert isinstance(books, list)
        assert books == []
        assert len(books) == 0
    
    def test_get_all_books_database_error(self, db_session, monkeypatch):
        """Testa erro de banco ao buscar todos os livros."""

        def fake_query(*args, **kwargs):
            raise SQLAlchemyError("Banco inacessível")

        monkeypatch.setattr(db_session, "query", fake_query)

        with pytest.raises(HTTPException) as exc_info:
            get_all_books(db_session)

        assert exc_info.value.status_code == 500
        assert "Error accessing the database" in exc_info.value.detail
    
    def test_get_books_by_title_success(self, db_session, multiple_books):
        """Testa a busca de livros por título."""
        books = get_books_by_title_and_category(db_session, title="Python")
        
        assert len(books) == 1
        assert books[0].title == "Python Programming"
    
    def test_get_books_by_category_success(self, db_session, multiple_books):
        """Testa a busca de livros por categoria."""
        books = get_books_by_title_and_category(db_session, category="Technology")
        
        assert len(books) == 2
        assert all(book.category == "Technology" for book in books)
    
    def test_get_books_by_title_and_category_success(self, db_session, multiple_books):
        """Testa a busca de livros por título e categoria."""
        books = get_books_by_title_and_category(
            db_session, 
            title="Data", 
            category="Technology"
        )
        
        assert len(books) == 1
        assert books[0].title == "Data Science Handbook"
        assert books[0].category == "Technology"
    
    def test_get_books_by_title_not_found(self, db_session, multiple_books):
        """Testa busca por título que não existe."""
        books = get_books_by_title_and_category(db_session, title="Nonexistent")

        assert isinstance(books, list)
        assert books == []
        assert len(books) == 0
    
    def test_get_book_by_id_success(self, db_session, sample_book):
        """Testa a busca de livro por ID com sucesso."""
        book = get_book_by_id(db_session, sample_book.id)
        
        assert book.id == sample_book.id
        assert book.title == sample_book.title
        assert isinstance(book, Book)
    
    def test_get_book_by_id_not_found(self, db_session):
        """Testa busca por ID que não existe."""
        with pytest.raises(BookNotFoundException) as exc_info:
            get_book_by_id(db_session, 999)
        
        assert "999" in str(exc_info.value)
    
    def test_get_book_by_id_database_error(self, db_session):
        """Testa erro de banco ao buscar livro por ID."""
        db_session.close()
        
        with pytest.raises(BookNotFoundException):
            get_book_by_id(db_session, 1)
    
    def test_get_top_rated_books_success(self, db_session, multiple_books):
        """Testa a busca de livros mais bem avaliados."""
        books = get_top_rated_books(db_session, limit=2)
        
        assert len(books) == 2
        assert books[0].rating == "Five"
        assert books[0].title == "Python Programming"
        assert books[1].rating == "Four"
    
    def test_get_top_rated_books_with_limit(self, db_session, multiple_books):
        """Testa a busca de livros mais bem avaliados com limite."""
        books = get_top_rated_books(db_session, limit=1)
        
        assert len(books) == 1
        assert books[0].rating == "Five"
    
    def test_get_books_by_price_range_success(self, db_session, multiple_books):
        """Testa a busca de livros por faixa de preço."""
        books = get_books_by_price_range(db_session, min_price=20.0, max_price=50.0)
        
        assert len(books) == 1
        assert books[0].title == "Python Programming"
        assert float(books[0].price) == 45.99
    
    def test_get_books_by_price_range_not_found(self, db_session, multiple_books):
        """Testa busca por faixa de preço sem resultados."""
        books = get_books_by_price_range(db_session, min_price=200.0, max_price=500.0)

        assert isinstance(books, list)
        assert books == []
        assert len(books) == 0
    
    def test_get_books_by_price_range_database_error(self, db_session, monkeypatch):
        """Testa erro de banco ao buscar por faixa de preço."""

        def fake_query(*args, **kwargs):
            raise SQLAlchemyError("Banco inacessível")

        monkeypatch.setattr(db_session, "query", fake_query)

        with pytest.raises(HTTPException) as exc_info:
            get_all_books(db_session)

        assert exc_info.value.status_code == 500
        assert "Error accessing the database" in exc_info.value.detail