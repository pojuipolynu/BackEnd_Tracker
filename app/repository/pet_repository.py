from repository.base_repository import BaseRepository
from db.models import Pet, Room
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, update
from uuid import UUID
from  db.enum_variables import InviteStatus

class PetRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, model=Pet)
        self.room_model = Room

    async def get_pet_by_room(self, room_id: UUID):
        result = await self.db.execute(select(self.model).where(self.model.room_id == room_id))
        return result.scalar_one_or_none()
    
    async def get_active_pets(self):
        query = (
            select(self.model)
            .join(self.room_model, self.model.room_id == self.room_model.id)
            .where(
                self.room_model.room_status == True,
                self.room_model.creation_status == InviteStatus.ACCEPTED,
                self.model.is_dead == False
            )
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_all_hp(self, update_data: list[dict]):
        await self.db.execute(update(self.model), update_data)
        await self.db.commit()