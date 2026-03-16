from fastapi import APIRouter, Depends, status
from schemas.room_schema import Room, RoomBase, RoomUpdateRequest, Rooms
from uuid import UUID
from services.authorization_service import AuthorizationService
from services.room_service import RoomService
from services.level_service import LevelService
from  db.enum_variables import InviteStatus
from utils.depends import get_room_service, get_level_service

router = APIRouter(prefix="/rooms")

@router.get("/", response_model=Rooms, status_code=status.HTTP_201_CREATED)
async def get_all_rooms(room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user), offset: int = 0, limit: int = 100):
    return await room_service.get_rooms(current_user.id, offset, limit)

@router.get("/pending", response_model=Rooms, status_code=status.HTTP_201_CREATED)
async def get_pending_rooms(room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user), offset: int = 0, limit: int = 100):
    return await room_service.get_pending_rooms(current_user.id, offset, limit)

@router.delete("/delete/{room_id}", status_code=status.HTTP_201_CREATED)
async def delete_room(room_id:UUID, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.delete_room(room_id, current_user.id)

@router.post("/create/{user_id}", response_model=Room, status_code=status.HTTP_201_CREATED)
async def create_room(user_id:UUID, room_create: RoomBase, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.create_room(room_create, current_user.id, user_id)

@router.patch("/decline/{room_id}", status_code=status.HTTP_201_CREATED)
async def decline_room(room_id: UUID, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.change_invite_status(room_id, current_user.id, InviteStatus.DECLINED)

@router.patch("/accepted/{room_id}", status_code=status.HTTP_201_CREATED)
async def accept_room(room_id: UUID, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.change_invite_status(room_id, current_user.id, InviteStatus.ACCEPTED)

@router.patch("/end_room/{room_id}", status_code=status.HTTP_201_CREATED)
async def change_room_status(room_id: UUID, new_room_status:bool, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.change_room_status(room_id, current_user.id, new_room_status)

@router.patch("/update_room/{room_id}", status_code=status.HTTP_201_CREATED)
async def update_room(room_id: UUID, room_update: RoomUpdateRequest, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.update_room(room_id, current_user.id, room_update)