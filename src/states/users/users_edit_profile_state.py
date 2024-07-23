from aiogram.fsm.state import StatesGroup, State


class UsersEditProfileState(StatesGroup):
    tg_chat_id = State()
    property = State()
    value = State()
