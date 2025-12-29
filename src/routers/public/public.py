from fastapi import APIRouter, Depends

from src.routers.public.quesion_openai import route as question_route
# from src.routers.public.auth import router as auth_route
from src.middlewares.authenticate import authenticate


router = APIRouter(prefix="/public", tags=["public"], dependencies=[Depends(authenticate)])

print("Including public routes...")
router.include_router(question_route)
# router.include_router(auth_route)
