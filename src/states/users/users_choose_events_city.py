from aiogram.fsm.state import StatesGroup, State


class UsersChooseEventsCity(StatesGroup):
    city = State()
