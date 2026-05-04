import pytest
from unittest.mock import patch
from fastapi import HTTPException
from app.core.auth import get_current_user
from app.models.user import User

def test_get_current_user_valid_token(db_session):
    """Test getting current user with valid token."""
    # Create a user
    user = User(email="test@example.com", hashed_password="hashed", first_name="Test", last_name="User")
    db_session.add(user)
    db_session.commit()

    with patch('app.core.auth.decode_token', return_value={"user_id": user.id}):
        with patch('app.core.auth.get_db', return_value=db_session):
            # Mock the dependency injection
            result = get_current_user(token="fake_token", db=db_session)
            assert result.id == user.id

def test_get_current_user_invalid_token(db_session):
    """Test getting current user with invalid token."""
    with patch('app.core.auth.decode_token', return_value=None):
        with patch('app.core.auth.get_db', return_value=db_session):
            with pytest.raises(HTTPException) as exc_info:
                get_current_user(token="invalid_token", db=db_session)
            assert exc_info.value.status_code == 401

def test_get_current_user_missing_user_id(db_session):
    """Test getting current user with token missing user_id."""
    with patch('app.core.auth.decode_token', return_value={"some": "data"}):
        with patch('app.core.auth.get_db', return_value=db_session):
            with pytest.raises(HTTPException) as exc_info:
                get_current_user(token="fake_token", db=db_session)
            assert exc_info.value.status_code == 401

def test_get_current_user_user_not_found(db_session):
    """Test getting current user when user does not exist."""
    with patch('app.core.auth.decode_token', return_value={"user_id": 999}):
        with patch('app.core.auth.get_db', return_value=db_session):
            with pytest.raises(HTTPException) as exc_info:
                get_current_user(token="fake_token", db=db_session)
            assert exc_info.value.status_code == 401