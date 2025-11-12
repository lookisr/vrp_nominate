import asyncio
import logging

from app.telegram_bot.bot import create_bot, create_dispatcher
from app.telegram_bot.handlers import get_handlers_router
from app.telegram_bot.middleware import AdminMiddleware

logger = logging.getLogger(__name__)


async def start_polling() -> None:
    """Эта функция запускает бота в режиме polling."""

    bot = create_bot()
    dp = create_dispatcher()

    # Регистрируем мидлвар
    dp.message.middleware(AdminMiddleware())
    dp.callback_query.middleware(AdminMiddleware())

    # Регистрируем хэндлеры
    dp.include_router(get_handlers_router())

    # Запускаем polling
    logger.info("Telegram bot started in polling mode")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


def run_bot_in_background() -> None:
    """Эта функция запускает бота в фоновом режиме."""

    async def _run():
        try:
            await start_polling()
        except Exception as e:
            logger.error(f"Error running bot: {e}", exc_info=True)

    asyncio.create_task(_run())

