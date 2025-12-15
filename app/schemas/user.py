from uuid import UUID

from pydantic import BaseModel


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
