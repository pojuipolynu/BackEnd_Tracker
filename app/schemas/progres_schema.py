from pydantic import BaseModel
from uuid import UUID
from datetime import datetime 

class Progress(BaseModel):
    id: UUID
    user_id: UUID
    habbit_id: UUID
    created_at: datetime 
    
    class Config:
        orm_mode = True
        from_attributes = True


class ProgressList(BaseModel):
    progresses: list[Progress]

