import pytest
from app.models.user import User
from app.core.security import hash_password

def test_register_user(client, db_session):
    """Test user registration."""
    user_data = {
        "email": "test@example.com",
        "password": "testpass",
        "first_name": "Test",
        "last_name": "User"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["first_name"] == user_data["first_name"]
    assert data["last_name"] == user_data["last_name"]
    assert "id" in data

def test_register_duplicate_email(client, db_session):
    """Test registering with duplicate email."""
    user_data = {
        "email": "test@example.com",
        "password": "testpass",
        "first_name": "Test",
        "last_name": "User"
    }
    # Create first user
    client.post("/auth/register", json=user_data)
    # Try to create duplicate
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_login_success(client, db_session):
    """Test successful login."""
    # Create user first
    user_data = {
        "email": "test@example.com",
        "password": "testpass",
        "first_name": "Test",
        "last_name": "User"
    }
    client.post("/auth/register", json=user_data)

    # Login
    login_data = {
        "username": "test@example.com",
        "password": "testpass"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client, db_session):
    """Test login with invalid credentials."""
    login_data = {
        "username": "wrong@example.com",
        "password": "wrongpass"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]