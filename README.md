# Trello REST API

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
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

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
