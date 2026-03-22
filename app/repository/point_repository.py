from repository.base_repository import BaseRepository
from db.models import Point
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from uuid import UUID

class PointRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, model=Point)