import os

from litestar import Litestar
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.controllers.report_controller import ReportController
from app.controllers.user_controller import UserController
from app.db import async_session_factory, provide_db_session
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository(db_session)


async def provide_user_service(user_repository: UserRepository) -> UserService:
    return UserService(user_repository)


app = Litestar(
    route_handlers=[UserController, ReportController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
        "user_service": Provide(provide_user_service),
    },
    debug=True,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
