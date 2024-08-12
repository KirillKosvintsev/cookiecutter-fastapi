from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import alembic.config

from app.config.config import settings


# Асинхронный движок SQLAlchemy
engine = create_async_engine(
    settings.database.url,
    echo=settings.database.echo_sql,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow
)

# Фабрика сессий
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Функция для получения сессии базы данных
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Создаем базовый класс для моделей
Base = declarative_base()


# Функция для инициализации базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Функция для закрытия соединения с базой данных
async def close_db():
    await engine.dispose()


# Функция для выполнения миграций
async def run_migrations():
    alembic_cfg = alembic.config.Config("alembic.ini")
    alembic.command.upgrade(alembic_cfg, "head")


# @app.on_event("startup")
# async def startup_event():
#     await run_migrations()
#     await init_db()
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     await close_db()


