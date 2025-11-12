from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import settings


def create_bot() -> Bot:
    """Эта функция создаёт экземпляр Telegram-бота."""

    if not settings.telegram_bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN не установлен в переменных окружения")

    return Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


def create_dispatcher() -> Dispatcher:
    """Эта функция создаёт диспетчер для обработки сообщений."""

    storage = MemoryStorage()
    return Dispatcher(storage=storage)

