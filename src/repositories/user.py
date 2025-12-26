# from src.interfaces.auth import IPagination
# from src.models.user import User
# from src.repositories.base import ICrudRepository
# from src.interfaces.user import ICreateUser, IFilterUser, IUpdateUser

# from sqlalchemy import select, or_
# from sqlalchemy.sql import Select
# from sqlalchemy.ext.asyncio import AsyncSession
# from typing import Optional



# class UserRepository(ICrudRepository):
#     async def store(self, db: AsyncSession, data: ICreateUser) -> User:
#         new_user = User(**data.model_dump())
#         db.add(new_user)
#         await db.commit()
#         await db.refresh(new_user)

#         return new_user

#     async def update(self, db: AsyncSession, user: User, data: IUpdateUser) -> User :
#         update_data = data.model_dump(exclude_unset=True)
#         for key, value in update_data.items():
#             if hasattr(user, key):
#                 setattr(user, key, value)
        
#         await db.commit()
#         await db.refresh(user)
#         return user

#     async def delete(self, db: AsyncSession, user: User) :
#         await db.delete(user)
#         await db.commit()
#         return User(**user.model_dump())

#     async def find_by_pk(self, db: AsyncSession, user_id: int) -> Optional[User]:
#         return await db.get(User, user_id)

#     async def get_one(self, db: AsyncSession, filter_data: IFilterUser):
#         query = self.build_query(filter_data)
#         result = await db.execute(query)
#         return result.scalar_one_or_none()

#     async def get_many(self, db: AsyncSession, paging: IPagination, filter_data: IFilterUser):
#         query = self.build_query(filter_data)
#         query = query.limit(paging.limit).offset(paging.offset)
#         sort_by = getattr(User, paging.sort_by, None)
#         if sort_by is not None:
#             if paging.sort_order and paging.sort_order.lower() == 'desc':
#                 query = query.order_by(sort_by.desc())
#             else:
#                 query = query.order_by(sort_by.asc())
#         result = await db.execute(query)
#         return result.scalar().all()

#     @staticmethod
#     def build_query(filters: IFilterUser) -> Select:
#         query = select(User)
#         conditions = []
#         if filters.username_or_email:
#             conditions.append(
#                 or_(
#                     filters.username_or_email == User.email,
#                     filters.username_or_email == User.username)
#             )
#         else:
#             if filters.username:
#                 conditions.append(filters.username == User.username)
#             if filters.email:
#                 conditions.append(filters.email == User.email)

#         return query.where(*conditions)