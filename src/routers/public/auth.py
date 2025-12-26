# from fastapi import APIRouter, Depends
# from fastapi.responses import JSONResponse
# from sqlalchemy.ext.asyncio import AsyncSession

# from src.interfaces.auth import ILogin
# from src.interfaces.user import ICreateUser
# from src.services.auth import AuthService, get_auth_service
# from src.utils.response import res_ok
# from src.services.user import UserService, get_user_service
# from src.loaders.database import get_db

# router = APIRouter(prefix="/auth", tags=["auth"])


# @router.post("/login")
# async def login(user: ILogin, db: AsyncSession = Depends(get_db), auth_service: AuthService = Depends(get_auth_service)):
#     token = await auth_service.authenticate(db, user)

#     return JSONResponse(
#         status_code=200,
#         content=res_ok({
#             "access_token": token,
#         }),
#     )

# @router.post("/register")
# async def register(user: ICreateUser, db: AsyncSession = Depends(get_db), user_service: UserService = Depends(get_user_service)):
#     new_user = await user_service.store(db, user)
#     return JSONResponse(
#         status_code=200,
#         content=res_ok(new_user.model_dump())
#     )

