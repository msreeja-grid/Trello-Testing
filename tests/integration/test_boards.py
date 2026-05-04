import pytest

def test_create_board(auth_client):
    """Test creating a board."""
    board_data = {
        "name": "Test Board",
        "description": "A test board"
    }
    response = auth_client.post("/boards/", json=board_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == board_data["name"]
    assert data["description"] == board_data["description"]
    assert "id" in data

def test_get_boards(auth_client):
    """Test getting user's boards."""
    # Create a board first
    board_data = {
        "name": "Test Board",
        "description": "A test board"
    }
    auth_client.post("/boards/", json=board_data)

    # Get boards
    response = auth_client.get("/boards/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == board_data["name"]

def test_get_board(auth_client):
    """Test getting a specific board."""
    # Create a board first
    board_data = {
        "name": "Test Board",
        "description": "A test board"
    }
    create_response = auth_client.post("/boards/", json=board_data)
    board_id = create_response.json()["id"]

    # Get the board
    response = auth_client.get(f"/boards/{board_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == board_data["name"]
    assert "sections" in data
    assert "tickets" in data
    assert "users" in data

def test_get_nonexistent_board(auth_client):
    """Test getting a nonexistent board."""
    response = auth_client.get("/boards/999")
    assert response.status_code == 404
    assert "Board not found" in response.json()["detail"]

def test_invite_user_to_board(auth_client, client, db_session):
    """Test inviting a user to a board."""
    from app.models.user import User

    # Create another user
    user_data = {
        "email": "invitee@example.com",
        "password": "testpass",
        "first_name": "Invitee",
        "last_name": "User"
    }
    client.post("/auth/register", json=user_data)

    # Create a board
    board_data = {
        "name": "Test Board",
        "description": "A test board"
    }
    create_response = auth_client.post("/boards/", json=board_data)
    board_id = create_response.json()["id"]

    # Invite the user
    invite_data = {"email": "invitee@example.com"}
    response = auth_client.post(f"/boards/{board_id}/invite", json=invite_data)
    assert response.status_code == 200
    data = response.json()
    assert "token" in data