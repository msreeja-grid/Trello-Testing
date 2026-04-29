from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="owned_boards")
    sections = relationship("Section", back_populates="board", cascade="all, delete-orphan")
    invitations = relationship("Invitation", back_populates="board", cascade="all, delete-orphan")