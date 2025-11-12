from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


# Эта секция готовит подключения к базе данных.
# Асинхронный движок для FastAPI
async_engine = create_async_engine(settings.database_url, echo=False, future=True)
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

# Синхронный движок для Alembic (миграции работают синхронно)
sync_dsn = settings.database_url.replace("+asyncpg", "").replace("postgresql+asyncpg://", "postgresql://")
sync_engine = create_engine(sync_dsn, echo=False)


async def get_session() -> AsyncSession:
    """Эта функция отдаёт асинхронную сессию базы данных."""

    async with async_session_factory() as session:
        yield session

