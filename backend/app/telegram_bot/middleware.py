from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from app.db.session import async_session_factory
from app.services.admin_service import is_admin


class AdminMiddleware(BaseMiddleware):
    """Этот мидлвар проверяет, является ли пользователь администратором."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """Эта функция проверяет права администратора перед обработкой сообщения."""

        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id if event.from_user else None
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id if event.from_user else None

        if user_id:
            async with async_session_factory() as session:
                if await is_admin(session, user_id):
                    return await handler(event, data)
                else:
                    if isinstance(event, Message):
                        await event.answer("❌ У вас нет прав администратора.")
                    elif isinstance(event, CallbackQuery):
                        await event.answer("❌ У вас нет прав администратора.", show_alert=True)
                    return
        return await handler(event, data)

