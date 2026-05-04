from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    board_id = Column(Integer, ForeignKey("boards.id"))

    board = relationship("Board", back_populates="sections")
    tickets = relationship("Ticket", back_populates="section", cascade="all, delete-orphan")