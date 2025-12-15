import pytest

from app.models import User


@pytest.mark.asyncio
async def test_create_user(user_repository):
    user = User(
        username="john_doe",
        email="test@example.com",
        description="Test user",
    )

    created = await user_repository.create(user)

    assert created.id is not None
    assert created.username == "john_doe"
    assert created.email == "test@example.com"


@pytest.mark.asyncio
async def test_get_user_by_id(user_repository, session):
    user = User(
        username="user_get",
        email="get@example.com",
        description="Get user",
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    found = await user_repository.get_by_id(user.id)

    assert found is not None
    assert found.id == user.id
    assert found.email == "get@example.com"


@pytest.mark.asyncio
async def test_update_user(user_repository, session):
    user = User(
        username="old_name",
        email="old@example.com",
        description="Old",
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.username = "new_name"
    user.description = "Updated"

    updated = await user_repository.update(user)

    assert updated.username == "new_name"
    assert updated.description == "Updated"
