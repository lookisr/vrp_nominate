from pathlib import Path

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from app.core.config import settings
from app.db.models import Nomination, Nominee
from app.db.session import async_session_factory
from app.schemas.nomination import NominationResponse
from app.services.nomination_service import get_all_nominations
from app.telegram_bot.states import CreateNomineeState, EditNomineeState
from app.utils.image_validator import validate_image_square

router = Router()


def get_nominations_for_nominee_keyboard(nominations: list[NominationResponse]) -> InlineKeyboardMarkup:
    """Эта функция создаёт клавиатуру со списком номинаций для выбора."""

    buttons = []
    for nom in nominations:
        buttons.append(
            [InlineKeyboardButton(text=nom.title, callback_data=f"select_nom_for_nominee_{nom.id}")]
        )
    buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data="admin_nominees")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_nominees_keyboard(nomination_id: int, nominees: list) -> InlineKeyboardMarkup:
    """Эта функция создаёт клавиатуру со списком номинантов."""

    buttons = []
    for nominee in nominees:
        buttons.append(
            [InlineKeyboardButton(text=nominee.name, callback_data=f"nominee_{nominee.id}")]
        )
    buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data="admin_nominees")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_nominee_actions_keyboard(nominee_id: int) -> InlineKeyboardMarkup:
    """Эта функция создаёт клавиатуру с действиями для номинанта."""

    keyboard = [
        [
            InlineKeyboardButton(
                text="✏️ Изменить имя", callback_data=f"edit_nominee_name_{nominee_id}"
            ),
            InlineKeyboardButton(
                text="🖼️ Заменить фото", callback_data=f"edit_nominee_image_{nominee_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🗑️ Удалить", callback_data=f"delete_nominee_{nominee_id}"
            ),
        ],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="admin_nominees")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.callback_query(lambda c: c.data == "admin_nominees")
async def show_nominees_menu(callback: CallbackQuery) -> None:
    """Этот хэндлер показывает меню управления номинантами."""

    async with async_session_factory() as session:
        nominations = await get_all_nominations(session)

    if not nominations:
        await callback.message.edit_text(
            "❌ Сначала создайте номинацию.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="◀️ Назад", callback_data="admin_menu")]]
            ),
        )
        await callback.answer()
        return

    keyboard = [
        [InlineKeyboardButton(text="➕ Добавить номинанта", callback_data="create_nominee")],
        [InlineKeyboardButton(text="📋 Список номинантов", callback_data="list_nominees")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="admin_menu")],
    ]

    await callback.message.edit_text(
        "👤 <b>Управление номинантами</b>\n\nВыберите действие:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "create_nominee")
async def start_create_nominee(callback: CallbackQuery, state: FSMContext) -> None:
    """Этот хэндлер начинает процесс создания номинанта."""

    async with async_session_factory() as session:
        nominations = await get_all_nominations(session)

    if not nominations:
        await callback.answer("❌ Сначала создайте номинацию.", show_alert=True)
        return

    await state.set_state(CreateNomineeState.waiting_for_nomination)
    await callback.message.edit_text(
        "📋 Выберите номинацию:",
        reply_markup=get_nominations_for_nominee_keyboard(nominations),
    )
    await callback.answer()


@router.callback_query(
    lambda c: c.data and c.data.startswith("select_nom_for_nominee_"),
    CreateNomineeState.waiting_for_nomination,
)
async def process_nomination_for_nominee(callback: CallbackQuery, state: FSMContext) -> None:
    """Этот хэндлер обрабатывает выбор номинации для номинанта."""

    nomination_id = int(callback.data.split("_")[4])
    await state.update_data(nomination_id=nomination_id)
    await state.set_state(CreateNomineeState.waiting_for_name)
    await callback.message.edit_text("👤 Введите имя номинанта:")
    await callback.answer()


@router.message(CreateNomineeState.waiting_for_name)
async def process_nominee_name(message: Message, state: FSMContext) -> None:
    """Этот хэндлер обрабатывает имя номинанта."""

    name = message.text.strip()
    if not name:
        await message.answer("❌ Имя не может быть пустым. Попробуйте снова:")
        return

    await state.update_data(name=name)
    await state.set_state(CreateNomineeState.waiting_for_image)
    await message.answer("📸 Отправьте квадратное изображение номинанта:")


@router.message(CreateNomineeState.waiting_for_image)
async def process_nominee_image(message: Message, state: FSMContext) -> None:
    """Этот хэндлер обрабатывает изображение номинанта."""

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
    name = data.get("name")

    if not nomination_id or not name:
        await message.answer("❌ Ошибка: данные не найдены. Начните заново.")
        await state.clear()
        return

    # Сохраняем изображение
    media_dir = Path(settings.media_folder) / "nominees"
    media_dir.mkdir(parents=True, exist_ok=True)

    file_extension = Path(file.file_path).suffix or ".jpg"
    file_name = f"{name.lower().replace(' ', '_')}_{nomination_id}{file_extension}"
    file_path = media_dir / file_name
    file_path.write_bytes(image_data)

    # Сохраняем в БД
    async with async_session_factory() as session:
        nominee = Nominee(
            nomination_id=nomination_id,
            name=name,
            image_path=str(file_path.relative_to(Path(settings.media_folder))),
        )
        session.add(nominee)
        await session.commit()

    await state.clear()
    await message.answer(f"✅ Номинант <b>{name}</b> успешно добавлен!")


@router.callback_query(lambda c: c.data == "list_nominees")
async def list_nominees(callback: CallbackQuery) -> None:
    """Этот хэндлер показывает список номинаций для выбора номинантов."""

    async with async_session_factory() as session:
        nominations = await get_all_nominations(session)

    if not nominations:
        await callback.message.edit_text(
            "❌ Нет номинаций.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="◀️ Назад", callback_data="admin_nominees")]]
            ),
        )
        await callback.answer()
        return

    await callback.message.edit_text(
        "📋 Выберите номинацию для просмотра номинантов:",
        reply_markup=get_nominations_for_nominee_keyboard(nominations),
    )
    await callback.answer()


