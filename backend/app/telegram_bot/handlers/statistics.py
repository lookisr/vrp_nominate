from aiogram import Router
from aiogram.types import BufferedInputFile, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from app.db.session import async_session_factory
from app.schemas.nomination import NominationResponse
from app.services.nomination_service import get_all_nominations
from app.services.result_service import get_results_by_nomination
from app.telegram_bot.states import StatisticsState

router = Router()


def get_nominations_for_stats_keyboard(nominations: list[NominationResponse]) -> InlineKeyboardMarkup:
    """Эта функция создаёт клавиатуру со списком номинаций для статистики."""

    buttons = []
    for nom in nominations:
        buttons.append(
            [InlineKeyboardButton(text=nom.title, callback_data=f"stats_nomination_{nom.id}")]
        )
    buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data="admin_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(lambda c: c.data == "admin_statistics")
async def show_statistics_menu(callback: CallbackQuery) -> None:
    """Этот хэндлер показывает меню статистики."""

    async with async_session_factory() as session:
        nominations = await get_all_nominations(session)

    if not nominations:
        await callback.message.edit_text(
            "❌ Нет номинаций для отображения статистики.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="◀️ Назад", callback_data="admin_menu")]]
            ),
        )
        await callback.answer()
        return

    await callback.message.edit_text(
        "📊 <b>Статистика</b>\n\nВыберите номинацию:",
        reply_markup=get_nominations_for_stats_keyboard(nominations),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("stats_nomination_"))
async def show_nomination_statistics(callback: CallbackQuery) -> None:
    """Этот хэндлер показывает статистику по номинации."""

    nomination_id = int(callback.data.split("_")[2])
    async with async_session_factory() as session:
        result = await get_results_by_nomination(session, nomination_id)

    if not result:
        await callback.answer("❌ Номинация не найдена.", show_alert=True)
        return

    # Формируем текстовое сообщение со статистикой
    text = f"📊 <b>Статистика: {result.nomination_title}</b>\n\n"
    if not result.nominees:
        text += "Номинантов пока нет."
    else:
        for idx, nominee in enumerate(result.nominees, 1):
            text += f"{idx}. <b>{nominee.name}</b> — {nominee.vote_count} голосов\n"

    keyboard = [
        [InlineKeyboardButton(text="◀️ Назад", callback_data="admin_statistics")],
    ]

    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
    await callback.answer()


@router.callback_query(lambda c: c.data == "admin_export")
async def export_csv(callback: CallbackQuery) -> None:
    """Этот хэндлер экспортирует результаты в CSV файл."""

    import csv
    import io

    async with async_session_factory() as session:
        from app.services.result_service import get_all_results

        results = await get_all_results(session)

    if not results.nominations:
        await callback.answer("❌ Нет данных для экспорта.", show_alert=True)
        return

    # Создаём CSV в памяти
    output = io.StringIO()
    writer = csv.writer(output)

    # Заголовки
    writer.writerow(["Номинация", "Номинант", "Голосов"])

    # Данные
    for nomination_result in results.nominations:
        for nominee in nomination_result.nominees:
            writer.writerow([nomination_result.nomination_title, nominee.name, nominee.vote_count])

    csv_content = output.getvalue()
    output.close()

    # Отправляем файл
    file = BufferedInputFile(csv_content.encode("utf-8"), filename="results.csv")
    await callback.message.answer_document(file, caption="📥 Отчёт по результатам голосования")
    await callback.answer("Отчёт отправлен")

