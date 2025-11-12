from aiogram import Router

from app.telegram_bot.handlers import admin_menu, nominees, nominations, statistics, voting

# Создаём главный роутер для всех хэндлеров
def get_handlers_router() -> Router:
    """Эта функция собирает все хэндлеры бота в один роутер."""

    router = Router()
    router.include_router(admin_menu.router)
    router.include_router(nominations.router)
    router.include_router(nominees.router)
    router.include_router(voting.router)
    router.include_router(statistics.router)
    return router

