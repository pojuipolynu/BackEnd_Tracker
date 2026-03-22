from pydantic import BaseModel
from uuid import UUID

class HabbitBase(BaseModel):
    name: str
    points_id: UUID

class Habbit(HabbitBase):
    id: UUID
    room_id: UUID
    class Config:
        orm_mode = True
        from_attributes = True

class Habbits(BaseModel):
    habbits: list[Habbit]

