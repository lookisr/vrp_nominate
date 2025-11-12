import os
from pathlib import Path

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from app.core.config import settings
from app.db.models import Nomination
from app.db.session import async_session_factory
from app.schemas.nomination import NominationResponse
from app.services.nomination_service import get_all_nominations
from app.telegram_bot.states import CreateNominationState, EditNominationState
from app.utils.image_validator import validate_image_square

router = Router()


def get_nominations_keyboard(nominations: list[NominationResponse]) -> InlineKeyboardMarkup:
    """Эта функция создаёт клавиатуру со списком номинаций."""

    buttons = []
    for nom in nominations:
        buttons.append(
            [InlineKeyboardButton(text=nom.title, callback_data=f"nomination_{nom.id}")]
        )
    buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data="admin_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_nomination_actions_keyboard(nomination_id: int) -> InlineKeyboardMarkup:
    """Эта функция создаёт клавиатуру с действиями для номинации."""

    keyboard = [
        [
            InlineKeyboardButton(
                text="✏️ Изменить название", callback_data=f"edit_nom_title_{nomination_id}"
            ),
            InlineKeyboardButton(
                text="🖼️ Заменить фото", callback_data=f"edit_nom_image_{nomination_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🗑️ Удалить", callback_data=f"delete_nomination_{nomination_id}"
            ),
        ],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="admin_nominations")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.callback_query(lambda c: c.data == "admin_nominations")
async def show_nominations_menu(callback: CallbackQuery) -> None:
    """Этот хэндлер показывает меню управления номинациями."""

    async with async_session_factory() as session:
        nominations = await get_all_nominations(session)

    keyboard = [
        [InlineKeyboardButton(text="➕ Создать номинацию", callback_data="create_nomination")],
    ]
    if nominations:
        keyboard.append([InlineKeyboardButton(text="📋 Список номинаций", callback_data="list_nominations")])
    keyboard.append([InlineKeyboardButton(text="◀️ Назад", callback_data="admin_menu")])

    await callback.message.edit_text(
        "📋 <b>Управление номинациями</b>\n\nВыберите действие:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "create_nomination")
async def start_create_nomination(callback: CallbackQuery, state: FSMContext) -> None:
    """Этот хэндлер начинает процесс создания номинации."""

    await state.set_state(CreateNominationState.waiting_for_title)
    await callback.message.edit_text(
        "📝 <b>Создание номинации</b>\n\nВведите название номинации:"
    )
    await callback.answer()


@router.message(CreateNominationState.waiting_for_title)
async def process_nomination_title(message: Message, state: FSMContext) -> None:
    """Этот хэндлер обрабатывает название номинации."""

    title = message.text.strip()
    if not title:
        await message.answer("❌ Название не может быть пустым. Попробуйте снова:")
        return

    await state.update_data(title=title)
    await state.set_state(CreateNominationState.waiting_for_image)
    await message.answer("📸 Отправьте квадратное изображение для номинации:")


@router.message(CreateNominationState.waiting_for_image)
async def process_nomination_image(message: Message, state: FSMContext) -> None:
    """Этот хэндлер обрабатывает изображение номинации."""

    if not message.photo:
        await message.answer("❌ Пожалуйста, отправьте изображение:")
        return

    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_data = await message.bot.download_file(file.file_path)

    image_data = file_data.read() if hasattr(file_data, 'read') else file_data
    is_valid, error_msg = validate_image_square(image_data)
    if not is_valid:
        await message.answer(f"❌ {error_msg}\nПопробуйте снова:")
        return

    # Сохраняем изображение
    data = await state.get_data()
    title = data.get("title")
    if not title:
        await message.answer("❌ Ошибка: название не найдено. Начните заново.")
        await state.clear()
        return

    # Создаём директорию для изображений
    media_dir = Path(settings.media_folder) / "nominations"
    media_dir.mkdir(parents=True, exist_ok=True)

    # Сохраняем файл
    file_extension = Path(file.file_path).suffix or ".jpg"
    file_name = f"{title.lower().replace(' ', '_')}{file_extension}"
    file_path = media_dir / file_name
    file_path.write_bytes(image_data)

    # Сохраняем в БД
    async with async_session_factory() as session:
        nomination = Nomination(
            title=title,
            image_path=str(file_path.relative_to(Path(settings.media_folder))),
        )
        session.add(nomination)
        await session.commit()

    await state.clear()
    await message.answer(f"✅ Номинация <b>{title}</b> успешно создана!")


@router.callback_query(lambda c: c.data == "list_nominations")
async def list_nominations(callback: CallbackQuery) -> None:
    """Этот хэндлер показывает список номинаций."""

    async with async_session_factory() as session:
        nominations = await get_all_nominations(session)

    if not nominations:
        await callback.message.edit_text(
            "📋 Список номинаций пуст.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="◀️ Назад", callback_data="admin_nominations")]]
            ),
        )
        await callback.answer()
        return

    await callback.message.edit_text(
        "📋 <b>Список номинаций</b>\n\nВыберите номинацию:",
        reply_markup=get_nominations_keyboard(nominations),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("nomination_"))
