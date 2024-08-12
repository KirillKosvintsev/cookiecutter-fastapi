from typing import List, Optional
from beanie import PydanticObjectId
from app.models.example_model import User


class UserRepository:
    async def get_user_by_id(self, user_id: PydanticObjectId) -> Optional[User]:
        return await User.get(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await User.find_one(User.email == email)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        return await User.find_one(User.username == username)

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await User.find_all().skip(skip).limit(limit).to_list()

    async def create_user(self, user_data: dict) -> User:
        user = User(**user_data)
        return await user.insert()

    async def update_user(self, user_id: PydanticObjectId, update_data: dict) -> Optional[User]:
        user = await self.get_user_by_id(user_id)
        if user:
            await user.set(update_data)
            return user
        return None

    async def delete_user(self, user_id: PydanticObjectId) -> bool:
        user = await self.get_user_by_id(user_id)
        if user:
            await user.delete()
            return True
        return False

    async def count_users(self) -> int:
        return await User.count()

    async def get_active_users(self) -> List[User]:
        return await User.find(User.is_active == True).to_list()

    async def deactivate_user(self, user_id: PydanticObjectId) -> Optional[User]:
        return await self.update_user(user_id, {"is_active": False})

    async def activate_user(self, user_id: PydanticObjectId) -> Optional[User]:
        return await self.update_user(user_id, {"is_active": True})
