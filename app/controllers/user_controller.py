from typing import Any
from uuid import UUID

from litestar import Controller, get, post, put, delete
from litestar.params import Parameter
from litestar.exceptions import NotFoundException

from app.models import User
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse


class UserController(Controller):
    path = "/users"

    @get("/{user_id:uuid}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        user_id: UUID,
    ) -> dict:
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        }


    @get()
    async def get_all_users(
        self,
        user_service: UserService,
    ) -> dict[str, Any]:
        users = await user_service.get_by_filter(count=100, page=1)
        items = [
            {
                "id": str(u.id),
                "username": u.username,
                "email": u.email,
                "created_at": u.created_at.isoformat() if u.created_at else None,
                "updated_at": u.updated_at.isoformat() if u.updated_at else None,
            }
            for u in users
        ]
        return {
            "items": items,
            "total": len(items),
        }

    @post()
    async def create_user(
        self,
        user_service: UserService,
        data: UserCreate,
    ) -> UserResponse:
        user = await user_service.create(data)
        return UserResponse.from_orm(user)

    @put("/{user_id:uuid}")
    async def update_user(
        self,
        user_service: UserService,
        user_id: UUID,      # UUID вместо int
        data: UserCreate,   # тело запроса, как в примере
    ) -> UserResponse:
        """Обновление пользователя по UUID."""

        user = await user_service.get_by_id(user_id)

        user.username = data.username
        user.email = data.email
        user.description = data.description

        updated = await user_service.update(user)
        return UserResponse.from_orm(updated)

    @delete("/{user_id:uuid}")
    async def delete_user(
        self,
        user_service: UserService,
        user_id: UUID,
    ) -> None:
        await user_service.delete(user_id)

