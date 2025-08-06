import pytest
import os
import sys
from datetime import datetime, timedelta
from unittest.mock import patch, Mock
from app.core.auth import get_password_hash, verify_password, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM
import pytest
from jose import jwt

class TestAuth:
    """Testes para o módulo de autenticação."""
    
    def test_verify_password_correct(self):
        """Testa verificação de senha correta."""
        
        password = "testpassword"
        hashed = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # hash de "secret"
        
        result = verify_password("secret", hashed)
        assert result is True
    
    def test_verify_password_incorrect(self):
        """Testa verificação de senha incorreta."""
        
        hashed = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
        
        result = verify_password("wrongpassword", hashed)
        assert result is False
    
    def test_get_password_hash(self):
        """Testa geração de hash de senha."""
        
        password = "testpassword"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed) is True
    
    def test_create_access_token(self):
        """Testa criação de token de acesso."""
        
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["sub"] == "testuser"
        assert "exp" in decoded
    
    def test_create_access_token_with_expiration(self):
        """Testa criação de token com expiração customizada."""
        
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=1)
        token = create_access_token(data, expires_delta)
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_timestamp = payload["exp"]
        current_timestamp = datetime.utcnow().timestamp()
        
        assert exp_timestamp - current_timestamp < 120
    
    def test_authenticate_user_success(self, db_session, sample_user):
        """Testa autenticação bem-sucedida."""
        
        result = authenticate_user(db_session, "testuser", "secret")
        assert result is not False
        assert result.username == "testuser"
    
    def test_authenticate_user_wrong_password(self, db_session, sample_user):
        """Testa autenticação com senha incorreta."""
        
        result = authenticate_user(db_session, "testuser", "wrongpass")
        assert result is False
    
    def test_authenticate_user_not_found(self, db_session):
        """Testa autenticação com usuário inexistente."""
        
        result = authenticate_user(db_session, "nonexistent", "password")
        assert result is False
    
    def test_get_current_user_valid_token(self, client, sample_user):
        """Testa obtenção do usuário atual com token válido."""
        
        token_data = {"sub": sample_user.username}
        token = create_access_token(token_data)
        
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/books/", headers=headers)
        
        assert response.status_code != 401
    
    def test_get_current_user_invalid_token(self, client):
        """Testa obtenção do usuário atual com token inválido."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/books/", headers=headers)
        
        assert response.status_code == 401
    
    def test_get_current_user_no_token(self, client):
        """Testa obtenção do usuário atual sem token."""
        response = client.get("/api/v1/books/")
        
        assert response.status_code == 401
    
    def test_get_current_user_expired_token(self, client, sample_user):
        """Testa obtenção do usuário atual com token expirado."""
        
        token_data = {"sub": sample_user.username}
        expired_delta = timedelta(minutes=-30)
        token = create_access_token(token_data, expired_delta)
        
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/books/", headers=headers)
        
        assert response.status_code == 401