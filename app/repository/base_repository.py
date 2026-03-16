from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

class BaseRepository:
    def __init__(self, db: AsyncSession, model):
        self.db = db
        self.model = model
    
    async def get_all(self, offset: int = 0, limit: int = 0):
        if limit == 0:
            result = await self.db.execute(select(self.model).offset(offset))
        else:
            result = await self.db.execute(select(self.model).offset(offset).limit(limit))
        variables = result.scalars().all()
        return variables

    async def get_one(self, user_id: UUID):
        result = await self.db.execute(select(self.model).filter(self.model.id == user_id))
        variable = result.scalars().first()
        if variable is None:
            return
        return variable

    async def create(self, variable):
        self.db.add(variable)
        await self.db.commit()
        await self.db.refresh(variable)
        return variable

    async def delete(self, variable):
        await self.db.delete(variable)
        await self.db.commit()

    async def update(self, variable, updated_variable):
        for field, value in updated_variable.model_dump(exclude_unset=True).items():
            setattr(variable, field, value)
        await self.db.commit()
        await self.db.refresh(variable)

        return variable
            

    async def count_all(self):
        result = await self.db.execute( select(func.count()) .select_from(self.model))
        count = result.scalar()
        return count