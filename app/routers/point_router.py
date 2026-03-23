from fastapi import APIRouter, Depends, status
from schemas.point_schema import Point, Points
from uuid import UUID
from services.authorization_service import AuthorizationService
from services.point_service import PointService
from utils.depends import get_point_service

router = APIRouter(prefix="/points")

@router.get("/", response_model=Points, status_code=status.HTTP_201_CREATED)
async def get_all_points(point_service: PointService = Depends(get_point_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await point_service.get_point()

@router.get("/point/{point_id}", response_model=Point, status_code=status.HTTP_201_CREATED)
async def get_point_by_id(point_id:UUID, point_service: PointService = Depends(get_point_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await point_service.get_point_by_id(point_id)

@router.post("/create", response_model=Point, status_code=status.HTTP_201_CREATED)
async def create_point(dev_password: str, point_value: int, point_service: PointService = Depends(get_point_service), current_user=Depends(AuthorizationService.get_current_user)):
    return await point_service.create_point(dev_password, point_value)
