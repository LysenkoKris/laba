from unittest.mock import AsyncMock

import pytest

from app.schemas.user import UserCreate
from app.services.user_service import UserService


@pytest.mark.asyncio
async def test_service_create_user_builds_model_and_calls_repo():
    mock_repo = AsyncMock()
    service = UserService(user_repository=mock_repo)

    data = UserCreate(
        username="service_user",
        email="service@example.com",
        description="From service",
    )

    mock_user = AsyncMock()
    mock_user.username = "service_user"
    mock_user.email = "service@example.com"
    mock_repo.create.return_value = mock_user

    result = await service.create(data)

    mock_repo.create.assert_awaited_once()
    called_user = mock_repo.create.call_args.args[0]
    assert called_user.username == "service_user"
    assert called_user.email == "service@example.com"
    assert result.email == "service@example.com"
