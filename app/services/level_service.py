from  db.models import Level
from  schemas.level_schema import LevelBase, LevelUpdateRequest
from  repository.level_repository import LevelRepository
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

class LevelService:
    def __init__(self, level_repository: LevelRepository):
        self.level_repository = level_repository

    async def get_level(self, offset: int = 0, limit: int = 100):
        levels = await self.level_repository.get_all(offset, limit)
        return {"levels": list(levels)}
  
    async def get_level_by_id(self, level_id: UUID):
        level = await self.level_repository.get_one(level_id)
        return level

    async def create_level(self, level_info: LevelBase):
        db_level = Level(name=level_info.name, points = level_info.points)
        try:
            created_level = await self.level_repository.create(db_level)
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=f"Level creation failed: {e}.")
        return created_level
    
    async def update_level(self, level_id: UUID, level_update: LevelUpdateRequest):
        level = await self.get_level_by_id(level_id)
        await self.level_repository.update(level, level_update)
        return 
    
    async def delete_level(self, level_id: UUID):
        level = await self.get_level_by_id(level_id)
        await self.level_repository.delete(level)
        return 
