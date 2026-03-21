from fastapi import APIRouter, Depends, status
from schemas.user_schema import UserCreate, SignInRequest, Token, Users, User, UserUpdateRequest
from schemas.request_schema import Requests, Request
from schemas.base_schema import BaseSchema
from uuid import UUID
from services.authorization_service import AuthorizationService
from db.enum_variables import InviteStatus
from utils.depends import get_authorization_service

router = APIRouter(prefix="/users")

@router.post("/login", response_model=Token, status_code=status.HTTP_201_CREATED)
async def login_user(user_login: SignInRequest, user_service: AuthorizationService = Depends(get_authorization_service)):
    return await user_service.login(user_login)

@router.post("/sign_up", response_model=Token, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, user_service: AuthorizationService = Depends(get_authorization_service)):
    return await user_service.sign_up(user_create)

@router.get("/user/me", response_model=User, status_code=status.HTTP_200_OK)
async def read_user_me(current_user=Depends(AuthorizationService.get_current_user)):
    return current_user

@router.patch("/user/me/update", response_model=User, status_code=status.HTTP_200_OK)
async def update_user_me(user_update: UserUpdateRequest, current_user=Depends(AuthorizationService.get_current_user), user_service: AuthorizationService = Depends(get_authorization_service)):
    return await user_service.update_user(current_user.id, user_update)

@router.delete("/user/me/delete", status_code=status.HTTP_200_OK)
async def delete_user_me(user_service: AuthorizationService = Depends(get_authorization_service), current_user=Depends(AuthorizationService.get_current_user)):
    await user_service.delete_user(current_user.id)
    return {"message": "User deleted successfully"}

@router.get("/user/me/friends", response_model=Users, status_code=status.HTTP_200_OK)
async def get_user_friends(user_service: AuthorizationService = Depends(get_authorization_service), current_user=Depends(AuthorizationService.get_current_user), offset: int = 0, limit: int = 100):
    return await user_service.get_user_friends(current_user.id, offset, limit)

@router.get("/user/me/friends/{user_username}", response_model=Users, status_code=status.HTTP_200_OK)
async def get_friends_by_username(user_username:str, user_service: AuthorizationService = Depends(get_authorization_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await user_service.get_friends_by_username(current_user.id, user_username)

@router.get("/user/me/check_person/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: UUID, user_service: AuthorizationService = Depends(get_authorization_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await user_service.get_user_by_id(user_id)

@router.get("/user/me/check_all_people", response_model=Users, status_code=status.HTTP_200_OK)
async def get_all_users(user_service: AuthorizationService = Depends(get_authorization_service), current_user=Depends(AuthorizationService.get_current_user), offset: int = 0, limit: int = 100):
    return await user_service.get_users(offset, limit)

@router.get("/user/me/check_all_people/{user_username}", response_model=Users, status_code=status.HTTP_200_OK)
async def get_users_by_username(user_username: str, user_service: AuthorizationService = Depends(get_authorization_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await user_service.get_users_by_username(user_username)

@router.get("/user/me/requests", response_model=Requests, status_code=status.HTTP_200_OK)
async def get_user_requests(user_service: AuthorizationService = Depends(get_authorization_service), current_user=Depends(AuthorizationService.get_current_user), offset: int = 0, limit: int = 100):
    return await user_service.get_requests(current_user.id, offset, limit)

@router.post("/user/me/send_request/{user_id}", response_model=Request, status_code=status.HTTP_201_CREATED)
async def send_request(user_id: UUID, user_service: AuthorizationService = Depends(get_authorization_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await user_service.create_request(current_user.id, user_id)

@router.patch("/user/me/accept_request/{request_id}", response_model=BaseSchema, status_code=status.HTTP_201_CREATED)
async def accept_request(request_id: UUID, user_service: AuthorizationService = Depends(get_authorization_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await user_service.update_request(current_user.id, request_id, InviteStatus.ACCEPTED)

@router.patch("/user/me/decline_request/{request_id}", response_model=BaseSchema, status_code=status.HTTP_201_CREATED)
async def decline_request(request_id: UUID, user_service: AuthorizationService = Depends(get_authorization_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await user_service.update_request(current_user.id, request_id, InviteStatus.DECLINED)