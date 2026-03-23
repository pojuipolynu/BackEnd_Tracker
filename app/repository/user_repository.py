from repository.base_repository import BaseRepository
from db.models import User, Friend
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
    
    async def get_user_by_username(self, user_value: str):
        result = await self.db.execute(select(self.model).filter(self.model.username == user_value))
        user = result.scalars().first()
        if user is None:
            return
        return user
    
    async def get_user_friends(self, user_id: UUID, offset: int, limit: int):
        query = (
            select(self.model)
            .join(
                self.friend_model, 
                or_(
                    (self.friend_model.user_1_id == user_id) & (self.model.id == self.friend_model.user_2_id),
                    (self.friend_model.user_2_id == user_id) & (self.model.id == self.friend_model.user_1_id)
                )
            )
        )
        if limit == 0:
            result = await self.db.execute(query.offset(offset))
        else:
            result = await self.db.execute(query.offset(offset).limit(limit))
        return result.scalars().all()
    
    async def get_user_friends_username(self, user_id: UUID, username_key: str):
        query = (
            select(self.model)
            .join(
                self.friend_model,
                or_(
                    (self.friend_model.user_1_id == user_id) & (self.model.id == self.friend_model.user_2_id),
                    (self.friend_model.user_2_id == user_id) & (self.model.id == self.friend_model.user_1_id)
                )
            )
            .where(self.model.username.ilike(f"%{username_key}%"))
        )

        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_users_username(self, username_key: str):
        result = await self.db.execute(select(self.model).where(self.model.username.ilike(f"%{username_key}%")))
        return result.scalars().all()
    
    async def get_search_users(self, user_id: UUID, offset: int, limit: int):
        if limit == 0:
            result = await self.db.execute(select(self.model).filter(self.model.id != user_id).offset(offset))
        else:
            result = await self.db.execute(select(self.model).filter(self.model.id != user_id).offset(offset).limit(limit))
        variables = result.scalars().all()
        return variables