import asyncio
from db.session import postgres_db
from utils.depends import get_room_service
from app.celery_app import celery_app

async def run_async_task(action: str):
    async for db in postgres_db():
        room_service = get_room_service(db)
        
        if action == "reduce_hp":
            await room_service.apply_daily_pet_reduce()
        elif action == "reset_progress":
            await room_service.reset_weekly_progress()

@celery_app.task(name="reduce_hp_task")
def reduce_hp():
    asyncio.run(run_async_task("reduce_hp"))

@celery_app.task(name="reset_progress_task")
def reset_progress():
    asyncio.run(run_async_task("reset_progress"))