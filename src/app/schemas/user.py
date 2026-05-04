from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

class UserOut(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)