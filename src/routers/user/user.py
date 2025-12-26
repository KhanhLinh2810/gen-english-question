# from fastapi import APIRouter, Depends
# from fastapi.responses import JSONResponse
# from typing import Optional

# from src.interfaces.user import IUpdateUser, IFilterUser
# from src.interfaces.auth import IPagination
# from src.middlewares.authenticate import authenticate
# from src.services.user import UserService, get_user_service
# from src.utils.response import res_ok

# router = APIRouter(
#     prefix="/users",
#     tags=["users"],
#     dependencies=[Depends(authenticate)]
# )

# @router.get("/")
# async def index(
#         paging: IPagination = Depends(IPagination),
#         keyword: Optional[str] = None,
#         user_service: UserService = Depends(get_user_service),
# ):
#     await user_service.get_many(
#         paging,
#         IFilterUser(username_or_email=keyword)
#     )

#     return JSONResponse(
#         status_code=200,
#         content=res_ok(
#             # result["rows"],
#             10,
#             message="success",
#             page=paging.page,
#             limit=paging.limit,
#             total_item=100
#         )
#     )

# @router.get("/")
# async def index(
#         paging: IPagination = Depends(IPagination),
#         keyword: Optional[str] = None,
#         user_service: UserService = Depends(get_user_service),
# ):
#     await user_service.get_many(
#         paging,
#         IFilterUser(username_or_email=keyword)
#     )

#     return JSONResponse(
#         status_code=200,
#         content=res_ok(
#             # result["rows"],
#             10,
#             message="success",
#             page=paging.page,
#             limit=paging.limit,
#             total_item=100
#         )
#     )

# @router.get("/{user_id}")
# async def detail(user_id: int, user_service: UserService = Depends(get_user_service),):
#     user = await user_service.find_or_fail(user_id)
#     return JSONResponse(
#         status_code=200,
#         content=res_ok(user.dict())
#     )

# @router.put("/{user_id}")
# async def update(user_id: int, user: IUpdateUser, user_service: UserService = Depends(get_user_service),):
#     updated_user = await user_service.update(user_id, user)
#     return JSONResponse(
#         status_code=200,
#         content=res_ok(updated_user.model_dump())
#     )

# @router.delete("/{user_id}")
# async def delete(user_id: int, user_service: UserService = Depends(get_user_service),):
#     await user_service.delete(user_id)
#     return JSONResponse(
#         status_code=200,
#         content=res_ok({"id": user_id})
#     )
