from aiogram.fsm.state import State, StatesGroup


class CreateNominationState(StatesGroup):
    """Состояния для создания номинации."""

    waiting_for_title = State()
    waiting_for_image = State()


class EditNominationState(StatesGroup):
    """Состояния для редактирования номинации."""

    waiting_for_nomination = State()
    waiting_for_action = State()
    waiting_for_new_title = State()
    waiting_for_new_image = State()


class CreateNomineeState(StatesGroup):
    """Состояния для создания номинанта."""

    waiting_for_nomination = State()
    waiting_for_name = State()
    waiting_for_image = State()


class EditNomineeState(StatesGroup):
    """Состояния для редактирования номинанта."""

    waiting_for_nomination = State()
    waiting_for_nominee = State()
    waiting_for_action = State()
    waiting_for_new_name = State()
    waiting_for_new_image = State()


class StatisticsState(StatesGroup):
    """Состояния для просмотра статистики."""

    waiting_for_nomination = State()

