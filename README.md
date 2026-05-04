# Trello  API

A FastAPI-based REST API for a Trello-style project management application.

## Features

- User registration and login
- JWT-based authentication
- Board creation and listing for authenticated users
- Board detail retrieval with sections, tickets, invited users, and invitation tokens
- Board invitation and membership handling
- Section CRUD operations for board owners
- Ticket CRUD operations with board- and user-level authorization

## Prerequisites

- Python 3.9 or higher
- Git
- Virtual environment support

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd "Trello REST API"
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a local environment file:
   ```bash
   cp .env.example .env
   ```

5. Load environment variables:
   ```bash
   source .env
   ```

6. Start the application:
   ```bash
   PYTHONPATH=src uvicorn src.app.main:app --reload --host 0.0.0.0 --port 3000
   ```

   **Note:** The application runs on HTTP by default on port 3000. Modern browsers will show a "Not Secure" warning, which is normal for development. For production, use HTTPS with a reverse proxy like Nginx.

## API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:3000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:3000/redoc

## Testing

This project includes comprehensive unit and integration tests to ensure code quality and functionality.

### Test Setup

1. Ensure you have activated the virtual environment and installed dependencies as described in the Setup section.

2. Install testing dependencies (if not already included in requirements.txt):
   ```bash
   pip install pytest httpx pytest-cov pytest-asyncio
   ```

### Running Tests

Run all tests with coverage:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

Run only unit tests:
```bash
pytest tests/unit/
```

Run only integration tests:
```bash
pytest tests/integration/
```

Generate HTML coverage report:
```bash
pytest --cov-report=html
open htmlcov/index.html
```

Check coverage percentage:
```bash
pytest --cov-report=term-missing
```

### Test Coverage Requirements

- **Unit Tests**: At least 50% of functions must be covered
- **Integration Tests**: At least 50% of endpoints must be covered
- **Overall Coverage**: Minimum 50% code coverage required

### Test Structure

- `tests/unit/`: Unit tests for individual functions and utilities
- `tests/integration/`: Integration tests for API endpoints
- `tests/conftest.py`: Shared test fixtures and configuration

### Writing Tests

When adding new features:

1. Write unit tests for utility functions in `tests/unit/`
2. Write integration tests for new endpoints in `tests/integration/`
3. Ensure all tests pass and coverage requirements are met
4. Run `pytest` before committing changes

## Environment Configuration

Create a `.env` file with the following variables:

```env
DATABASE_URL=sqlite:///./trello.db
SECRET_KEY=secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

- `DATABASE_URL`: Database connection URL
- `SECRET_KEY`: JWT signing secret
- `ALGORITHM`: JWT algorithm
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes

## API Documentation

Open the Swagger docs:

```bash
http://localhost:8000/docs
```

See detailed project documentation in:

```bash
docs/Project_Documentation.md
```

## Authentication

1. Register a new user at `POST /auth/register`
2. Log in at `POST /auth/login`
3. In Swagger UI, use the OAuth2 login form with:
   - `username`: your email
   - `password`: your password

## Endpoints

- `GET /` — Root health check
- `POST /auth/register` — Register a user
- `POST /auth/login` — Authenticate and get a JWT
- `GET /boards/` — List boards accessible to the current user
- `POST /boards/` — Create a new board
- `GET /boards/{board_id}` — Get board details
- `POST /boards/{board_id}/invite` — Invite a user to a board
- `POST /sections/` — Create a new section
- `GET /sections/{section_id}` — Get section details
- `PATCH /sections/{section_id}` — Update a section
- `DELETE /sections/{section_id}` — Delete a section
- `POST /tickets/` — Create a new ticket
- `GET /tickets/{ticket_id}` — Get ticket details
- `PATCH /tickets/{ticket_id}` — Update a ticket
- `DELETE /tickets/{ticket_id}` — Delete a ticket

## Notes

- The application automatically creates database tables on first startup.
- SQLite is enabled by default for local development.
- Do not commit `.env`, `.venv`, or `trello.db` to version control.
