from aiogram.fsm.state import StatesGroup, State


class EditEventsState(StatesGroup):
    event_id = State()
    property = State()
    value = State()
