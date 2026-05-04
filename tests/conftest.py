import sys
import os
# Add src to path for imports
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, src_path)

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.base import Base
from app.db.session import get_db

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test_trello.db"

# Create test engine
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Create all tables
    Base.metadata.create_all(bind=test_engine)

    # Create a session
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

    # Drop all tables after test
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database session override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def auth_client(client, db_session):
    """Create an authenticated test client."""
    # Register a user
    user_data = {
        "email": "test@example.com",
        "password": "testpass",
        "first_name": "Test",
        "last_name": "User"
    }
    client.post("/auth/register", json=user_data)

    # Login to get token
    login_data = {
        "username": "test@example.com",
        "password": "testpass"
    }
    response = client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]

    # Set authorization header
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client