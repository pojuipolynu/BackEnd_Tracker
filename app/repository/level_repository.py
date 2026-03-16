from repository.base_repository import BaseRepository
from db.models import Level
from sqlalchemy.ext.asyncio import AsyncSession

class LevelRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, model=Level)

    