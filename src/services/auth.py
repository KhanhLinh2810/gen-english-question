
# from typing import Dict
# import jwt
# from datetime import datetime, timezone, timedelta
# from sqlalchemy.ext.asyncio import AsyncSession


# from src.utils.exceptions import BadRequestException
# from src.utils.password import PasswordUtils
# from src.interfaces.auth import ILogin
# from src.repositories.auth import AuthRepository
# from src.dtos.user import UserDto
# from env import config


# class AuthService:
#     def __init__(self, repo: AuthRepository):
#         self.repo = repo

#     async def authenticate(self, db: AsyncSession, data: ILogin) -> UserDto:
#         user = await self.repo.find_by_username(db, data.username)

#         if not user:
#             raise BadRequestException('username_not_match')
#         if not PasswordUtils.check_password(data.password, user.password):
#             raise BadRequestException('password_not_match')
#         return self.create_access_token({
#             "id": "1",
#             "username": user.username,
#             "email": user.email,
#         })

#     @staticmethod
#     def create_access_token(data: Dict) -> UserDto:
#         data_encoded = data.copy()
#         data_encoded.update({"exp": datetime.now(timezone.utc) + timedelta(hours=config["jwt"]["expired_in"])})
#         token = jwt.encode(data_encoded, config["jwt"]["secret_key"], algorithm=config["jwt"]["algorithm"])
#         return token


# def get_auth_service() -> AuthService:
#     auth_repo = AuthRepository()
#     return AuthService(auth_repo)


