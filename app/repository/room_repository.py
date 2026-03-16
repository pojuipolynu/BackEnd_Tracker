from repository.base_repository import BaseRepository
from db.models import Room
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from uuid import UUID
from db.enum_variables import InviteStatus

class RoomRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, model=Room)

    async def get_pending_rooms(self, user_id: UUID, offset: int, limit: int):
        if limit == 0:
            result = await self.db.execute(select(self.model).filter(self.model.visitor_id==user_id, self.model.creation_status==InviteStatus.PENDING).offset(offset))
        else:
            result = await self.db.execute(select(self.model).filter(self.model.visitor_id==user_id, self.model.creation_status==InviteStatus.PENDING).offset(offset).limit(limit))
        variables = result.scalars().all()
        return variables
    
    async def get_user_rooms(self, user_id: UUID, offset: int, limit: int):
        if limit == 0:
            result = await self.db.execute(select(self.model).filter(or_(self.model.visitor_id==user_id, self.model.creator_id==user_id)).offset(offset))
        else:
            result = await self.db.execute(select(self.model).filter(or_(self.model.visitor_id==user_id, self.model.creator_id==user_id)).offset(offset).limit(limit))
        variables = result.scalars().all()
        return variables