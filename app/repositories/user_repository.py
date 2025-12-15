from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import delete as sa_delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Address, Order, User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.scalars(stmt)
        return result.first()

    async def get_by_filter(
        self,
        count: int,
        page: int,
        **kwargs: Any,
    ) -> Sequence[User]:
        stmt = select(User)
        for field, value in kwargs.items():
            if value is None:
                continue
            stmt = stmt.where(getattr(User, field) == value)
        stmt = stmt.limit(count).offset((page - 1) * count)
        result = await self.session.scalars(stmt)
        return result.all()

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: UUID) -> None:
        stmt_orders = sa_delete(Order).where(
            Order.address_id.in_(select(Address.id).where(Address.user_id == user_id))
        )
        await self.session.execute(stmt_orders)

        stmt_addresses = sa_delete(Address).where(Address.user_id == user_id)
        await self.session.execute(stmt_addresses)

        stmt_user = sa_delete(User).where(User.id == user_id)
        await self.session.execute(stmt_user)

        await self.session.commit()
