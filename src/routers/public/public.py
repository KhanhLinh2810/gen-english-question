from fastapi import APIRouter

from src.routers.public.quesion import route as question_route
from src.routers.public.auth import router as auth_route

router = APIRouter(prefix="/public", tags=["public"])

print("Including public routes...")
router.include_router(question_route)
router.include_router(auth_route)