from repository.base_repository import BaseRepository
from db.models import Habbit, Point
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, func
from uuid import UUID

class HabbitRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, model=Habbit)
        self.point_model = Point

    async def create_many(self, habbits_data):
        query = insert(self.model).values(habbits_data)
        await self.db.execute(query)
        await self.db.commit()

    async def get_reduce_room_points(self, room_id: UUID) -> int:
        query = (
            select(func.sum(self.point_model.point_value))
            .join(self.model, self.model.points_id == self.point_model.id)
            .where(self.model.room_id == room_id)
        )
        result = await self.db.execute(query)
        return result.scalar() or 0
    
    async def get_habbits_by_room(self, room_id: UUID):
        result = await self.db.execute(select(self.model).filter(self.model.room_id==room_id))
        variables = result.scalars().all()
        return variables