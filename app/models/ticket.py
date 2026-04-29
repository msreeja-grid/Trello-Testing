from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    section_id = Column(Integer, ForeignKey("sections.id"))
    assigned_to = Column(Integer, ForeignKey("users.id"))
    created_by = Column(Integer)

    section = relationship("Section", back_populates="tickets")
    assignee = relationship("User")
