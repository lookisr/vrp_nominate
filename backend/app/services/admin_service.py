from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models import Admin


async def is_admin(session: AsyncSession, telegram_id: int) -> bool:
    """Эта функция проверяет, является ли пользователь администратором."""

    # Сначала проверяем список из настроек
    if telegram_id in settings.admin_ids:
        return True

    # Затем проверяем базу данных
    result = await session.execute(select(Admin).where(Admin.telegram_id == telegram_id))
    admin = result.scalar_one_or_none()
    return admin is not None


async def add_admin(session: AsyncSession, telegram_id: int) -> Admin:
    """Эта функция добавляет администратора в базу данных."""

    result = await session.execute(select(Admin).where(Admin.telegram_id == telegram_id))
    admin = result.scalar_one_or_none()
    if admin:
        return admin

    admin = Admin(telegram_id=telegram_id)
    session.add(admin)
    await session.commit()
    await session.refresh(admin)
    return admin

