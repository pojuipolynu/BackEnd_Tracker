from repository.base_repository import BaseRepository
from db.models import Friend
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from uuid import UUID

class FriendRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, model=Friend)

    async def check_friend_existance(self, user_1_id: UUID, user_2_id: UUID):
        result = await self.db.execute(
            select(self.model).filter(
                or_(
                    and_(self.model.user_1_id == user_1_id, self.model.user_2_id == user_2_id),
                    and_(self.model.user_1_id == user_2_id, self.model.user_2_id == user_1_id)
                )
            )
        )
        variable = result.scalars().first()
        if variable is None:
            return
        return variable