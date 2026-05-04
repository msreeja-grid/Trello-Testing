import pytest

def test_create_ticket(auth_client):
    """Test creating a ticket."""
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

    # Create a ticket
    ticket_data = {
        "name": "Test Ticket",
        "description": "A test ticket",
        "section_id": section_id,
        "assigned_to": None
    }
    response = auth_client.post("/tickets/", json=ticket_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == ticket_data["name"]
    assert data["section_id"] == section_id

def test_get_ticket(auth_client):
    """Test getting a ticket."""
    # Create board, section, and ticket first
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

    ticket_data = {
        "name": "Test Ticket",
        "description": "A test ticket",
        "section_id": section_id,
        "assigned_to": None
    }
    ticket_response = auth_client.post("/tickets/", json=ticket_data)
    ticket_id = ticket_response.json()["id"]

    # Get the ticket
    response = auth_client.get(f"/tickets/{ticket_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == ticket_data["name"]

def test_update_ticket(auth_client):
    """Test updating a ticket."""
    # Create board, section, and ticket first
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

    ticket_data = {
        "name": "Test Ticket",
        "description": "A test ticket",
        "section_id": section_id,
        "assigned_to": None
    }
    ticket_response = auth_client.post("/tickets/", json=ticket_data)
    ticket_id = ticket_response.json()["id"]

    # Update the ticket
    update_data = {
        "name": "Updated Ticket",
        "description": "Updated description"
    }
    response = auth_client.patch(f"/tickets/{ticket_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]

def test_delete_ticket(auth_client):
    """Test deleting a ticket."""
    # Create board, section, and ticket first
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

    ticket_data = {
        "name": "Test Ticket",
        "description": "A test ticket",
        "section_id": section_id,
        "assigned_to": None
    }
    ticket_response = auth_client.post("/tickets/", json=ticket_data)
    ticket_id = ticket_response.json()["id"]

    # Delete the ticket
    response = auth_client.delete(f"/tickets/{ticket_id}")
    assert response.status_code == 200
    assert "Ticket deleted" in response.json()["detail"]