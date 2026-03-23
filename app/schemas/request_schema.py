from pydantic import BaseModel
from uuid import UUID
from db.enum_variables import InviteStatus

class RequestBase(BaseModel):
    creator_id: UUID
    user_id: UUID

class Request(RequestBase):
    id: UUID
    status: InviteStatus
    class Config:
        orm_mode = True
        from_attributes = True

class RequestUpdateRequest(BaseModel):
    status: InviteStatus
    
class Requests(BaseModel):
    requests: list[Request]