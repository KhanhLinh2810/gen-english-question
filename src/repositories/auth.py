# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession


# from src.interfaces.user import  *
# from src.models.user import User

# class AuthRepository():
#     async def find_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
#         query = select(User).where(User.username == username)
#         result = await db.execute(query)
#         return await result.scalar_one_or_none()