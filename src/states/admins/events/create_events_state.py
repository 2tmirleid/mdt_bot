from aiogram.fsm.state import StatesGroup, State


class CreateEventsState(StatesGroup):
    photo = State()
    title = State()
    description = State()
    event_date = State()
    city = State()
