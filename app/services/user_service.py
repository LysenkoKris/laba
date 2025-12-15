from typing import Any, Sequence
from uuid import UUID

from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self.user_repository.get_by_id(user_id)

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
        return await self.user_repository.create(user)

    async def update(self, user: User) -> User:
        return await self.user_repository.update(user)

    async def delete(self, user_id: UUID) -> None:
        await self.user_repository.delete(user_id)
