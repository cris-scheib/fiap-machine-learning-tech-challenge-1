import os
import sys
import pytest
from fastapi import HTTPException
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))
from app.core.auth import create_access_token


class TestBookController:
    """Testes para o controlador de livros."""
    
    def test_list_books_success(self, client, multiple_books, sample_user):
        """Testa a listagem de todos os livros."""
        
        token_data = {"sub": sample_user.username}
        token = create_access_token(token_data)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/api/v1/books/", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["title"] == "Python Programming"
    
    def test_list_books_empty(self, client, db_session, sample_user):
        """Testa a listagem quando não há livros."""
        
        token_data = {"sub": sample_user.username}
        token = create_access_token(token_data)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/api/v1/books/", headers=headers)
        
        assert response.status_code == 404
        assert "No books found" in response.json()["detail"]
    
    def test_search_books_by_title(self, client, multiple_books, sample_user):
        """Testa a busca de livros por título."""
        
        token_data = {"sub": sample_user.username}
        token = create_access_token(token_data)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/api/v1/books/search?title=Python", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Python Programming"
    
    def test_search_books_by_category(self, client, multiple_books, sample_user):
        """Testa a busca de livros por categoria."""
        
        token_data = {"sub": sample_user.username}
        token = create_access_token(token_data)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/api/v1/books/search?category=Technology", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(book["category"] == "Technology" for book in data)
    
    def test_search_books_by_title_and_category(self, client, multiple_books, sample_user):
        """Testa a busca de livros por título e categoria."""
        
        token_data = {"sub": sample_user.username}
        token = create_access_token(token_data)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/api/v1/books/search?title=Data&category=Technology", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Data Science Handbook"
    
    def test_search_books_not_found(self, client, multiple_books, sample_user):
        """Testa busca que não retorna resultados."""
        
        token_data = {"sub": sample_user.username}
        token = create_access_token(token_data)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/api/v1/books/search?title=Nonexistent", headers=headers)
        
        assert response.status_code == 404
        assert "No books found" in response.json()["detail"]
    
    def test_get_book_by_id_success(self, client, sample_book, sample_user):
        """Testa a busca de livro por ID."""
        
        token_data = {"sub": sample_user.username}
        token = create_access_token(token_data)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get(f"/api/v1/books/{sample_book.id}", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_book.id
        assert data["title"] == sample_book.title
    
    def test_get_book_by_id_not_found(self, client, db_session, sample_user):
        """Testa busca por ID que não existe."""
        
        token_data = {"sub": sample_user.username}
        token = create_access_token(token_data)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/api/v1/books/999", headers=headers)
        
        assert response.status_code == 404
        assert "999" in str(response.json()["detail"])
    
    def test_get_book_invalid_id(self, client, sample_user):
        """Testa busca com ID inválido."""
        
        token_data = {"sub": sample_user.username}
        token = create_access_token(token_data)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/api/v1/books/0", headers=headers)
        
        assert response.status_code == 422
    
    def test_top_rated_books(self, client, multiple_books, sample_user):
        """Testa a busca de livros mais bem avaliados."""
        
        token_data = {"sub": sample_user.username}
        token = create_access_token(token_data)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/api/v1/books/top-rated?limit=2", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["rating"] == "Five"
    
    def test_books_by_price_range(self, client, multiple_books, sample_user):
        """Testa a busca de livros por faixa de preço."""
        
        token_data = {"sub": sample_user.username}
        token = create_access_token(token_data)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/api/v1/books/price-range?min=20.0&max=50.0", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Python Programming"
    
    def test_books_by_price_range_not_found(self, client, multiple_books, sample_user):
        """Testa busca por faixa de preço sem resultados."""
        
        token_data = {"sub": sample_user.username}
        token = create_access_token(token_data)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/api/v1/books/price-range?min=100.0&max=200.0", headers=headers)
        
        assert response.status_code == 404
        assert "No books found in the specified price range" in response.json()["detail"]
    
    def test_unauthorized_access(self, client):
        """Testa acesso sem autenticação."""
        response = client.get("/api/v1/books/")
        
        assert response.status_code == 401