from repository.base_repository import BaseRepository
from db.models import User, Friend, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from uuid import UUID

class UserRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db=db, model=User)

        self.friend_model=Friend

    async def get_user_by_email(self, user_value: str):
        result = await self.db.execute(select(self.model).filter(self.model.email == user_value))
        user = result.scalars().first()
        if user is None:
            return
        return user
    
    async def get_user_friends(self, user_id: UUID):
        result = await self.db.execute(select(self.model).join(self.friend_model, or_((self.friend_model.user_1_id == user_id) & (self.model.id == self.friend_model.user_2_id),(self.friend_model.user_2_id == user_id) & (self.model.id == self.friend_model.user_1_id))))
        return result.scalars().all()