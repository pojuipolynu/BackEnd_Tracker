from pydantic import BaseModel
from uuid import UUID

class FriendBase(BaseModel):
    user_1_id: UUID
    user_2_id: UUID

class Friend(FriendBase):
    id: UUID
    class Config:
        orm_mode = True
        from_attributes = True

