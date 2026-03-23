from db.models import Point
from repository.point_repository import PointRepository
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from core.config import settings

class PointService:
    def __init__(self, point_repository: PointRepository):
        self.point_repository = point_repository

    async def get_point(self):
        points = await self.point_repository.get_all()
        return {"points": list(points)}
  
    async def get_point_by_id(self, point_id: UUID):
        point = await self.point_repository.get_one(point_id)
        return point

    async def create_point(self, dev_password: str, point_value: int):
        if dev_password != settings.DEV_PASSWORD:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User has no rights")
        db_point = Point(point_value=point_value)
        try:
            created_point = await self.point_repository.create(db_point)
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Point creation failed: {e}.")
        return created_point
    