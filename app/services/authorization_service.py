from schemas.user_schema import SignInRequest, UserCreate
from utils.basic_token_handler import user_token
from repository.user_repository import UserRepository
from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import postgres_db
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from schemas.user_schema import UserCreate
from db.models import User
from sqlalchemy import select
from services.user_service import UserService

security = HTTPBearer()

class AuthorizationService(UserService):
    def __init__(self, db:AsyncSession, user_repository: UserRepository):
        super().__init__(db, user_repository)

    async def sign_up(self, user_create: UserCreate):
        user = await self.create_user(user_create=user_create)
        token = user_token.sign_token(user.email)
        if not token:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate token")
        return {"access_token": token}

    async def login(self, user_login: SignInRequest):
        await self.checking_user(user_login)
        token = user_token.sign_token(user_login.email)
        if not token:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate token")
        return {"access_token": token}

    @staticmethod
    async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security), session: AsyncSession = Depends(postgres_db)):
        decoded_token = user_token.decode_token(token.credentials)
        user_check = await session.execute(select(User).filter(User.email==decoded_token.get('email')))
        user_check = user_check.scalars().first()
        if user_check:
            return user_check
        