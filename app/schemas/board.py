from typing import List
from pydantic import BaseModel
from app.schemas.section import SectionOut
from app.schemas.ticket import TicketOut
from app.schemas.user import UserOut

class BoardCreate(BaseModel):
    name: str
    description: str

class InvitationCreate(BaseModel):
    email: str

class BoardOut(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True

class BoardDetail(BoardOut):
    owner_id: int
    sections: List[SectionOut]
    tickets: List[TicketOut]
    users: List[UserOut]
    invitations: List[str]

    class Config:
        from_attributes = True