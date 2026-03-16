from fastapi import APIRouter, Depends, status
from schemas.level_schema import Level, LevelBase, Levels, LevelUpdateRequest
from uuid import UUID
from services.authorization_service import AuthorizationService
from services.level_service import LevelService
from utils.depends import get_level_service

router = APIRouter(prefix="/levels")

@router.get("/", response_model=Levels, status_code=status.HTTP_201_CREATED)
async def get_all_levels(level_service: LevelService = Depends(get_level_service), current_user=Depends(AuthorizationService.get_current_user), offset: int = 0, limit: int = 100):
    return await level_service.get_level(offset, limit)

@router.post("/create", response_model=Level, status_code=status.HTTP_201_CREATED)
async def create_level(level_create: LevelBase, level_service: LevelService = Depends(get_level_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await level_service.create_level(level_create)

@router.delete("/delete/{level_id}", status_code=status.HTTP_201_CREATED)
async def delete_level(level_id:UUID, level_service: LevelService = Depends(get_level_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await level_service.delete_level(level_id)

@router.patch("/update_level/{level_id}", status_code=status.HTTP_201_CREATED)
async def update_level(level_id: UUID, level_update: LevelUpdateRequest, level_service: LevelService = Depends(get_level_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await level_service.update_level(level_id, level_update)