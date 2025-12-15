from pydantic import BaseModel
from uuid import UUID

class UserCreate(BaseModel):
    username: str
    email: str
    description: str

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    description: str

    class Config:
        orm_mode = True