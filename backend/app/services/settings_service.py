from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models import Setting


async def get_setting_value(session: AsyncSession, key: str, default: str = "") -> str:
    """Эта функция получает значение настройки по ключу."""

    result = await session.execute(select(Setting).where(Setting.key == key))
    setting = result.scalar_one_or_none()
    if setting:
        return setting.value
    return default


async def set_setting_value(session: AsyncSession, key: str, value: str) -> None:
    """Эта функция устанавливает значение настройки."""

    result = await session.execute(select(Setting).where(Setting.key == key))
    setting = result.scalar_one_or_none()
    if setting:
        setting.value = value
    else:
        setting = Setting(key=key, value=value)
        session.add(setting)
    await session.commit()


async def is_voting_open(session: AsyncSession) -> bool:
    """Эта функция проверяет, открыто ли голосование."""

    value = await get_setting_value(session, "voting_open", str(settings.voting_open_default))
    return value.lower() in ("true", "1", "yes", "on")

