from sqlalchemy.orm import declarative_base # pyright: ignore[reportMissingImports]

Base = declarative_base()

# Import models so they are registered with SQLAlchemy metadata
from app.models import board, invitation, section, ticket, user  # noqa: F401