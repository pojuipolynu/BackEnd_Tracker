from fastapi import FastAPI
from core.config import settings
import uvicorn
from routers.user_router import router as user_router
from routers.room_router import router as room_router
from routers.point_router import router as point_router
# from routers.healthcheck import router as healthcheck_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(user_router)
app.include_router(room_router)
app.include_router(point_router)
# app.include_router(healthcheck_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# async def read_main():
#     return { "status_code": 200,
#             "detail": "ok",
#             "result": "working"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=settings.PORT, log_level="info", host=settings.HOST)