import json
from typing import Any, Sequence
from uuid import UUID

from app.models import User
from app.redis_client import redis_client
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    USER_TTL_SECONDS = 3600

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def get_by_id(self, user_id: UUID) -> User | None:
        cache_key = f"user:{user_id}"

        # 1. Пытаемся прочитать из Redis
        cached = redis_client.get(cache_key)
        if cached is not None:
            # принтуем, если читаем из Redis
            print("from cache")
            data = json.loads(cached)
            user = User(
                id=UUID(data["id"]),
                username=data["username"],
                email=data["email"],
                description=data["description"],
            )
            user.created_at = data.get("created_at")
            user.updated_at = data.get("updated_at")
            return user

        # 2. Если в кэше нет — идём в БД
        user = await self.user_repository.get_by_id(user_id)
        if user is not None:
            data_dict = {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "description": user.description,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            }
            redis_client.setex(
                cache_key,
                self.USER_TTL_SECONDS,
                json.dumps(data_dict),
            )
        return user

    async def get_by_filter(
        self,
        count: int,
        page: int,
        **kwargs: Any,
    ) -> Sequence[User]:
        return await self.user_repository.get_by_filter(
            count=count, page=page, **kwargs
        )

    async def create(self, data: UserCreate) -> User:
        user = User(
            username=data.username,
            email=data.email,
            description=data.description,
        )
        user = await self.user_repository.create(user)

        # сразу складывается в кэш созданный пользоватль
        cache_key = f"user:{user.id}"
        data_dict = {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "description": user.description,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        }
        redis_client.setex(
            cache_key,
            self.USER_TTL_SECONDS,
            json.dumps(data_dict),
        )
        return user

    async def update(self, user: User) -> User:
        user = await self.user_repository.update(user)
        cache_key = f"user:{user.id}"
        redis_client.delete(cache_key)  # очистка кэша при обновлении
        return user

    async def delete(self, user_id: UUID) -> None:
        await self.user_repository.delete(user_id)
        cache_key = f"user:{user_id}"
        redis_client.delete(cache_key)  # очистка при удалении
