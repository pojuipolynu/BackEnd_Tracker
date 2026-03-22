from  services.redis_service import redis_client
from fastapi import APIRouter

router = APIRouter(prefix="/healthcheck")

@router.get("/redis", tags=["redis"])
async def redis_db():
    ping_result = await redis_client.ping()
    if ping_result:
        return{"status": "working"}
    else:
        return {"status": "not working", "status_code": 503}