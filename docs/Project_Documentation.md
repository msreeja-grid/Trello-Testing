# Trello REST API Documentation

## Overview

This project is a FastAPI-based REST API that provides Trello-style board management features. It supports user registration and authentication, boards, sections, tickets, and board invitations.

## Project Structure

- `app/main.py` - Application entry point, FastAPI app setup, route registration
- `app/db/` - Database setup and session handling
- `app/models/` - SQLAlchemy ORM models for users, boards, sections, tickets, and invitations
- `app/schemas/` - Pydantic request/response schemas
- `app/api/routes/` - FastAPI route modules for authentication, boards, sections, and tickets
- `app/core/` - Authentication and security utility functions
- `app/utils/` - JWT creation and validation utilities

## Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` file or copy from `.env.example`:
   ```bash
   cp .env.example .env
   ```
4. Start the app:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Environment Variables

- `DATABASE_URL` - Database connection URL, default `sqlite:///./trello.db`
- `SECRET_KEY` - JWT signing secret
- `ALGORITHM` - JWT signing algorithm (default `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - JWT expiration time

## Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Log in using OAuth2 password flow and receive a bearer token

### Authentication Flow

1. Register a user with email, password, first name, and last name.
2. Log in with email and password to receive a JWT access token.
3. Use the token to authorize protected routes in Swagger UI or API clients.

## API Endpoints

### Boards

- `GET /boards/` - List boards available to the current user
- `POST /boards/` - Create a new board
- `GET /boards/{board_id}` - Retrieve board details
- `POST /boards/{board_id}/invite` - Invite an existing user to a board

### Sections

- `POST /sections/` - Create a new section in a board
- `GET /sections/{section_id}` - Get section details
- `PATCH /sections/{section_id}` - Update a section
- `DELETE /sections/{section_id}` - Delete a section

### Tickets

- `POST /tickets/` - Create a new ticket
- `GET /tickets/{ticket_id}` - Get ticket details
- `PATCH /tickets/{ticket_id}` - Update a ticket
- `DELETE /tickets/{ticket_id}` - Delete a ticket

## Notes

- The app automatically creates database tables on startup.
- `board_id`, `section_id`, and `ticket_id` values are created from POST responses and used for later requests.
- `assigned_to` should reference an existing user ID.

## API Docs

When the app is running, explore the interactive documentation at:

```text
http://localhost:8000/docs
```
