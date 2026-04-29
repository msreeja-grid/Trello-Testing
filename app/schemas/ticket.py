from typing import Optional
from pydantic import BaseModel

class TicketCreate(BaseModel):
    name: str
    description: str
    section_id: int
    assigned_to: int

class TicketUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    section_id: Optional[int] = None
    assigned_to: Optional[int] = None

class TicketOut(BaseModel):
    id: int
    name: str
    description: str
    section_id: int
    assigned_to: int
    created_by: int

    class Config:
        from_attributes = True
