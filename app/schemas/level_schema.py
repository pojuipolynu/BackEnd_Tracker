from pydantic import BaseModel
from uuid import UUID

class LevelBase(BaseModel):
    name: str
    points: int

class Level(LevelBase):
    id: UUID
    class Config:
        orm_mode = True
        from_attributes = True

class LevelUpdateRequest(BaseModel):
    name: str | None = None
    points: int| None = None

class Levels(BaseModel):
    levels: list[Level]

