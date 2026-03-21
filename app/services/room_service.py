from  db.models import Room
from  schemas.room_schema import RoomBase, RoomUpdateRequest, RoomUpdateStatus
from  repository.room_repository import RoomRepository
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from  db.enum_variables import InviteStatus

class RoomService:
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

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

        print("NUMBERS: " + str(room_count_user_1) + str(room_count_user_2))

        if room_count_user_1 >= 20 or room_count_user_2 >= 20:
            raise HTTPException(status_code=400, detail="User can`t have more than 20 rooms")

    async def create_room(self, room_info: RoomBase, creator_id: UUID, visitor_id: UUID):
        await self.room_limitation(creator_id, visitor_id)

        db_room = Room(name=room_info.name, creator_id=creator_id, visitor_id=visitor_id)
        try:
            created_room = await self.room_repository.create(db_room)
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail="Room creation failed.")
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

    async def change_invite_status(self, room_id: UUID, user_id: UUID, invite_status: InviteStatus):
        room = await self.room_repository.get_one(room_id)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        elif room.visitor_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User has no rights")
        
        await self.room_limitation(room.creator_id, user_id)

        update_data = RoomUpdateStatus(**{"creation_status": invite_status})
        await self.room_repository.update(room, update_data)
        return {"message": "Room invite status changed"}
        
    async def change_room_status(self, room_id: UUID, user_id: UUID, new_status: bool):
        room = await self.check_room(room_id, user_id)
        update_data = RoomUpdateStatus(**{"room_status": new_status})
        await self.room_repository.update(room, update_data)
        return {"message": "Room status changed"}
    # BASE SCHEMA RESPONSES