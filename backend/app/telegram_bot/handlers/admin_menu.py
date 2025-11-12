from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from app.db.session import async_session_factory
from app.services.admin_service import is_admin

router = Router()


def get_admin_keyboard() -> InlineKeyboardMarkup:
    """Эта функция создаёт клавиатуру главного меню администратора."""

    keyboard = [
        [
            InlineKeyboardButton(text="📋 Номинации", callback_data="admin_nominations"),
            InlineKeyboardButton(text="👤 Номинанты", callback_data="admin_nominees"),
        ],
        [
            InlineKeyboardButton(text="🗳️ Голосование", callback_data="admin_voting"),
        ],
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="admin_statistics"),
            InlineKeyboardButton(text="📥 Выгрузить отчет", callback_data="admin_export"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    """Этот хэндлер обрабатывает команду /admin."""

    user_id = message.from_user.id if message.from_user else None
    if not user_id:
        await message.answer("❌ Не удалось определить пользователя.")
        return

    async with async_session_factory() as session:
        if await is_admin(session, user_id):
            await message.answer(
                "👋 <b>Панель администратора</b>\n\nВыберите действие:",
                reply_markup=get_admin_keyboard(),
            )
        else:
            await message.answer("❌ У вас нет прав администратора.")


@router.callback_query(lambda c: c.data == "admin_menu")
async def show_admin_menu(callback: CallbackQuery) -> None:
    """Этот хэндлер показывает главное меню администратора."""

    await callback.message.edit_text(
        "👋 <b>Панель администратора</b>\n\nВыберите действие:",
        reply_markup=get_admin_keyboard(),
    )
    await callback.answer()

