from typing import Optional
from pydantic import BaseModel

class SectionCreate(BaseModel):
    name: str
    description: str
    board_id: int

class SectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class SectionOut(BaseModel):
    id: int
    name: str
    description: str
    board_id: int

    class Config:
        from_attributes = True
