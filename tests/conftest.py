import os
import sys
import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))
from app.core.database import Base, get_db
from app.entities.book_entity import Book
from app.entities.user_entity import User
from main import app

fake = Faker('pt_BR')

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Cria uma sessão de banco de dados para testes."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Cria um cliente de teste FastAPI."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_book_data():
    """Dados de exemplo para um livro."""
    return {
        "id": 1,
        "title": "Test Book",
        "price": "29.99",
        "availability": "In stock",
        "rating": "Four",
        "category": "Fiction",
        "image_url": "https://example.com/book.jpg"
    }

@pytest.fixture
def sample_book(db_session, sample_book_data):
    """Cria um livro de exemplo no banco de dados."""
    book = Book(**sample_book_data)
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)
    return book

@pytest.fixture
def multiple_books(db_session):
    """Cria múltiplos livros para testes."""
    books_data = [
        {
            "title": "Python Programming",
            "price": "45.99",
            "availability": "In stock",
            "rating": "Five",
            "category": "Technology",
            "image_url": "https://example.com/python.jpg"
        },
        {
            "title": "Data Science Handbook",
            "price": "55.99",
            "availability": "Out of stock",
            "rating": "Four",
            "category": "Technology",
            "image_url": "https://example.com/datascience.jpg"
        },
        {
            "title": "Fiction Novel",
            "price": "19.99",
            "availability": "In stock",
            "rating": "Three",
            "category": "Fiction",
            "image_url": "https://example.com/fiction.jpg"
        }
    ]
    
    books = []
    for book_data in books_data:
        book = Book(**book_data)
        db_session.add(book)
        books.append(book)
    
    db_session.commit()
    for book in books:
        db_session.refresh(book)
    
    return books

@pytest.fixture
def sample_user_data():
    """Dados de exemplo para um usuário."""
    return {
        "username": "testuser",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # secret
    }

@pytest.fixture
def sample_user(db_session, sample_user_data):
    """Cria um usuário de exemplo no banco de dados."""
    user = User(**sample_user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user