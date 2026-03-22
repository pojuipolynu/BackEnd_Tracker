from  db.models import User, Friend, Request
from  schemas.user_schema import UserCreate, UserUpdateRequest, SignInRequest
from  repository.user_repository import UserRepository
from  repository.request_repository import RequestRepository
from  repository.friend_repository import FriendRepository
from uuid import UUID
from fastapi import HTTPException, status
from  schemas.user_schema import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt
from  db.enum_variables import InviteStatus

class UserService:
    def __init__(self, db: AsyncSession, user_repository: UserRepository):
        self.user_repository = user_repository
        self.request_repository = RequestRepository(db)
        self.friend_repository = FriendRepository(db)

    def hash_password(self, password: str):
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(pwd_bytes, salt)
        return hashed_password.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str):
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )

    async def get_users(self, offset: int = 0, limit: int = 100):
        users = await self.user_repository.get_all(offset, limit)
        return {"users": list(users)}
    
    async def get_users_by_username(self, username_key: str):
        users = await self.user_repository.get_users_username(username_key)
        return {"users": list(users)}

    async def get_user_by_id(self, user_id: UUID):
        user = await self.user_repository.get_one(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    
    async def get_user_by_email(self, user_email: str):
        user = await self.user_repository.get_user_by_email(user_email)
        return user

    async def get_user_by_username(self, user_username: str):
        user = await self.user_repository.get_user_by_username(user_username)
        return user
    
    async def checking_user(self, user: SignInRequest):
        user_check = await self.get_user_by_email(user.email)
        if user_check:
            if self.verify_password(user.password, user_check.hashed_password):
                return True
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    async def create_user(self, user_create: UserCreate):
        if user_create is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data wasn`t given")

        user_email_check = await self.get_user_by_email(user_create.email)
        user_username_check = await self.get_user_by_username(user_create.username)

        if user_email_check:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email should be unique")
        elif user_username_check:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Username should be unique")
        
        hashed_password = self.hash_password(user_create.password)
        db_user = User(username = user_create.username, email=user_create.email, hashed_password=hashed_password)
        created_user = await self.user_repository.create(db_user)
        
        return created_user
    
    async def update_user(self, user_id: UUID, user_update: UserUpdateRequest):
        user = await self.user_repository.get_one(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if user_update.username:
            user_username_check = await self.get_user_by_username(user_update.username)
            if user_username_check:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Username should be unique")
            
        if user_update.hashed_password:
            user_update.hashed_password = self.hash_password(user_update.hashed_password)

        return await self.user_repository.update(user, user_update)

    async def delete_user(self, user_id: UUID):
        user = await self.user_repository.get_one(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        await self.user_repository.delete(user)

    async def get_user_friends(self, user_id: UUID, offset: int = 0, limit: int = 100):
        users = await self.user_repository.get_user_friends(user_id, offset, limit)
        return {"users": list(users)}
    
    async def get_friends_by_username(self, user_id: UUID, username_key: str):
        users = await self.user_repository.get_user_friends_username(user_id, username_key)
        return {"users": list(users)}
    
    async def check_request(self, creator_id: UUID, user_id: UUID):
        check_request = await self.request_repository.check_request_availability(creator_id, user_id)
        if check_request is not None:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="You already sent request")
        check_friend = await self.friend_repository.check_friend_existance(creator_id, user_id)
        if check_friend is not None:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="User is already your friend")

    async def create_request(self, user_id: UUID, friend_id: UUID):
        await self.get_user_by_id(friend_id)
        await self.check_request(user_id, friend_id)
        friend_request = Request(creator_id=user_id, user_id=friend_id)
        created_request = await self.request_repository.create(friend_request)

        return created_request
    
    async def get_requests(self, user_id: UUID, offset: int = 0, limit: int = 100):
        requests = await self.request_repository.get_user_requests(user_id, offset, limit)
        return {"requests": list(requests)}

    async def get_request_by_id(self, request_id: UUID):
        request = await self.request_repository.get_one(request_id)
        if request is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
        return request
    
    async def update_request(self, user_id:UUID, request_id: UUID, request_status: InviteStatus):
        request = await self.request_repository.get_one(request_id)
        if request is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
        
        if request.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User has no rights")

        if request_status == InviteStatus.ACCEPTED:
            await self.friend_repository.create(Friend(user_1_id=request.creator_id, user_2_id=request.user_id))
            await self.request_repository.delete(request)
        else:
            await self.request_repository.update(request, request_status)

        return {"message": "Request updated"}