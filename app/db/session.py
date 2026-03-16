from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

engine = create_async_engine(settings.POSTGRES_URL, echo=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def postgres_db():
    async with async_session() as db:
        yield db
        