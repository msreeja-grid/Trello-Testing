import pytest
from unittest.mock import patch
from app.utils.jwt import create_token, decode_token

def test_create_token():
    """Test token creation."""
    data = {"user_id": 1}
    token = create_token(data)
    assert isinstance(token, str)
    assert len(token) > 0

def test_decode_token():
    """Test token decoding."""
    data = {"user_id": 1}
    token = create_token(data)
    decoded = decode_token(token)
    assert decoded is not None
    assert decoded["user_id"] == 1

def test_decode_invalid_token():
    """Test decoding invalid token."""
    decoded = decode_token("invalid_token")
    assert decoded is None