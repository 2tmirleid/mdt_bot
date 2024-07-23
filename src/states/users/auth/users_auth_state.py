from aiogram.fsm.state import StatesGroup, State


class UsersAuthState(StatesGroup):
    phone = State()
    photo = State()
    full_name = State()
    birth_date = State()
    city = State()
    company = State()
    position = State()
    rm_status = State()
    hobbies = State()
    resources = State()
    expertise = State()
