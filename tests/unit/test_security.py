import pytest
from app.core.security import hash_password, verify_password

def test_hash_password():
    """Test password hashing."""
    password = "testpassword"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)

def test_verify_password():
    """Test password verification."""
    password = "testpassword"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)