from pydantic import BaseModel
from uuid import UUID

class PetBase(BaseModel):
    name: str

class Pet(PetBase):
    id: UUID
    room_id: UUID
    is_dead: bool
    max_hp: int
    current_hp: int
    class Config:
        orm_mode = True
        from_attributes = True

class PetUpdateRequest(BaseModel):
    name: str | None = None

class PetUpdateStatus(BaseModel):
    current_hp: int| None = None
    is_dead: bool| None = None

