from fastapi import FastAPI, Request, HTTPException
from fastapi.concurrency import asynccontextmanager


from src.loaders.database import init_db
from src.services.schedule.verify_answer_by_ai import verify_answer_by_ai
from src.routers.public.public import router
from src.utils.response import handler_error
from apscheduler.schedulers.asyncio import AsyncIOScheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    scheduler = AsyncIOScheduler()    
    # Chạy lúc 3 giờ sáng mỗi ngày
    scheduler.add_job(
        verify_answer_by_ai, 
        trigger='cron', 
        hour=3, 
        minute=0
    )
    # scheduler.add_job(
    #     verify_answer_by_ai, 
    #     trigger='interval', 
    #     seconds=12,
    #     max_instances=1,  # Chỉ chạy 1 instance tại 1 thời điểm
    #     misfire_grace_time=1500  # Cho phép trễ tối đa 30s
    # )
    scheduler.start()

        
    yield  
    
    scheduler.shutdown()
    
app = FastAPI(lifespan=lifespan)
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return handler_error(exc)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return handler_error(exc)

@app.get('/check-health')
def check_health():
    return {"status": "ok"}

app.include_router(router)

if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)