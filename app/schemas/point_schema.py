from pydantic import BaseModel
from uuid import UUID

class Point(BaseModel):
    id: UUID
    point_value: int 
    class Config:
        orm_mode = True
        from_attributes = True

class Points(BaseModel):
    points: list[Point]

