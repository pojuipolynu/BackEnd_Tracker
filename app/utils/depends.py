from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import postgres_db
from services.authorization_service import AuthorizationService
from services.user_service import UserService
from services.room_service import RoomService
from services.point_service import PointService
from repository.user_repository import UserRepository
from repository.room_repository import RoomRepository
from repository.point_repository import PointRepository
from typing import Annotated

def get_user_service(db: Annotated[AsyncSession, Depends(postgres_db)]):
    user_repository = UserRepository(db)
    return UserService(db=db, user_repository=user_repository)

def get_authorization_service(db: Annotated[AsyncSession, Depends(postgres_db)]):
    user_repository = UserRepository(db)
    return AuthorizationService(db=db, user_repository=user_repository)

def get_room_service(db: Annotated[AsyncSession, Depends(postgres_db)]):
    room_repository = RoomRepository(db)
    return RoomService(db=db, room_repository=room_repository)

def get_point_service(db: Annotated[AsyncSession, Depends(postgres_db)]):
    poiny_repository = PointRepository(db)
    return PointService(poiny_repository)
