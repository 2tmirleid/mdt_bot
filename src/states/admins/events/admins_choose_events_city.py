from aiogram.fsm.state import StatesGroup, State


class AdminsChooseEventsCity(StatesGroup):
    city = State()
