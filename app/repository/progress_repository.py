from repository.base_repository import BaseRepository
from db.models import Progress, Point, Habbit, Room
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, delete
from uuid import UUID

class ProgressRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, model=Progress)
        self.habbit_model = Habbit
        self.point_model = Point
        self.room_model = Room

    async def get_point_value(self, habbit_id: UUID) -> int:
        result = await self.db.execute(select(self.point_model.point_value).join(self.habbit_model, self.habbit_model.points_id == self.point_model.id).where(self.habbit_model.id == habbit_id))
        return result.scalar_one_or_none()
    
    async def get_progress_by_room(self, room_id: UUID):
        result = await self.db.execute(select(self.model).join(self.habbit_model, self.model.habbit_id == self.habbit_model.id).where(self.habbit_model.room_id == room_id))
        return result.scalars().all()
    
    async def get_progress_by_habbit(self, habbit_id: UUID):
        result = await self.db.execute(select(self.model).filter(self.model.habbit_id==habbit_id))
        return result.scalars().all()
    
    async def get_progress_by_user(self, room_id: UUID, user_id: UUID):
        query = (
            select(self.model).join(self.habbit_model, self.model.habbit_id == self.habbit_model.id)
            .where(
                and_(
                    self.habbit_model.room_id == room_id,
                    self.model.user_id == user_id
                )
            )
        )
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def clear_all_progress(self):
        await self.db.execute(delete(self.model))
        await self.db.commit()