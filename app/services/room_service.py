from db.models import Room, Pet, Progress
from schemas.room_schema import RoomBase, RoomUpdateRequest, RoomUpdateStatus
from schemas.pet_schema import PetBase, PetUpdateRequest, PetUpdateStatus
from schemas.habbit_schema import HabbitBase
from repository.room_repository import RoomRepository
from repository.pet_repository import PetRepository
from repository.habbit_repository import HabbitRepository
from repository.progress_repository import ProgressRepository
from repository.point_repository import PointRepository
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from db.enum_variables import InviteStatus, PointsCalculations, CreationLimits
from sqlalchemy.ext.asyncio import AsyncSession

class RoomService:
    def __init__(self, db: AsyncSession, room_repository: RoomRepository):
        self.room_repository = room_repository
        self.pet_repository = PetRepository(db)
        self.habbit_repository = HabbitRepository(db)
        self.progress_repository = ProgressRepository(db)
        self.point_repository = PointRepository(db)

    async def get_rooms(self, creator_id:UUID, offset: int = 0, limit: int = 100):
        rooms = await self.room_repository.get_user_rooms(creator_id, offset, limit)
        return {"rooms": list(rooms)}
    
    async def get_pending_rooms(self, user_id:UUID, offset: int = 0, limit: int = 100):
        rooms = await self.room_repository.get_pending_rooms(user_id, offset, limit)
        return {"rooms": list(rooms)}
    
    async def get_room_by_id(self, room_id: UUID, user_id:UUID):
        room = await self.check_room(room_id, user_id)
        return room
    
    async def room_limitation(self, user_id_1: UUID, user_id_2: UUID):
        room_count_user_1 = await self.room_repository.get_user_rooms_count(user_id_1)
        room_count_user_2 = await self.room_repository.get_user_rooms_count(user_id_2)

        if room_count_user_1 >= CreationLimits.ACTIVE_ROOM_MAX.value or room_count_user_2 >= CreationLimits.ACTIVE_ROOM_MAX.value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User can`t have more than 20 rooms")

    async def create_room(self, room_info: RoomBase, creator_id: UUID, visitor_id: UUID):
        await self.room_limitation(creator_id, visitor_id)

        db_room = Room(name=room_info.name, creator_id=creator_id, visitor_id=visitor_id)
        try:
            created_room = await self.room_repository.create(db_room)
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room creation failed.")
        return created_room
    
    async def check_room(self, room_id: UUID, user_id: UUID):
        room = await self.room_repository.get_one(room_id)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        elif room.creator_id != user_id and (room.visitor_id != user_id and room.creation_status==InviteStatus.ACCEPTED):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User has no rights")
        return room    

    # BASE SCHEMA RESPONSES
    async def update_room(self, room_id: UUID, user_id: UUID, room_update: RoomUpdateRequest):
        room = await self.check_room(room_id, user_id)
        await self.room_repository.update(room, room_update)
        return {"message": "Room updated"}
    
    async def delete_room(self, room_id: UUID, user_id: UUID):
        room = await self.check_room(room_id, user_id)
        await self.room_repository.delete(room)
        return {"message": "Room deleted"}

    async def change_invite_status(self, room_id: UUID, user_id: UUID, invite_status: InviteStatus, habbits: list[HabbitBase] = [], pet_data: PetBase = None):
        room = await self.room_repository.get_one(room_id)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        elif room.visitor_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User has no rights")
        
        await self.room_limitation(room.creator_id, user_id)

        if invite_status == InviteStatus.ACCEPTED:
            if habbits == None or pet_data is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data given")
            
            max_hp = await self.create_habbits(room_id, habbits)
            await self.create_pet(max_hp, room_id, pet_data)
        
        update_data = RoomUpdateStatus(**{"creation_status": invite_status})
        await self.room_repository.update(room, update_data)
        return {"message": "Room invite status changed"}
    
    #HABBIT|PET LOGIC
    async def create_habbits(self, room_id: UUID, habbits: list[HabbitBase]):
        if len(habbits) < CreationLimits.HABBIT_MIN.value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Should be at least one habbit.")
        elif len(habbits) > CreationLimits.HABBIT_MAX.value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Should be less than five habbits.")
        
        habbit_list = []
        max_hp = 0
        for habbit in habbits:
            points = await self.point_repository.get_one(habbit.points_id)
            if points is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong point key")
            max_hp += points.point_value
            habbit_list.append({"room_id": room_id, "name": habbit.name, "points_id": habbit.points_id})

        await self.habbit_repository.create_many(habbit_list)
        return max_hp * PointsCalculations.USER_COUNT.value * PointsCalculations.HEADSTART_POINTS_COEF.value

    async def check_habbit(self, habbit_id: UUID):
        habbit = await self.habbit_repository.get_one(habbit_id)
        if habbit is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habbit not found")
        return habbit   
    
    async def get_habbits_by_room(self, room_id: UUID, user_id: UUID):
        await self.check_room(room_id, user_id)
        habbits = await self.habbit_repository.get_habbits_by_room(room_id)
        return {"habbits": list(habbits)}

    async def create_pet(self, max_hp: int, room_id: UUID, pet_data: PetBase):
        db_pet = Pet(name = pet_data.name, room_id = room_id, max_hp=max_hp, current_hp=max_hp)
        try:
            created_pet = await self.pet_repository.create(db_pet)
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pet creation failed.")
        return created_pet
    
    async def check_pet(self, pet_id: UUID):
        pet = await self.pet_repository.get_one(pet_id)
        if pet is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
        return pet    

    async def update_pet_name(self, pet_id: UUID, pet_name: PetUpdateRequest):
        pet = await self.check_pet(pet_id)
        await self.pet_repository.update(pet, pet_name)
        return {"message": "Pet name updated"}

    async def update_pet_points(self, pet, points: int):
        await self.pet_repository.update(pet, PetUpdateStatus(**{"current_hp": points}))
        if points <= 0:
            await self.kill_pet(pet)
        return {"message": "Pet points updated"}
    
    async def kill_pet(self, pet):
        await self.pet_repository.update(pet, PetUpdateStatus(**{"current_hp": 0, "is_dead": True}))

        room = await self.room_repository.get_one(pet.room_id)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        await self.room_repository.update(room, RoomUpdateStatus(**{"room_status": False}))
        return {"message": "Pet killed. Room closed"}

    async def get_pet_by_room(self, room_id: UUID, user_id: UUID):
        await self.check_room(room_id, user_id)
        pet = await self.pet_repository.get_pet_by_room(room_id)
        return pet

    async def create_progress(self, habbit_id: UUID, user_id: UUID):
        db_progress = Progress(habbit_id=habbit_id, user_id=user_id)
        try:
            habbit = await self.check_habbit(habbit_id)
            pet = await self.pet_repository.get_pet_by_room(habbit.room_id)
            added_points = await self.progress_repository.get_point_value(habbit_id)
            if added_points is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Points adding went wrong.")
            await self.progress_repository.create(db_progress)
            await self.update_pet_points(pet, pet.current_hp + added_points)
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Progress creation failed.")
        return {"message": "Habbit checked"}
    
    async def get_room_progress(self, room_id: UUID, user_id: UUID):
        await self.check_room(room_id, user_id)
        progresses = await self.progress_repository.get_progress_by_room(room_id)
        return {"progresses": list(progresses)}

    async def get_habbit_progress(self, habbit_id: UUID):
        await self.check_habbit(habbit_id)
        progresses =  await self.progress_repository.get_progress_by_habbit(habbit_id)
        return {"progresses": list(progresses)}
    
    async def get_user_progress(self, user_id: UUID, room_id: UUID):
        await self.check_room(room_id, user_id)
        progresses =  await self.progress_repository.get_progress_by_user(room_id, user_id)
        return {"progresses": list(progresses)}

    #HABBIT|PET LOGIC

    #POINTS LOGIC
    async def apply_daily_pet_reduce(self):
        active_pets = await self.pet_repository.get_active_pets()
        update_list = []

        for pet in active_pets:
            total_points = await self.habbit_repository.get_reduce_room_points(pet.room_id)
            reduce = total_points * PointsCalculations.USER_COUNT.value
            new_hp = pet.current_hp - reduce
            
            if new_hp <= 0:
                await self.kill_pet(pet)
            else:
                update_list.append({"id": pet.id, "current_hp": new_hp})

        if update_list:
            await self.pet_repository.update_all_hp(update_list)
        
        return {"message": "Pets hp updated"}

    async def reset_weekly_progress(self):
        await self.progress_repository.clear_all_progress()
        return {"message": "Progress cleared"}
    #POINTS LOGIC
        
    async def change_room_status(self, room_id: UUID, user_id: UUID, new_status: bool):
        room = await self.check_room(room_id, user_id)
        update_data = RoomUpdateStatus(**{"room_status": new_status})
        await self.room_repository.update(room, update_data)
        return {"message": "Room status changed"}
    # BASE SCHEMA RESPONSES