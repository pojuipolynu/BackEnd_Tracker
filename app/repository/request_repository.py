from repository.base_repository import BaseRepository
from db.models import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from uuid import UUID
from db.enum_variables import InviteStatus

class RequestRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, model=Request)

    async def check_request_availability(self, creator_id: UUID, user_id: UUID):
        result = await self.db.execute(select(self.model).filter(self.model.creator_id == creator_id, self.model.user_id == user_id, self.model.status==InviteStatus.PENDING))
        variable = result.scalars().first()
        if variable is None:
            return
        return variable
    
    async def get_user_requests(self, user_id: UUID, offset: int, limit: int):
        if limit == 0:
            result = await self.db.execute(select(self.model).filter(or_(self.model.creator_id == user_id, self.model.user_id == user_id)).offset(offset))
        else:
            result = await self.db.execute(select(self.model).filter(or_(self.model.creator_id == user_id, self.model.user_id == user_id)).offset(offset).limit(limit))
        variables = result.scalars().all()
        return variables