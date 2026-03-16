from pydantic import BaseModel
from uuid import UUID
from  db.enum_variables import InviteStatus

class FriendBase(BaseModel):
    user_1_id: UUID
    user_2_id: UUID

class Friend(FriendBase):
    id: UUID
    class Config:
        orm_mode = True
        from_attributes = True