@router.callback_query(
    lambda c: c.data and c.data.startswith("select_nom_for_nominee_"),
)
async def show_nominees_by_nomination(callback: CallbackQuery) -> None:
    """Этот хэндлер показывает список номинантов по номинации."""

    nomination_id = int(callback.data.split("_")[4])
    async with async_session_factory() as session:
        from sqlalchemy import select

        result = await session.execute(
            select(Nominee).where(Nominee.nomination_id == nomination_id).order_by(Nominee.name)
        )
        nominees = result.scalars().all()

    if not nominees:
        await callback.message.edit_text(
            "👤 Номинантов в этой номинации пока нет.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="◀️ Назад", callback_data="list_nominees")]]
            ),
        )
        await callback.answer()
        return

    nominees_list = [{"id": n.id, "name": n.name} for n in nominees]
    await callback.message.edit_text(
        "👤 <b>Список номинантов</b>\n\nВыберите номинанта:",
        reply_markup=get_nominees_keyboard(nomination_id, nominees_list),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("nominee_"))
async def show_nominee_details(callback: CallbackQuery) -> None:
    """Этот хэндлер показывает детали номинанта и действия."""

    nominee_id = int(callback.data.split("_")[1])
    async with async_session_factory() as session:
        from sqlalchemy import select

        result = await session.execute(select(Nominee).where(Nominee.id == nominee_id))
        nominee = result.scalar_one_or_none()

    if not nominee:
        await callback.answer("❌ Номинант не найден.", show_alert=True)
        return

    await callback.message.edit_text(
        f"👤 <b>{nominee.name}</b>\n\nВыберите действие:",
        reply_markup=get_nominee_actions_keyboard(nominee_id),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("delete_nominee_"))
