import pytest

def test_create_section(auth_client):
    """Test creating a section."""
    # Create a board first
    board_data = {
        "name": "Test Board",
        "description": "A test board"
    }
    board_response = auth_client.post("/boards/", json=board_data)
    board_id = board_response.json()["id"]

    # Create a section
    section_data = {
        "name": "Test Section",
        "description": "A test section",
        "board_id": board_id
    }
    response = auth_client.post("/sections/", json=section_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == section_data["name"]
    assert data["board_id"] == board_id

def test_get_section(auth_client):
    """Test getting a section."""
    # Create a board and section first
    board_data = {
        "name": "Test Board",
        "description": "A test board"
    }
    board_response = auth_client.post("/boards/", json=board_data)
    board_id = board_response.json()["id"]

    section_data = {
        "name": "Test Section",
        "description": "A test section",
        "board_id": board_id
    }
    section_response = auth_client.post("/sections/", json=section_data)
    section_id = section_response.json()["id"]

    # Get the section
    response = auth_client.get(f"/sections/{section_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == section_data["name"]

def test_update_section(auth_client):
    """Test updating a section."""
    # Create a board and section first
    board_data = {
        "name": "Test Board",
        "description": "A test board"
    }
    board_response = auth_client.post("/boards/", json=board_data)
    board_id = board_response.json()["id"]

    section_data = {
        "name": "Test Section",
        "description": "A test section",
        "board_id": board_id
    }
    section_response = auth_client.post("/sections/", json=section_data)
    section_id = section_response.json()["id"]

    # Update the section
    update_data = {
        "name": "Updated Section",
        "description": "Updated description"
    }
    response = auth_client.patch(f"/sections/{section_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]

def test_delete_section(auth_client):
    """Test deleting a section."""
    # Create a board and section first
    board_data = {
        "name": "Test Board",
        "description": "A test board"
    }
    board_response = auth_client.post("/boards/", json=board_data)
    board_id = board_response.json()["id"]

    section_data = {
        "name": "Test Section",
        "description": "A test section",
        "board_id": board_id
    }
    section_response = auth_client.post("/sections/", json=section_data)
    section_id = section_response.json()["id"]

    # Delete the section
    response = auth_client.delete(f"/sections/{section_id}")
    assert response.status_code == 200
    assert "Section deleted" in response.json()["detail"]