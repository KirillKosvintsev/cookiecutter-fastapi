from typing import Optional

from beanie import Document, Indexed
from pydantic import EmailStr, Field
from pymongo import IndexModel, ASCENDING, HASHED


class User(Document):
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    class Settings:
        name = "users"
        use_state_management = True
        collection = "dataframe_collection"
        indexes = [
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("user_id", ASCENDING), (
                "filename", ASCENDING)], unique=True),
            IndexModel([("parent_id", HASHED)]),
        ]

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "full_name": "John Doe",
                "hashed_password": "secret_hash",
                "is_active": True,
                "is_superuser": False,
            }
        }
