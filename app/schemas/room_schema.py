from pydantic import BaseModel
from uuid import UUID
from  db.enum_variables import InviteStatus

class RoomBase(BaseModel):
    name: str
    description: str
    level_id: UUID

class Room(RoomBase):
    id: UUID
    creator_id: UUID
    visitor_id: UUID
    class Config:
        orm_mode = True
        from_attributes = True

class RoomUpdateRequest(BaseModel):
    description: str | None = None
    name: str | None = None

class RoomUpdateStatus(BaseModel):
    room_status: bool| None = None
    creation_status: InviteStatus| None = None

class Rooms(BaseModel):
    rooms: list[Room]

