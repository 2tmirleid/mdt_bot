from aiogram.fsm.state import StatesGroup, State


class UsersSearchResidentsState(StatesGroup):
    property = State()
    value = State()
