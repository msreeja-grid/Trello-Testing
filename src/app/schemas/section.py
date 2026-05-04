from typing import Optional
from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)