async def delete_nominee(callback: CallbackQuery) -> None:
    """Этот хэндлер удаляет номинанта."""

    nominee_id = int(callback.data.split("_")[2])
    async with async_session_factory() as session:
        from sqlalchemy import select

        result = await session.execute(select(Nominee).where(Nominee.id == nominee_id))
        nominee = result.scalar_one_or_none()

        if nominee:
            # Удаляем файл изображения
            image_path = Path(settings.media_folder) / nominee.image_path
            if image_path.exists():
                image_path.unlink()

            await session.delete(nominee)
            await session.commit()
            await callback.message.edit_text("✅ Номинант удалён.")
        else:
            await callback.answer("❌ Номинант не найден.", show_alert=True)

    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("edit_nominee_name_"))
async def start_edit_nominee_name(callback: CallbackQuery, state: FSMContext) -> None:
    """Этот хэндлер начинает редактирование имени номинанта."""

    nominee_id = int(callback.data.split("_")[3])
    await state.update_data(nominee_id=nominee_id)
    await state.set_state(EditNomineeState.waiting_for_new_name)
    await callback.message.edit_text("✏️ Введите новое имя номинанта:")
    await callback.answer()


@router.message(EditNomineeState.waiting_for_new_name)
async def process_new_nominee_name(message: Message, state: FSMContext) -> None:
    """Этот хэндлер обрабатывает новое имя номинанта."""

    new_name = message.text.strip()
    if not new_name:
        await message.answer("❌ Имя не может быть пустым. Попробуйте снова:")
        return

    data = await state.get_data()
    nominee_id = data.get("nominee_id")
    if not nominee_id:
        await message.answer("❌ Ошибка: ID номинанта не найден.")
        await state.clear()
        return

    async with async_session_factory() as session:
        from sqlalchemy import select

        result = await session.execute(select(Nominee).where(Nominee.id == nominee_id))
        nominee = result.scalar_one_or_none()

        if nominee:
            nominee.name = new_name
            await session.commit()
            await message.answer(f"✅ Имя номинанта изменено на <b>{new_name}</b>")
        else:
            await message.answer("❌ Номинант не найден.")

    await state.clear()


@router.callback_query(lambda c: c.data and c.data.startswith("edit_nominee_image_"))
async def start_edit_nominee_image(callback: CallbackQuery, state: FSMContext) -> None:
    """Этот хэндлер начинает редактирование изображения номинанта."""

    nominee_id = int(callback.data.split("_")[3])
    await state.update_data(nominee_id=nominee_id)
    await state.set_state(EditNomineeState.waiting_for_new_image)
    await callback.message.edit_text("📸 Отправьте новое квадратное изображение:")
    await callback.answer()


@router.message(EditNomineeState.waiting_for_new_image)
async def process_new_nominee_image(message: Message, state: FSMContext) -> None:
    """Этот хэндлер обрабатывает новое изображение номинанта."""

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
    nominee_id = data.get("nominee_id")
    if not nominee_id:
        await message.answer("❌ Ошибка: ID номинанта не найден.")
        await state.clear()
        return

    async with async_session_factory() as session:
        from sqlalchemy import select

        result = await session.execute(select(Nominee).where(Nominee.id == nominee_id))
        nominee = result.scalar_one_or_none()

        if nominee:
            # Удаляем старое изображение
            old_image_path = Path(settings.media_folder) / nominee.image_path
            if old_image_path.exists():
                old_image_path.unlink()

            # Сохраняем новое изображение
            media_dir = Path(settings.media_folder) / "nominees"
            media_dir.mkdir(parents=True, exist_ok=True)

            file_extension = Path(file.file_path).suffix or ".jpg"
            file_name = f"{nominee.name.lower().replace(' ', '_')}_{nominee.nomination_id}{file_extension}"
            file_path = media_dir / file_name
            file_path.write_bytes(image_data)

            nominee.image_path = str(file_path.relative_to(Path(settings.media_folder)))
            await session.commit()
            await message.answer("✅ Изображение номинанта обновлено.")
        else:
            await message.answer("❌ Номинант не найден.")

    await state.clear()

