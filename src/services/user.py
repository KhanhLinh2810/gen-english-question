from src.interfaces.auth import IPagination
from src.interfaces.user import ICreateUser, IFilterUser, IUpdateUser
from src.repositories.user import UserRepository
from src.dtos.user import UserDto
from src.models.user import User
from src.utils.password import PasswordUtils
from src.utils.exceptions import BadRequestException

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def store(self, db: AsyncSession, data: ICreateUser) -> UserDto:
        await self.validate_unique_username(db, data.username)

        hashed_password = PasswordUtils.hash_password(data.password)
        user_data = data.model_copy(update={"password": hashed_password})

        new_user = await self.repo.store(db, data=user_data)

        return UserDto.model_validate(new_user)

    async def update(self, db: AsyncSession, user_id: int, data: IUpdateUser) -> UserDto:
        user = await self.find_or_fail(db, user_id)
        if data.password:
            hashed_password = PasswordUtils.hash_password(data.password)
            data.update(password= hashed_password)

        updated_user = await self.repo.update(db, user, data)
        return updated_user

    async def delete(self, db: AsyncSession, user_id: int):
        user = await self.find_or_fail(db, user_id)
        await self.repo.delete(db, user)

    async def get_one(self, db: AsyncSession, filter_data: IFilterUser) -> Optional[UserDto]:
        user = await self.repo.get_one(db, filter_data)
        if user is None:
            return None
        else:
            return user

    async def get_many(self, db: AsyncSession, paging: IPagination, filter_data: IFilterUser) -> List[UserDto]:
        list_user = await self.repo.get_many(db, paging, filter_data.user_id)
        return list(map(UserDto.model_validate, list_user))

    async def validate_unique_username(self, db: AsyncSession, username: str):
        old_user = await self.repo.get_one(db, IFilterUser(username=username))
        if old_user:
            raise BadRequestException('username_already_exists')

    async def find_by_pk(self, db: AsyncSession, user_id: int):
        return await self.repo.find_by_pk(db, user_id)

    async def find_or_fail(self, db: AsyncSession, user_id: int) -> User:
        user = await self.find_by_pk(db, user_id)
        if not user:
            raise BadRequestException('user_not_found')

        return user

def get_user_service() -> UserService:
    user_repo = UserRepository()
    return UserService(user_repo)

