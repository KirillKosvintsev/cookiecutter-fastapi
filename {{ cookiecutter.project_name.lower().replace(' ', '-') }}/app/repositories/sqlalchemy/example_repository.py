from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from models.sqlalchemy.example_model import User
from typing import List, Optional


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def create_user(self, email: str, hashed_password: str) -> User:
        user = User(email=email, hashed_password=hashed_password)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        await self.db.execute(
            update(User).
            where(User.id == user_id).
            values(**kwargs)
        )
        await self.db.commit()
        return await self.get_user_by_id(user_id)

    async def delete_user(self, user_id: int) -> bool:
        result = await self.db.execute(
            delete(User).where(User.id == user_id)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def count_users(self) -> int:
        result = await self.db.execute(select(func.count()).select_from(User))
        return result.scalar_one()

    async def get_active_users(self) -> List[User]:
        result = await self.db.execute(select(User).filter(User.is_active == True))
        return result.scalars().all()

    async def deactivate_user(self, user_id: int) -> Optional[User]:
        return await self.update_user(user_id, is_active=False)

    async def activate_user(self, user_id: int) -> Optional[User]:
        return await self.update_user(user_id, is_active=True)