import os
import sys

import pytest
from litestar import Litestar
from litestar.di import Provide
from litestar.testing import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, PROJECT_ROOT)

from app.controllers.user_controller import UserController
from app.models import Base
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def test_engine():
    return create_async_engine(TEST_DATABASE_URL, echo=True)


@pytest.fixture(scope="session")
async def tables(test_engine):
    """Создаёт таблицы в тестовой БД."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def test_db_session(test_engine, tables):
    """Фикстура сессии для тестов."""
    async_session_maker = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_maker() as session:
        yield session


@pytest.fixture
def test_app(test_db_session):
    """Тестовый экземпляр Litestar с переопределёнными зависимостями."""

    async def provide_test_db_session() -> AsyncSession:
        yield test_db_session

    async def provide_test_user_repository(db_session: AsyncSession) -> UserRepository:
        return UserRepository(db_session)

    async def provide_test_user_service(user_repository: UserRepository) -> UserService:
        return UserService(user_repository)

    test_app = Litestar(
        route_handlers=[UserController],
        dependencies={
            "db_session": Provide(provide_test_db_session),
            "user_repository": Provide(provide_test_user_repository),
            "user_service": Provide(provide_test_user_service),
        },
        debug=True,
    )

    return test_app


@pytest.fixture
def client(test_app):
    return TestClient(app=test_app)


@pytest.fixture
async def session(test_db_session):
    yield test_db_session


@pytest.fixture
def user_repository(session):
    return UserRepository(session)
