from fastapi import APIRouter, Depends, status
from schemas.room_schema import Room, RoomBase, RoomUpdateRequest, Rooms
from schemas.base_schema import BaseSchema
from uuid import UUID
from services.authorization_service import AuthorizationService
from services.room_service import RoomService
from db.enum_variables import InviteStatus
from utils.depends import get_room_service
from schemas.pet_schema import PetBase, PetUpdateRequest, Pet
from schemas.progres_schema import ProgressList
from schemas.habbit_schema import HabbitBase, Habbits

router = APIRouter(prefix="/rooms")

@router.get("/", response_model=Rooms, status_code=status.HTTP_201_CREATED)
async def get_all_rooms(room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user), offset: int = 0, limit: int = 100):
    return await room_service.get_rooms(current_user.id, offset, limit)

""" 
ВАЖЛИВО, ЯКЩО РУТОМ БУДЕТЕ КОРИСТУВАТИСЬ!!!!
Повертає пендінг кімнати для корситувача, якого запросили!!! Не для творця
"""
@router.get("/pending", response_model=Rooms, status_code=status.HTTP_201_CREATED)
async def get_pending_rooms(room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user), offset: int = 0, limit: int = 100):
    return await room_service.get_pending_rooms(current_user.id, offset, limit)

@router.delete("/delete/{room_id}", response_model=BaseSchema, status_code=status.HTTP_201_CREATED)
async def delete_room(room_id:UUID, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.delete_room(room_id, current_user.id)

@router.post("/create/{user_id}", response_model=Room, status_code=status.HTTP_201_CREATED)
async def create_room(user_id:UUID, room_create: RoomBase, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.create_room(room_create, current_user.id, user_id)

@router.patch("/decline/{room_id}", response_model=BaseSchema, status_code=status.HTTP_201_CREATED)
async def decline_room(room_id: UUID, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.change_invite_status(room_id, current_user.id, InviteStatus.DECLINED)

@router.patch("/accepted/{room_id}", response_model=BaseSchema, status_code=status.HTTP_201_CREATED)
async def accept_room(pet_data: PetBase, habbits: list[HabbitBase], room_id: UUID, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.change_invite_status(room_id, current_user.id, InviteStatus.ACCEPTED, habbits, pet_data)

@router.patch("/end_room/{room_id}", response_model=BaseSchema, status_code=status.HTTP_201_CREATED)
async def change_room_status(room_id: UUID, new_room_status:bool, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.change_room_status(room_id, current_user.id, new_room_status)

@router.patch("/update_room/{room_id}", response_model=BaseSchema, status_code=status.HTTP_201_CREATED)
async def update_room(room_id: UUID, room_update: RoomUpdateRequest, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.update_room(room_id, current_user.id, room_update)


@router.post("/habbits/{habbit_id}", response_model=BaseSchema, status_code=status.HTTP_201_CREATED)
async def check_habbit(habbit_id:UUID, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.create_progress(habbit_id, current_user.id)

@router.get("/progress/by_user/{room_id}", response_model=ProgressList, status_code=status.HTTP_201_CREATED)
async def get_progress_by_user(room_id: UUID, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.get_user_progress(current_user.id, room_id)

@router.get("/progress/by_room/{room_id}", response_model=ProgressList, status_code=status.HTTP_201_CREATED)
async def get_progress_by_room(room_id: UUID, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.get_room_progress(room_id, current_user.id)

@router.get("/progress/by_habbit/{habbit_id}", response_model=ProgressList, status_code=status.HTTP_201_CREATED)
async def get_progress_by_habbit(habbit_id: UUID, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.get_habbit_progress(habbit_id)

@router.get("/pet/{room_id}", response_model=Pet, status_code=status.HTTP_201_CREATED)
async def get_pet(room_id: UUID, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.get_pet_by_room(room_id, current_user.id)

@router.patch("/pet/{pet_id}", response_model=BaseSchema, status_code=status.HTTP_201_CREATED)
async def update_pet_name(pet_id: UUID, pet_data: PetUpdateRequest, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.update_pet_name(pet_id, pet_data)


@router.get("/habbits/{room_id}", response_model=Habbits, status_code=status.HTTP_201_CREATED)
async def get_habbits(room_id: UUID, room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await room_service.get_habbits_by_room(room_id, current_user.id)

"""
РУТИ ФУНКЦІОНАЛУ ТАСОК СЕЛЕРІ ДЛЯ ПЕРЕВІРКИ РОБОТИ ФУНКЦІЙ
"""
# @router.get("/reduce_hp", status_code=status.HTTP_201_CREATED)
# async def test_reduce_hp(room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
#     return await room_service.apply_daily_pet_reduce()

# @router.get("/clean_progress", status_code=status.HTTP_201_CREATED)
# async def test_clean_progress(room_service: RoomService = Depends(get_room_service), current_user=Depends(AuthorizationService.get_current_user)):
#     return await room_service.reset_weekly_progress()
"""
РУТИ ФУНКЦІОНАЛУ ТАСОК СЕЛЕРІ ДЛЯ ПЕРЕВІРКИ РОБОТИ ФУНКЦІЙ
"""