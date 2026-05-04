from typing import Optional
from pydantic import BaseModel, ConfigDict

class TicketCreate(BaseModel):
    name: str
    description: str
    section_id: int
    assigned_to: Optional[int] = None

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
    assigned_to: Optional[int]
    created_by: int

    model_config = ConfigDict(from_attributes=True)
