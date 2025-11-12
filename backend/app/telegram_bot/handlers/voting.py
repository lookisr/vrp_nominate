from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from app.db.session import async_session_factory
from app.services.settings_service import is_voting_open, set_setting_value

router = Router()


def get_voting_keyboard(is_open: bool) -> InlineKeyboardMarkup:
    """Эта функция создаёт клавиатуру для управления голосованием."""

    status_text = "🟢 Открыто" if is_open else "🔴 Закрыто"
    keyboard = [
        [
            InlineKeyboardButton(
                text="▶️ Старт" if not is_open else "⏸️ Остановить",
                callback_data="voting_start" if not is_open else "voting_stop",
            ),
        ],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="admin_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.callback_query(lambda c: c.data == "admin_voting")
async def show_voting_menu(callback: CallbackQuery) -> None:
    """Этот хэндлер показывает меню управления голосованием."""

    async with async_session_factory() as session:
        voting_open = await is_voting_open(session)
        status_text = "🟢 Открыто" if voting_open else "🔴 Закрыто"

    await callback.message.edit_text(
        f"🗳️ <b>Управление голосованием</b>\n\nТекущий статус: {status_text}\n\nВыберите действие:",
        reply_markup=get_voting_keyboard(voting_open),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "voting_start")
async def start_voting(callback: CallbackQuery) -> None:
    """Этот хэндлер запускает голосование."""

    async with async_session_factory() as session:
        await set_setting_value(session, "voting_open", "true")

    await callback.message.edit_text(
        "✅ <b>Голосование запущено!</b>\n\nТеперь пользователи могут голосовать в Mini App.",
        reply_markup=get_voting_keyboard(True),
    )
    await callback.answer("Голосование запущено")


@router.callback_query(lambda c: c.data == "voting_stop")
async def stop_voting(callback: CallbackQuery) -> None:
    """Этот хэндлер останавливает голосование."""

    async with async_session_factory() as session:
        await set_setting_value(session, "voting_open", "false")

    await callback.message.edit_text(
        "⏸️ <b>Голосование остановлено.</b>\n\nПользователи больше не могут голосовать.",
        reply_markup=get_voting_keyboard(False),
    )
    await callback.answer("Голосование остановлено")

