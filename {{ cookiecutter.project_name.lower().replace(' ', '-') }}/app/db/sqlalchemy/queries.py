from loguru import logger

from db.sqlalchemy.session import AsyncSessionLocal


# Функция для выполнения SQL-запроса
async def execute_raw_sql(sql: str, params: dict = None):
    async with AsyncSessionLocal() as session:
        result = await session.execute(sql, params)
        await session.commit()
        return result


# Функция для проверки соединения с базой данных
async def check_db_connection():
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