async def show_nomination_details(callback: CallbackQuery) -> None:
    """Этот хэндлер показывает детали номинации и действия."""

    nomination_id = int(callback.data.split("_")[1])
    async with async_session_factory() as session:
        from sqlalchemy import select

        result = await session.execute(select(Nomination).where(Nomination.id == nomination_id))
        nomination = result.scalar_one_or_none()

    if not nomination:
        await callback.answer("❌ Номинация не найдена.", show_alert=True)
        return

    await callback.message.edit_text(
        f"📋 <b>{nomination.title}</b>\n\nВыберите действие:",
        reply_markup=get_nomination_actions_keyboard(nomination_id),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("delete_nomination_"))
async def delete_nomination(callback: CallbackQuery) -> None:
    """Этот хэндлер удаляет номинацию."""

    nomination_id = int(callback.data.split("_")[2])
    async with async_session_factory() as session:
        from sqlalchemy import select

        result = await session.execute(select(Nomination).where(Nomination.id == nomination_id))
        nomination = result.scalar_one_or_none()

        if nomination:
            # Удаляем файл изображения
            image_path = Path(settings.media_folder) / nomination.image_path
            if image_path.exists():
                image_path.unlink()

            await session.delete(nomination)
            await session.commit()
            await callback.message.edit_text("✅ Номинация удалена.")
        else:
            await callback.answer("❌ Номинация не найдена.", show_alert=True)

    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("edit_nom_title_"))
async def start_edit_nomination_title(callback: CallbackQuery, state: FSMContext) -> None:
    """Этот хэндлер начинает редактирование названия номинации."""

    nomination_id = int(callback.data.split("_")[3])
    await state.update_data(nomination_id=nomination_id)
    await state.set_state(EditNominationState.waiting_for_new_title)
    await callback.message.edit_text("✏️ Введите новое название номинации:")
    await callback.answer()


@router.message(EditNominationState.waiting_for_new_title)
async def process_new_nomination_title(message: Message, state: FSMContext) -> None:
    """Этот хэндлер обрабатывает новое название номинации."""

    new_title = message.text.strip()
    if not new_title:
        await message.answer("❌ Название не может быть пустым. Попробуйте снова:")
        return

    data = await state.get_data()
    nomination_id = data.get("nomination_id")
    if not nomination_id:
        await message.answer("❌ Ошибка: ID номинации не найден.")
        await state.clear()
        return

    async with async_session_factory() as session:
        from sqlalchemy import select

        result = await session.execute(select(Nomination).where(Nomination.id == nomination_id))
        nomination = result.scalar_one_or_none()

        if nomination:
            nomination.title = new_title
            await session.commit()
            await message.answer(f"✅ Название номинации изменено на <b>{new_title}</b>")
        else:
            await message.answer("❌ Номинация не найдена.")

    await state.clear()


@router.callback_query(lambda c: c.data and c.data.startswith("edit_nom_image_"))
async def start_edit_nomination_image(callback: CallbackQuery, state: FSMContext) -> None:
    """Этот хэндлер начинает редактирование изображения номинации."""

    nomination_id = int(callback.data.split("_")[3])
    await state.update_data(nomination_id=nomination_id)
    await state.set_state(EditNominationState.waiting_for_new_image)
    await callback.message.edit_text("📸 Отправьте новое квадратное изображение:")
    await callback.answer()


@router.message(EditNominationState.waiting_for_new_image)
async def process_new_nomination_image(message: Message, state: FSMContext) -> None:
    """Этот хэндлер обрабатывает новое изображение номинации."""

    if not message.photo:
        await message.answer("❌ Пожалуйста, отправьте изображение:")
        return

    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_data = await message.bot.download_file(file.file_path)

    image_data = file_data.read() if hasattr(file_data, 'read') else file_data
    is_valid, error_msg = validate_image_square(image_data)
    if not is_valid:
        await message.answer(f"❌ {error_msg}\nПопробуйте снова:")
        return

    data = await state.get_data()
    nomination_id = data.get("nomination_id")
    if not nomination_id:
        await message.answer("❌ Ошибка: ID номинации не найден.")
        await state.clear()
        return

    async with async_session_factory() as session:
        from sqlalchemy import select

        result = await session.execute(select(Nomination).where(Nomination.id == nomination_id))
        nomination = result.scalar_one_or_none()

        if nomination:
            # Удаляем старое изображение
            old_image_path = Path(settings.media_folder) / nomination.image_path
            if old_image_path.exists():
                old_image_path.unlink()

            # Сохраняем новое изображение
            media_dir = Path(settings.media_folder) / "nominations"
            media_dir.mkdir(parents=True, exist_ok=True)

            file_extension = Path(file.file_path).suffix or ".jpg"
            file_name = f"{nomination.title.lower().replace(' ', '_')}{file_extension}"
            file_path = media_dir / file_name
            file_path.write_bytes(image_data)

            nomination.image_path = str(file_path.relative_to(Path(settings.media_folder)))
            await session.commit()
            await message.answer("✅ Изображение номинации обновлено.")
        else:
            await message.answer("❌ Номинация не найдена.")

    await state.clear()

